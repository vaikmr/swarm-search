# Actual fourteen-day holder components — reconciled, not certified T1

This package replaces rate-only arithmetic with **actual public account
observations**, while preserving narrower scope than full actor equity or net
profit. No T1/T2/T3 qualification or strategy recommendation is claimed.

The selected address is
[`0x56957E411Ea83a0B4A0689C1fB0D1e5eA0d20149`](https://eth.blockscout.com/address/0x56957E411Ea83a0B4A0689C1fB0D1e5eA0d20149).
Selection was deterministic: the first non-contract holder in the previously
archived first-ten Aave USDC holder sample, **before** computing its return.
This identifies an on-chain address, not its beneficial owner, firm, purpose,
external treasury, or complete strategy.

## Exact observed window and scope

| Endpoint | Ethereum block | UTC |
| --- | ---: | --- |
| Opening | 26,196,084 | 2026-10-15 06:20:59 |
| Closing | 26,296,884 | 2026-10-29 07:24:59 |

Actual elapsed time is **14.04444444 days**, not an assumed blocks-per-day
conversion. Requested block numbers are checked against returned headers.
Hashes and timestamps are preserved.

The scope is **one address's verified USDC, Aave V3 USDC aToken, native ETH,
and Aave V3 endpoint collateral/debt data**. It excludes other assets, NFTs,
protocols, chains and off-address accounts/liabilities. The exact verified token
contracts, not symbols or token display names, control inclusion.

| Observed balance | Opening | Closing |
| --- | ---: | ---: |
| USDC | 0 | 0.000200 |
| aUSDC, underlying USDC units | 133,902,645.238106 | 134,089,443.615618 |
| Native ETH | 0.667480702784307378 | 0.667146602333009682 |
| Aave V3 reported debt, base USD | 0 | 0 |

At both endpoints, Aave's reported total collateral matches this aUSDC position
at the queried USDC oracle mark, with zero base-unit residual. This does **not**
establish absence of other protocols' or the owner's off-address liabilities.

## Flows, token index and expenses

The bounded explorer crawl crossed the opening boundary for each selected
token, normal transactions and internal transactions. It returned:

- **100 USDC plus 26 aUSDC transfer logs**, each matched to the exact token,
  sender, receiver, value, block and log index in actual RPC receipts.
- **102 transaction receipts** covering every selected transfer and normal
  transaction, including zero-value USDC transfers.
- **41 normal transactions**: 39 address-sent transactions with paid gas and
  two incoming transactions whose gas was not charged to this address.
- **No internal ETH transfers** in the window according to the paginated
  explorer response.
- **85 historical price reads** at external flow and paid-expense blocks.

The generic unfiltered token page contained untrusted lookalike display names.
Those records were not valued or counted as genuine USDC. Genuine zero-value
USDC logs were retained with zero financial effect.

External net USDC movement was **−7,664.757399 USDC**, not profit. The large
transfers to/from a recurring counterparty are treated as external capital
flows, with **no assumption of common ownership**. Transfers between the
address and its Aave position are internal asset movements, not fresh capital.
A tiny incoming **0.00000003 ETH** is likewise a capital flow.

Both raw USDC cash and native ETH balance equations reconcile **exactly**:

```text
USDC_close - USDC_open - internal_position_flows - external_USDC_flows = 0 raw units
ETH_close - ETH_open - external_ETH_flows + sender_paid_gas = 0 wei
```

Scaled aToken units times the actual normalized liquidity index also reproduce
both observed aUSDC balances exactly. An initial legacy half-up calculation
failed by one micro-USDC at each endpoint. Verified deployed `TokenMath`
source and endpoint implementation-slot reads showed that this aToken uses
**rayMulFloor**, not half-up multiplication; the correction is source-backed,
not a tolerance chosen to force a match.

Actual interest attributable to the observed position **in USDC units**:

| Component | USDC units |
| --- | ---: |
| Total post-opening accrual from position balances and cash movements | 194,463.135111 |
| Cash-interest component of segments ending with verified zero inventory | 173,998.001186 |
| Closing accrual in the remaining unclosed segment | 20,465.133925 |

There were **13 withdrawals but only four zero-inventory segment endings**.
Other withdrawals left observed residual positions; they were not falsely
treated as full exits. Segment accounting uses the opening marked token units
as the first window basis, **not** the unknown lifetime or tax cost basis.
These unit amounts are not full realized USD net income.

Receipts show **0.000334130451297696 ETH** paid by the address in network fees,
or **$0.799763428905** using the historical ETH oracle mark at each paid
transaction's block. Explorer paid-fee values equal receipt
`gasUsed * effectiveGasPrice`; incoming senders' fees are excluded. Network fees
are already reflected in the native balance equation and are not subtracted
again from the total wallet-component calculation.

## Actual price sources and limited marked result

The recorded Aave oracle is
`0x54586bE62E3c3580375aE3723C145253060Ca0C2`.
Both endpoints return zero-address `BASE_CURRENCY` (the documented USD
convention) and `BASE_CURRENCY_UNIT = 100000000`. Provider `getPriceOracle`
also identifies that oracle at both endpoints. The same oracle contract's
historical `getAssetPrice` values mark each external flow and expense.

| Reference oracle mark | Opening USD | Closing USD |
| --- | ---: | ---: |
| USDC | 0.99987936 | 0.99972447 |
| ETH, through WETH asset price | 2,351.63 | 2,309.84088059 |

No fixed $1 USDC price was substituted. These are **oracle-defined accounting
marks**, not executable spot quotes, OTC prices, cash redemption prices, or
realized USD conversion proceeds. Endpoint identity equality also does not
prove no intervening governance/configuration change.

```text
selected component marked PnL
  = marked closing USDC+aUSDC+ETH
  - marked opening USDC+aUSDC+ETH
  - externally transferred capital, marked at each flow block
```

This yields **$173,641.329360** for the selected components after observed
address-paid network fees, including USDC/ETH mark changes. The USDC component
before network-fee allocation is **$173,669.994582**; native ETH contributes
**−$28.665221**, including its price movement and paid fees.
**Neither figure is full actor net profit.** Unknown infrastructure, custody,
tax and other liabilities remain `null`, not zero. The position is around
$134 million: do not linearly turn its dollars or observed tiny gas bill into
a $50,000 strategy, deployability claim or capacity conclusion.

## Access findings and remaining evidence

- Free PublicNode served recent state and headers, but the fourteen-day
  historical calls/storage returned `-32602`, archive personal-token required.
- `https://eth.llamarpc.com` returned HTTP 525 in the bounded archive probe.
- **Free `https://eth.drpc.org` served the historical views, storage and
  receipts without credentials.** A three-read batch succeeded; an earlier
  eleven-read batch returned HTTP 500. No generalized cause is inferred.
- A dRPC `web3_sha3` request returned HTTP 400; public PublicNode
  `web3_sha3` supplied the exact selectors instead.
- The dRPC log-range probes returned code 35 / free-plan range error,
  including a nominal 10,000-block query. An isolated receipt request worked.
  Explorer pagination plus receipt matching is therefore **not** an
  independently exhaustive RPC `getLogs` enumeration.

Actual failed/successful probe records, exact receipt data, source requests,
response hashes, page boundaries and timestamps are preserved in
[`actor-observations.json`](evidence/actor-observations.json).
The compact file retains only the scoped tokens/address's logs, not large
unrelated transaction datasets. Observation times explicitly use cache-write
timestamps where a separate server/request time was not captured.

The outstanding T1 blockers are complete asset/liability and cost scope, actual
owner/strategy attribution, realized-versus-marked USD treatment, and independent
review of indexer completeness and accounting. Full actor net PnL and the
qualification flag remain **`null` and `false`**. This is real public evidence
with specific limitations, not a simulated successful trader.

## Reproduce

```sh
python3 strategies/benchmark-lending/sim/collect_actor_ledger.py
python3 strategies/benchmark-lending/sim/reconcile_actor_ledger.py
python3 -m unittest discover -s strategies/benchmark-lending/sim -v
```

The collector bounds pagination to five pages per stream, live RPC reads to
350 per invocation, uses batches of three with pacing, and allows only specified
read methods. The offline reconciler and tests need no network. Captured
prerequisite failures are optional cache inputs; a fresh run does not invent
past failures. See
[`actor-reconciliation.json`](evidence/actor-reconciliation.json) for exact
Decimal arithmetic, all 13 withdrawal observations and four closed segments.
