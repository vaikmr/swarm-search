# Lawful order-flow-auction backrunning

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.

## Hypothesis

A searcher might capture residual lawful backrun margin after user refunds, builder
payments and execution/infrastructure costs. Restrict all research to backruns
permitted by the user-selected order-flow mechanism. No front-running, sandwiches,
private-data acquisition or transaction submission.

## Sources and attribution pitfalls

[Flashbots' public data announcement](https://collective.flashbots.net/t/publishing-flashbots-protect-and-mev-share-data/3087)
points to public datasets and explains backrun-only shared hints. Dataset leads:

- https://flashbots-data.s3.us-east-2.amazonaws.com/index.html
- `dune.flashbots.dataset_mevshare_transactions`
- `dune.flashbots.dataset_protect_transactions`
- https://dune.com/flashbots/flashbots-protect-mevshare

**User refunds are not searcher profits.** Published successful-backrun counts
and user-refund totals are therefore not adopted as T1. A user refund address is
not automatically a searcher identity, and an oracle forwarder address is not
a liquidator.

Chainlink's
[SVR Ethereum onboarding](https://docs.chain.link/data-feeds/svr-feeds/searcher-onboarding-ethereum)
documents another lawful liquidation-backrun auction with multiple bidders and
protocol/network value recapture. This is a competition lead, not a guaranteed
profit opportunity. No feed decoding, bundle signing or submission was implemented.

## Missing evidence / next gate

Identify actual landed backrun executors, count independent competitors, reconcile
token/native transfers, builder payments, user refunds, gas, losing attempts and
capital. Recover exactly the hints available at decision time for replay; full
historical transaction visibility creates lookahead if those details were not
actually shared. No searcher address is currently verified from primary records
in this package. No recommendation follows from availability of the event stream.
