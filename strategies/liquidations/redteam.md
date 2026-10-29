# Legitimate liquidations — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; collateral disposal, competition and oracle-access evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). No oracle manipulation, vulnerability testing or exploit reproduction is permitted.

## Candidate-specific failure paths

- Eligibility at an oracle price does not establish profitable executable collateral disposal. Bonuses can be consumed by slippage, gas, debt accrual and competitors. Sparse markets can contain bad collateral rather than attractive liquidations.
- Pauses and recovery grace periods can remove the opportunity or leave preexisting positions trapped. Aave's historical protective pause is relevant context, not a current-market assertion ([S07](https://governance.aave.com/t/aave-v2-v3-security-incident-04-11-2023/15335/37)).
- Sequencer and oracle outages create uneven execution access; uptime and freshness must be checked without deliberately inducing or exploiting a failure ([S04](https://docs.chain.link/data-feeds/l2-sequencer-feeds)).

## Required tests and mitigations

Replay only legitimate eligibility and ordinary protocol-authorized liquidation paths. Deny unproven races; include failed attempts and timestamp-consistent disposal depth. Test debt/collateral depeg, oracle staleness, restart grace, gas shocks, protocol parameter changes, halt and a larger competitor. Deny CEX/bridge escape routes when those fail.

Use bounded own-capital exposure and require neutral execution where leverage is involved; do not assume an atomic loan is automatically exempt from the user's leverage rule. Avoid warehousing seized collateral without an explicit inventory risk budget. Verify the specific small market still meets eligibility or is labeled higher risk.

**Reassessment inputs:** eligibility/configuration snapshots, public ordinary liquidation event history, eligible collateral, disposal fills, competition and full inventory/gas accounting. No gross liquidation volume is treated as profit; probabilities and monthly tail bounds remain unavailable.
