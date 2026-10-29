# Genuine-fork prerequisites: bounded access probe

**Status: archive-access prerequisite investigation only. No fork started, no EVM execution performed, no strategy replay, and no T1/T2/T3 performance evidence.**

## Latest result: separately authorized eight-read dRPC follow-up

On **2026-10-29 from 07:37:02.457621 to 07:37:03.133089 UTC**, a separately authorized **eight-read** probe of credential-free `https://eth.drpc.org` succeeded. The first 12-read PublicNode result below is preserved separately and was not overwritten or retried.

Executable: [`replay_drpc_probe.py`](replay_drpc_probe.py). Recorded artifact: [`replay_drpc_archive_probe.json`](replay_drpc_archive_probe.json).

```text
SHA256 1a4022e4cd26cdd74f5f587f0982613b363f7e120c7bb24220582770c703512d
```

| Read | Exact capability | Actual result |
| --- | --- | --- |
| 1 | `eth_chainId` | Ethereum mainnet `0x1` |
| 2 | Start header, block `26080884` | `2026-09-29T04:58:47Z`, hash `0xc27eb6a8592b703fed5180626e29db037f217eff4f11f4a188687cece69ed244` |
| 3 | Pinned end header, block `26296884` | `2026-10-29T07:24:59Z`, number/hash matched prior identity evidence |
| 4 | Pool proxy code at start | Nonempty bytecode returned |
| 5, 6 | Implementation slot at start and end | Both independently returned `0x728a138a4823392c2efa55e028d434f526fe03cf` |
| 7, 8 | aToken `balanceOf` the public actor candidate at start and end | Two valid 32-byte results, not a PnL calculation |

All eight responses were HTTP 200 without RPC errors. The actual timestamp difference is **2,600,772 seconds**, or **30.10152777777777777777777778 days**; this was checked from returned timestamps, not assumed from a block-count subtraction. The start timestamp and hash were independently matched against the [start-block explorer page](https://etherscan.io/block/26080884) after the run. Both source headers are now pinned for reproduction.

The public actor candidate was `0x56957E411Ea83a0B4A0689C1fB0D1e5eA0d20149`, also used in the independent historical-state lead. These `balanceOf` views do not reconcile deposits, withdrawals, rewards, liabilities, inventory prices or costs. **They establish neither realized PnL nor profitability.**

The follow-up preserved response body text plus parsed values and verified all eight body SHA256 hashes offline. Neither run involved a real key, signer, credential, transaction, payment, tool installation or local EVM. No additional calls were made after the second budget was exhausted.

**Conclusion:** sampled remote code/storage/view access at endpoints at least 30 days apart is available through dRPC. This is a viable upstream candidate for the next local-fork smoke test, not proof that all lazy dependencies or intervening states are available. The local EVM runtime is still missing, historical implementation code/ABI/audit equivalence remains unverified, and **no fork was started**.

The eight-read follow-up can be reproduced only under a new authorized budget:

```sh
python3 -m research_tools.replay_drpc_probe \
  --run-eight-read-probe --output /tmp/drpc-archive-prerequisites.json
```

## First run: 12-read PublicNode execution

The read-only collector ran on **2026-10-29 from 07:34:05.707386 to 07:34:07.080653 UTC**, attempting exactly **12 JSON-RPC reads**, with no retries, wallet, signer, state-changing calls, paid provider, credential, or package installation.

Executable collector: [`replay_rpc_probe.py`](replay_rpc_probe.py).

Recorded artifact: [`replay_archive_probe.json`](replay_archive_probe.json).

Artifact SHA256:

```text
15f15337cb23a945d75b6adc749a46579a42f87363f4b20800bbd14a2153f613
```

This artifact preserves request objects, parsed JSON response values, HTTP statuses, response hashes and observation timestamps. Original whitespace/wire-text bytes were **not retained in this first run**; hashes alone cannot reconstruct them. The collector now additionally retains response text for any separately authorized future run. The published run was not repeated after that preservation improvement, and no additional RPC budget was spent.

## Source-verified identity

The official Aave address registry pinned at commit `73676d409a24eb33d04687f28287f23a40f2afd9` identifies:

| Role | Ethereum mainnet address |
| --- | --- |
| Pool proxy | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| USDC underlying | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDC aToken | `0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c` |

The collector re-fetched this [pinned official registry](https://raw.githubusercontent.com/aave-dao/aave-address-book/73676d409a24eb33d04687f28287f23a40f2afd9/src/AaveV3Ethereum.sol) and checked all three addresses. Full source-response SHA256 was `afe8adbbf8fe7d709ae1d2168b8d97ccb8110fdedb572fc2120ecae10ae7588b`; selected source lines are recorded in the artifact.

**This registry snapshot is not proof of the implementation/configuration at an older block.** Historical implementation, ABI/bytecode equivalence, reserve/oracle configuration, and historical eligibility require their own dated evidence. The older implementation slot was inaccessible in this probe and remains unknown.

Two dated blocks were queried at the [anonymous PublicNode endpoint](https://ethereum.publicnode.com):

| Block | UTC timestamp | Hash verification |
| --- | --- | --- |
| `21000000` / `0x1406f40` | `2024-10-19T13:45:47Z` | Returned header hash `0xf5e1d15a3e380006bd271e73c8eeed75fafc3ae6942b16f63c21361079bba709`; timestamp independently matches the [block explorer](https://etherscan.io/block/21000000) |
| `26296884` / `0x1914234` | `2026-10-29T07:24:59Z` | Returned hash `0x534506ea07ed9fef6d016fb370ea548ff8554e3f33241f481e0ec84de4c08f30` matches the [previous public identity artifact](https://github.com/vaikmr/swarm-search/blob/18370d81039303e86263dc998c87164d8d75226e/strategies/benchmark-lending/evidence/aave-usdc-deployment-identity.json) |

The recent read is **fixed dated state**, not an unpinned `latest` query. Neither block header demonstrates intervening historical-state coverage or a strategy holding period.

## Exact capability outcomes

| Request IDs | Capability | Actual result |
| --- | --- | --- |
| 1 | Ethereum chain identity | `eth_chainId` returned `0x1` |
| 2, 3 | Old and recent block metadata | Both headers returned and passed number/timestamp/hash checks described above |
| 4, 11 | Old pool/aToken code | HTTP 403, JSON-RPC `-32602`, archive token required |
| 5 | Old pool EIP-1967 implementation storage | Same archive token gate |
| 6, 7, 9 | Old ERC-20 `totalSupply`, `balanceOf`, `decimals` calls | Same archive token gate |
| 8 | Recent fixed-block USDC `balanceOf(aToken)` | 32-byte result returned; not PnL, exit capacity or return evidence |
| 10 | Receipt for the first transaction hash listed in old block | HTTP 200 with `result: null`; **no receipt recovered** |
| 12 | Recent fixed-block pool implementation storage | 32-byte result, containing `0x728a138a4823392c2efa55e028d434f526fe03cf`; matches recent identity, not old implementation proof |

The provider's actual old-state error was:

```text
Archive requests require a personal token. Get one at: https://www.allnodes.com/publicnode
```

The [provider page](https://ethereum.publicnode.com) advertises archive access, but this credential-free endpoint did not grant the tested old state reads. We did not request a token, use a private account, pay, retry, or attempt to bypass the gate.

**Receipt/header retrieval and account-state retrieval are separate capabilities.** A block header succeeding cannot be called historical-fork access. Here, historical receipt recovery also remained unestablished for the one tested transaction. A null receipt does not prove all receipts are unavailable.

The old-state denial is **provider-specific**, not proof that every public endpoint is blocked. A separate worker reported credential-free historical `eth_call` and implementation-storage success through `https://eth.drpc.org` at block `26196084` (`2026-10-15T06:20:59Z`). That was not independently re-tested during the first run. The separately authorized follow-up above subsequently confirmed different start/end samples spanning more than 30 days; neither probe establishes access to every historical state or a local fork.

## Local runtime findings

`python3` and `curl` were available. No `anvil`, `cast`, `forge`, `revm`, `geth`, `reth`, Node.js or Docker executable was found. Python package discovery also found no `Crypto`, `eth_utils`, `web3` or `requests`.

Availability here means an executable search on `PATH` and Python module discovery, not an exhaustive filesystem or Rust-library inventory. No software was installed. An unavailable local EVM command and unavailable old state are distinct prerequisites; installing an EVM tool alone cannot repair a provider's authorization requirement.

## Smallest viable real-fork plan

1. **Retain the now-passing sampled remote prerequisite, without upgrading its scope.** The separate dRPC follow-up verified code, proxy slots and aToken views at dated endpoints more than 30 days apart. The next stage must pin the historical implementation's code/ABI and verify dependencies actually needed by the local view. It cannot assume complete 30-day state availability, audited-build equivalence or all lazy fork reads from these eight samples. If credentials become necessary, stop for a separate human-approved secure setup; an endpoint's token gate does not authorize credential acquisition or spending.
2. **Follow package-management guidance before installing a pinned local EVM runtime.** Prefer official Anvil release assets with recorded version and checksum. Do not pipe an unreviewed remote installer into a shell. Check installed help/version before composing flags. Disable generated accounts (`--accounts 0`, if confirmed by that version), bind loopback, and do not attach a real signer or wallet.
3. **Run a minimal, read-only fork smoke test at the pinned historical block.** Verify the historical proxy's implementation and ABI applicable at that block rather than today's implementation. Execute a public view such as the reserve's normalized-income getter locally and cross-check against the same pinned remote state. Record local EVM version, upstream block hash and fetched dependency/code hashes. No strategy trades, public transactions or local impersonation are needed for this prerequisite.
4. **Do not upgrade that smoke test to T2.** It proves, at most, that the selected runtime can execute a small view call against some historical state. All lazily fetched account/code/storage dependencies for a real path, fees, prices, latency, competing transactions and full cutoff inventory remain unverified.
5. **Only begin a genuine strategy replay after inputs are defensible.** Require historical contract/ABI/configuration identity, complete economic/fee boundaries, measured latency and competitor capture rules, rejected/failed opportunities, and pending-position carryover without later-settlement lookahead. Then the charter still requires at least 30 days including a volatile window, realistic execution/cost/competition, independent review, and separate actual seven-day forward observation before recommendation.

No command to start a fork was run or claimed successful. Both the initial 12-read and separately authorized eight-read budgets are exhausted; this report does not authorize another probe, tool installation, paid access or deployment.

## Reproduction and checks

The following command consumes **up to 12 new reads** and must only be run under a separately authorized budget:

```sh
python3 -m research_tools.replay_rpc_probe \
  --run-read-only-probe --output /tmp/archive-prerequisite-probe.json
```

The explicit CLI flag, fixed credential-free endpoint, RPC allowlist, 12-attempt hard limit, and no-retry behavior are tested offline:

```sh
python3 -m unittest discover -s tests -p 'test_replay_rpc_probe.py' -v
```

Protocol read semantics: [ERC-20](https://eips.ethereum.org/EIPS/eip-20), [EIP-1967 implementation slot](https://eips.ethereum.org/EIPS/eip-1967). Local-fork reference: [official Anvil overview](https://getfoundry.sh/anvil/overview).
