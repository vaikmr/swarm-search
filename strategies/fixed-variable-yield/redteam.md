# Fixed/variable yield trades — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; underlying claims, maturity and financed-exit evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). No verdict, forecast rate or realized-return evidence is supplied.

## Candidate-specific failure paths

- A tokenized fixed-yield claim can depend on the yield-tokenization protocol, its underlying issuer/lending protocol, an oracle, bridge representation and collateral manager. Different token names do not prove independent failure domains.
- Holding to maturity and marking a redeemable claim today are different risks. A fixed nominal payoff in an impaired underlying unit is not guaranteed fixed USD value. Market-rate changes can produce intramonth mark-to-market losses even if nominal maturity redemption later succeeds.
- A floating-rate borrowing leg can reprice, suffer collateral haircut, become unavailable or be liquidated while the purportedly fixed leg remains locked. Historical lending pauses show why uninterrupted repayment/exit access cannot be assumed ([S07](https://governance.aave.com/t/aave-v2-v3-security-incident-04-11-2023/15335/37)).

## Required tests and mitigations

Pin maturity, redemption mechanics, underlying representation, executable depth, fees and borrow terms. Stress underlying depeg, delayed/failed redemption, stale oracles, adverse rate/cap changes, gas spikes, halt, bridge delay and larger competitor/capital inflow. Deny CEX/bridge-funded collateral rescue if present.

Budget exit liquidity instead of valuing every token at nominal maturity payout. Count look-through issuer/protocol exposure and match financed obligations to accessible reserves. Only charter-permitted delta-neutral leverage may be considered.

**Reassessment inputs:** exact deployed series, maturity cashflows, redemption evidence, borrow/hedge terms, depth and state-based stress output. No tail frequency or monthly drawdown certification is available.
