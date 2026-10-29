# Keeper and automation bounties

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.

## Hypothesis

Open, funded maintenance jobs might provide small residual service revenue without
large inventory risk. This is labor/competition-limited income; protocol usage
does not automatically create permissionless work or surplus beyond gas.

## Discovery facts

[Keep3r keeper documentation](https://docs.keep3r.network/core/keepers) permits
registration without a minimum bond for the basic role, but individual jobs can
require bonded funds, age or earnings history. The documented default bond delay
is **3 days** and unbond delay **14 days**; these are documentary defaults, not
verified current contract settings or observation durations.
[Jobs documentation](https://docs.keep3r.network/core/jobs) describes payment and
filtered access. Gross payment must be separated from gas reimbursement and
reward-token inventory risk.

[The official registry](https://docs.keep3r.network/registry) lists
`0xeb02addCfD8B773A5FFA6B9d1FE99c566f8c44CC` explicitly under **Beta Addresses**.
It is a historical registry lead, **not** a verified current production deployment
or profitable keeper. Job-registry lead: https://github.com/keep3r-network/job-registry/ .

[Chainlink Automation architecture](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
describes registry-compensated nodes using OCR consensus. It does not establish
that an unaffiliated new operator can join the currently authorized network or
win public bounties. Do not treat registering an upkeep as registering a paid node.

## Next gate

Find current audited eligible deployments and funded jobs, enumerate actual paid
keepers and recent active jobs, verify admission, reconcile work/reward events to
receipts and failures, and mark reward tokens at liquidation value. No current
paid keeper actor, available job capacity or qualifying actor PnL has yet been
verified. If a viable contract/job universe cannot be established, keep this
unverified rather than fabricating a monthly income estimate.
