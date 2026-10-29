# Long-tail DEX arbitrage

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.

## Hypothesis

Legitimate atomic arbitrage around established pools with less incumbent attention
might earn residual margin. Being obscure is not itself an advantage: thin depth,
token transfer restrictions, manipulated prices and inventory risk can dominate.
No vulnerability discovery or testing is part of this study.

## Public lead

The public
[Velocimeter/Graphene Fastlane Base dashboard](https://dune.com/outergod/fastlane-bot-base)
identifies a Bancor arbitrage contract on Base:
[`0x2AE2404cD44c830d278f51f053a08F54b3756e1c`](https://basescan.org/address/0x2AE2404cD44c830d278f51f053a08F54b3756e1c).
This is an execution infrastructure contract, **not** a single profitable actor.
The dashboard describes shared rewards between protocol and callers; that
description is a lead requiring current contract/event verification, not an
assumed operator margin.

Repository lead: https://github.com/bancorprotocol/fastlane-bot .
No third-party bot code was executed. Public repositories advertising profit are
not evidence of successful operation.

## Missing evidence / next gate

Extract reward events by caller, transaction receipts including reverts, all
explicit payments and inventory effects over a qualifying history. Check whether
the protocol is live, audited and satisfies the TVL/age gate today. The pool/token
universe must exclude bait tokens, unsafe unknown contracts and markets whose
only apparent opportunity depends on manipulation. No contestable niche or
newcomer edge has yet been demonstrated. Do not replace that absence with a
claim that no one is profitable.
