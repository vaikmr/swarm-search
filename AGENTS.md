# Research rules

## Safety and scope

- Research only: local historical replays and read-only forward paper observation.
- Never hold or request private keys, sign or broadcast transactions, deploy to mainnet, or place live trades.
- No sandwiching, front-running users, contract exploitation, oracle/market manipulation, wash trading, phishing, bait tokens, or governance attacks.
- Do not search for or reproduce vulnerabilities. If one is incidentally noticed, stop that path and report minimal safe details privately; do not publish exploitation details.
- Public sources and authorized research data only. No unrelated employer/customer data, credentials, private correspondence, internal identifiers, or coordination metadata.
- No paid data, RPC, hosting, or other purchases without explicit approval. The infrastructure ceiling is not authorization to spend.

## Evidence integrity

- Every numeric performance, cost, or probability claim must include its source or reproducible calculation, timestamp/window, units, and evidence label.
- Input constraints and exact arithmetic derived from them must be distinguished from observed performance.
- Missing evidence means unverified. A failed search does not prove no profitable actor exists.
- Advertised rates and gross inflows are not realized net PnL.
- Label synthetic data and test fixtures; never present them as market observations.
- Preserve failed runs, rejected fills, missing data, and limitations. No lookahead, cherry-picking, or optimistic tie fills.
- Enforce the charter's separate monthly confidence and annual tail-scenario gates. A p5 statistic is not a 99% risk certificate.
- No recommendation without actual qualifying T2 and T3 evidence and independent review.

## Collaboration

- Follow [workstream ownership](docs/WORKSTREAMS.md); avoid overlapping edits.
- Use separate branches; do not push changes directly to `main`.
- No worker-created PRs unless coordinated. Provide tested commits and file manifests for integration.
- The judge must not originate a strategy's return evidence, simulation, or risk report.
- Only a human can authorize live deployment. A research PR is not such authorization.

## Validation and commits

- Prefer small Python standard-library tools with focused unit tests.
- Run relevant tests and `git diff --check`; document blocked checks truthfully.
- No secrets or generated large market datasets in Git. Record public source URLs and reproducible retrieval instructions.
- Include `Assisted-by: Replit` in every assisted commit.
