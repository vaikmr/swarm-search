#!/usr/bin/env python3
"""Offline checks of observed one-address components, never full-firm T1."""
import argparse
import datetime as dt
from decimal import Decimal, getcontext
import json
from pathlib import Path
from collect_actor_ledger import ACTOR, USDC, ATOKEN, START, END, TRANSFER
from snapshot_market_identity import validate_header

getcontext().prec = 60
D = Decimal
RAY = 10**27
ZERO = "0x" + "0" * 40


def signed(raw, sender, recipient, actor=ACTOR):
    if actor not in (sender, recipient):
        raise ValueError("Observation does not involve scoped address")
    return int(raw) * ((recipient == actor) - (sender == actor))


def receipt_fee(receipt):
    fee = int(receipt["gasUsed"], 16) * int(receipt["effectiveGasPrice"], 16)
    blob_used, blob_price = receipt.get("blobGasUsed"), receipt.get("blobGasPrice")
    if receipt.get("type") == "0x3" and (blob_used is None or blob_price is None):
        raise ValueError("Missing fee data for blob transaction")
    if (blob_used is None) != (blob_price is None):
        raise ValueError("Incomplete blob fee")
    if blob_used is not None:
        fee += int(blob_used, 16) * int(blob_price, 16)
    return fee


def verify_log(row, receipt):
    if receipt["status"] != "0x1" or int(receipt["blockNumber"], 16) != row["block"]:
        raise ValueError("Transfer receipt failed or wrong block")
    matches = [log for log in receipt["logs"] if int(log["logIndex"], 16) == row["log_index"]]
    if len(matches) != 1:
        raise ValueError("Missing or duplicate receipt log")
    log = matches[0]
    topics = log["topics"]
    if (log["address"].lower() != row["token"] or len(topics) != 3 or topics[0].lower() != TRANSFER
            or ("0x" + topics[1][-40:]).lower() != row["from"]
            or ("0x" + topics[2][-40:]).lower() != row["to"]
            or int(log["data"], 16) != int(row["raw_value"])):
        raise ValueError("Indexer transfer differs from actual receipt")


def check_index(endpoint):
    # Verified deployed AToken's TokenMath.getATokenBalance uses rayMulFloor,
    # not legacy half-up ray multiplication. Do not hide a one-unit mismatch.
    computed = int(endpoint["scaled"]) * int(endpoint["index"]) // RAY
    if computed != int(endpoint["aUSDC"]):
        raise ValueError("Scaled balance and normalized income do not reconcile")


def partition_interest(opening_units, closing_units, flows, after_withdraw):
    """Close segments only when observed post-withdraw aToken inventory is zero."""
    segment_cash, closed_interest, rows = -int(opening_units), 0, []
    for r in sorted(flows, key=lambda x: (x["block"], x["log_index"])):
        v = signed(r["raw_value"], r["from"], r["to"])
        segment_cash += v
        if v > 0:
            remaining = after_withdraw.get(str(r["block"]))
            if remaining is None:
                raise ValueError("Missing observed post-withdraw token balance")
            completed = segment_cash if int(remaining) == 0 else None
            rows.append({"withdraw_block": r["block"], "tx": r["tx"],
                         "cash_withdrawn_usdc": str(D(v) / 10**6),
                         "observed_remaining_aUSDC_units": str(D(remaining) / 10**6),
                         "completed_segment_cash_interest_usdc": str(D(completed) / 10**6) if completed is not None else None})
            if completed is not None:
                closed_interest += completed
                segment_cash = 0
    return closed_interest, int(closing_units) + segment_cash, rows


def reconcile(data):
    if data["actor"] != ACTOR or data["start"] != START or data["end"] != END:
        raise ValueError("Unexpected actor/window")
    begin, end = (data["endpoints"][str(b)] for b in (START, END))
    for block, endpoint in ((START, begin), (END, end)):
        h = endpoint["header"]
        actual = validate_header({"number": h["returned_block_number"], "hash": h["block_hash"],
                                  "timestamp": h["returned_block_timestamp"]}, hex(block))
        if actual != h:
            raise ValueError("Normalized header differs from preserved actual header")
    elapsed = (dt.datetime.fromisoformat(end["header"]["block_time"]) -
               dt.datetime.fromisoformat(begin["header"]["block_time"])).total_seconds()
    if elapsed < 14 * 86400 or elapsed != data["elapsed_seconds"]:
        raise ValueError("Unverified or short actor window")
    currencies = data["oracle_base_currency_at_endpoints"]
    if set(currencies) != {str(START), str(END)} or any(int(v, 16) for v in currencies.values()):
        raise ValueError("USD oracle base convention not established")
    for endpoint in (begin, end):
        check_index(endpoint)
        if int(endpoint["price_unit"]) != 10**8:
            raise ValueError("Unknown oracle scale")
    collateral_residuals = {}
    for tag, endpoint in (("opening", begin), ("closing", end)):
        modeled = int(endpoint["aUSDC"]) * int(endpoint["USDC_price"]) // 10**6
        residual = int(endpoint["aave_account_base_8_decimals"][0]) - modeled
        if residual:
            raise ValueError("Other Aave collateral or pricing difference needs reconstruction")
        collateral_residuals[tag] = residual
    transfers, normal, receipts = data["transfers"], data["normal_transactions"], data["receipts"]
    seen = set()
    internal_usdc, external_usdc, external_atoken = 0, 0, 0
    external_usdc_usd = external_atoken_usd = D(0)

    def price(block, asset):
        return D(data["reference_prices_8_decimals"][str(block) + ":" + asset]) / 10**8

    for r in transfers:
        key = (r["tx"], r["log_index"])
        if key in seen:
            raise ValueError("Duplicate token transfer")
        seen.add(key)
        if r["token"] not in (USDC, ATOKEN):
            raise ValueError("Unverified token contract")
        verify_log(r, receipts[r["tx"]])
        value = signed(r["raw_value"], r["from"], r["to"])
        if r["token"] == USDC:
            if ATOKEN in (r["from"], r["to"]):
                internal_usdc += value
            else:
                external_usdc += value
                if value:
                    external_usdc_usd += D(value) / 10**6 * price(r["block"], "USDC")
        elif ZERO not in (r["from"], r["to"]):
            external_atoken += value
            if value:
                external_atoken_usd += D(value) / 10**6 * price(r["block"], "USDC")
    usdc_residual = int(end["USDC"]) - int(begin["USDC"]) - internal_usdc - external_usdc
    if usdc_residual:
        raise ValueError("Underlying USDC cash movements do not reconcile")
    gas_wei, gas_usd, eth_flows, eth_flows_usd = 0, D(0), 0, D(0)
    sender_count = 0
    for r in normal:
        receipt = receipts[r["tx"]]
        if (receipt["from"].lower() != r["from"] or
                int(receipt["blockNumber"], 16) != r["block"]):
            raise ValueError("Normal transaction identity mismatch")
        fee = receipt_fee(receipt)
        if fee != int(r["explorer_fee_wei"]):
            raise ValueError("Explorer and receipt paid gas differ")
        if r["from"] == ACTOR:
            gas_wei += fee
            gas_usd += D(fee) / 10**18 * price(r["block"], "ETH")
            sender_count += 1
        if receipt["status"] == "0x1":
            value = signed(r["wei_value"], r["from"], r["to"])
            eth_flows += value
            if value:
                eth_flows_usd += D(value) / 10**18 * price(r["block"], "ETH")
    for r in data["internal_transactions"]:
        if r["success"]:
            value = signed(r["wei_value"], r["from"], r["to"])
            eth_flows += value
            if value:
                eth_flows_usd += D(value) / 10**18 * price(r["block"], "ETH")
    eth_residual = int(end["ETH"]) - int(begin["ETH"]) - eth_flows + gas_wei
    if eth_residual:
        raise ValueError("Native ETH movements and paid gas do not reconcile")
    unit_interest = (int(end["aUSDC"]) - int(begin["aUSDC"]) + internal_usdc - external_atoken)
    # Partial withdrawals are not falsely declared full exits. Only zero-inventory
    # observations close a cash-flow segment. Opening units are a window mark,
    # not the actor's unknown lifetime tax/cost basis.
    flows = [r for r in transfers if r["token"] == USDC and ATOKEN in (r["from"], r["to"])]
    realized_units, unrealized, cycle_rows = partition_interest(
        begin["aUSDC"], end["aUSDC"], flows, data["a_token_balance_after_withdraw_block"])
    if external_atoken or realized_units + unrealized != unit_interest:
        raise ValueError("Cash-interest decomposition requires additional position flows")
    usd_equity = {}
    for tag, endpoint in (("opening", begin), ("closing", end)):
        units = D(int(endpoint["USDC"]) + int(endpoint["aUSDC"])) / 10**6
        usd_equity[tag] = {
            "USDC_and_aUSDC": units * D(endpoint["USDC_price"]) / 10**8,
            "native_ETH": D(endpoint["ETH"]) / 10**18 * D(endpoint["ETH_price"]) / 10**8,
            "recorded_Aave_debt_base_usd": D(endpoint["aave_account_base_8_decimals"][1]) / 10**8,
        }
    if any(v["recorded_Aave_debt_base_usd"] != 0 for v in usd_equity.values()):
        raise ValueError("Additional nonzero Aave liabilities need asset-level reconstruction")
    usdc_marked = (usd_equity["closing"]["USDC_and_aUSDC"] - usd_equity["opening"]["USDC_and_aUSDC"]
                   - external_usdc_usd - external_atoken_usd)
    native_marked = usd_equity["closing"]["native_ETH"] - usd_equity["opening"]["native_ETH"] - eth_flows_usd
    total_marked = usdc_marked + native_marked
    return {
        "status": "OBSERVED_ADDRESS_COMPONENTS_RECONCILED_NOT_FULL_ACTOR_OR_T1",
        "evidence_label": "Observed partial one-address ledger; nonqualifying for T1, not T2/T3",
        "actor": ACTOR, "start": begin["header"], "end": end["header"],
        "elapsed_days": str(D(str(data["elapsed_seconds"])) / 86400),
        "scope": data["scope"], "price_basis": data["price_basis"],
        "usd_equity_components": {k: {a: str(v) for a, v in m.items()} for k, m in usd_equity.items()},
        "transfers": {"verified_token_logs": len(transfers), "receipt_checked_logs": len(seen),
                      "normal_transactions": len(normal), "sender_transactions_with_paid_gas": sender_count,
                      "internal_transactions": len(data["internal_transactions"]),
                      "USDC_external_net_units": str(D(external_usdc) / 10**6),
                      "USDC_external_net_reference_usd": str(external_usdc_usd),
                      "native_ETH_external_net_units": str(D(eth_flows) / 10**18)},
        "reconciliation": {"USDC_raw_cash_residual": usdc_residual, "ETH_wei_residual": eth_residual,
                           "Aave_collateral_base_price_residuals": collateral_residuals,
                           "scaled_index_balances_match": True,
                           "post_opening_USDC_interest_units": str(D(unit_interest) / 10**6),
                           "closed_segment_post_opening_cash_interest_units": str(D(realized_units) / 10**6),
                           "unclosed_segment_closing_accrual_units": str(D(unrealized) / 10**6),
                           "withdrawal_cycles": cycle_rows},
        "observed_network_fees": {"paid_wei": str(gas_wei), "paid_ETH": str(D(gas_wei) / 10**18),
                                  "reference_usd_at_transaction_blocks": str(gas_usd),
                                  "warning": "Sender-only paid gas; already included through native balance changes; do not subtract twice"},
        "marked_components_usd": {"USDC_including_price_changes_before_network_fee_allocation": str(usdc_marked),
                                  "USDC_after_observed_network_fee_allocation": str(usdc_marked - gas_usd),
                                  "native_ETH_including_price_changes_and_network_fees": str(native_marked),
                                  "selected_wallet_components_after_observed_network_fees": str(total_marked)},
        "unknown_costs_and_liabilities": {"infrastructure": None, "custody": None, "tax": None,
                                        "other_protocol_debt": None, "off_address_assets_liabilities": None},
        "full_actor_net_pnl_usd": None, "T1_qualified": False,
        "limits": data["limits"] + [
            "Oracle-defined accounting marks are not realized USD prices or executable bids",
            "Post-opening realized cash interest is in USDC units, not full realized USD net income",
            "No scaling this large holder's dollars into a $50k strategy recommendation",
            "No p99, annual tail probability, fork replay or qualifying paper evidence"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("strategies/benchmark-lending/evidence/actor-observations.json"))
    parser.add_argument("--out", type=Path, default=Path("strategies/benchmark-lending/evidence/actor-reconciliation.json"))
    args = parser.parse_args()
    result = reconcile(json.loads(args.input.read_text()))
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "elapsed_days", "observed_network_fees", "marked_components_usd", "T1_qualified")}, indent=2))


if __name__ == "__main__":
    main()
