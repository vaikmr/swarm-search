# Keeper/automation bounties — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; accessible work, payout and cost evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). No strategy verdict or performance evidence is supplied.

## Candidate-specific failure paths

- A public keeper interface is not proof of accessible paid work. Whitelisting, bonds, operator admission, pending jobs, bounty changes and incumbent competition may leave a newcomer with costs but no revenue.
- An atomic task with bounded gas can have little deployed principal, but any bond, prefund, collateral or long-lived execution balance introduces a separate failure domain.
- Automation depends on timely data and execution. Outages can remove all revenue and delay collateral recovery; a protective protocol pause may also disable the task ([Arbitrum S03](https://status.arbitrum.io/clq6te1l142387b8n5bmllk9es), [Aave S07](https://governance.aave.com/t/aave-v2-v3-security-incident-04-11-2023/15335/37)).

## Required tests and mitigations

Measure genuine eligible tasks and paid rewards, not advertised rates or contract event counts. Charge rejected/racing attempts, server/RPC costs and gas shocks. Remove captured tasks under larger-competitor entry, stop rewards and change admission/bond rules. Stress depeg of any treasury/reward asset, bridge-backed prefunds, stale oracle signals, chain halt and CEX freeze if used.

Bound expenditure and contract balances; skip negative-margin work. The rest of the portfolio must retain the risk-adjusted lending/reserve treatment rather than pretending all capital earns keeper returns.

**Reassessment inputs:** live access rules, reproducible task/payout attribution, bonds and prefunding, attempt logs and whole-portfolio accounting. Low capital use does not establish the requested monthly income; probabilities and tail bounds remain unavailable.
