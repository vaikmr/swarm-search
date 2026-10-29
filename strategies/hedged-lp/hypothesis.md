# Hedged concentrated-liquidity LP — unverified and not advanced

**Stage:** 0/1 breadth screen. **T1/T2/T3:** not established.
No honest numerical net-return estimate is available from the current evidence.

Provide concentrated liquidity, hedge the volatile inventory, and hope that
fees exceed LVR/impermanent loss, hedge funding, rebalance costs, slippage and
infrastructure. A static short does not keep a concentrated position neutral as
price crosses ticks. Neutralizing first-order delta does not remove adverse
selection, gamma, gap risk, out-of-range loss or margin liquidation.

## Public actor/venue leads and eligibility

The timestamped public protocol screen is preserved in
[`protocol-screen.json`](evidence/protocol-screen.json), from
[DefiLlama protocols](https://api.llama.fi/protocols).
It is a venue screen, not a claim that every listed protocol runs a hedged CLLP
strategy.

- GammaSwap's [vault audit lead](https://skynet.certik.com/third-party-audit-reports/jqfm0se0f03r/thirdparty-1d77721231ae438993b045d847a21414-pdf/d9f4e91b54b946903222a79c1badb947/GammaSwap-security-review_2024-12-30.pdf)
  describes delta-neutral Uniswap V3 vault designs. The current public screen
  lists GammaSwap Yield Tokens about $81.9k, Open Interest about $47.2k and Classic
  about $4.5k. All are well below $50M individually; they do not establish an
  ordinary-eligible venue. Audit existence does not prove live profitability.
- Orange Finance is a historical delta-neutral-liquidity lead, but the current
  protocol snapshot reports roughly $89 TVL, far below the ordinary gate.
- Rage Trade v1 reports roughly $6 TVL. Historical marketing for GLP hedging is
  not current contestable concentrated-liquidity evidence.
- Arrakis Modular reports about $56.95M and public audit links. This establishes
  a managed-LP venue lead, **not an identified hedged strategy or reconciled
  profitable actor**. An explicit hedge account/position must be proven.
- Charm Finance V2 reports about $1.53M, below the ordinary gate, and a managed-LP
  label alone likewise does not establish hedging.

Exact values, provider dates and audit-link metadata are in the snapshot.
No actor's fourteen-day capital, fills, transfers, hedge inventory and net profit
has been reconciled. Do not conclude that no profitable hedged LPs exist from
this bounded incomplete search.

## Evidence required to advance

Find a specific deployed LP vault/account and its hedge counterpart; reconstruct
token amounts, tick ranges, LP value, collected/uncollected fees, funding, gas,
rebalances and capital flows at both endpoints. Replay swaps with realistic tick
liquidity and adversarial fills; compare **total dollar equity**, not fee APY, to
the same inventory held outside the LP and to net lending.

Venue failures below the ordinary TVL threshold exclude those particular routes
unless explicitly treated as higher risk. The strategy family is **unverified**
rather than proven unprofitable. Independent red-team and judge files are not
authored or pre-decided by this scout.
