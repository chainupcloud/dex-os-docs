# Signing and authorization

Public reads require no API key. Every signed write is one command submitted to `POST /v1/commands` as `{"command":"0x…"}`, the lower-case hex of the signed command's canonical bytes. The request JSON is not what gets signed, and the gateway does not sign, fill in a nonce or extend validity for you. Use private keys only for local signing; never send them to the gateway.

Build commands with the public Go SDK [dex-sdk-go](https://github.com/chainupcloud/dex-sdk-go) (package `dexosv1`); its `examples/commands` program walks through grant, place, resubmit, cancel, expiry and revoke. Do not hand-roll the binary encoding.

## What a command binds

| Part | Where it comes from |
|---|---|
| Network identity: `networkId`, `genesisHash`, `ledgerEpoch`, chain id, verifying contract, `manifestHash` | The SDK reads it from the gateway of each environment; never hard-code it |
| Signing principal | The account root (a main wallet that is a member of the account's signing policy) or an API wallet acting under a grant |
| Nonce lane and nonce | `trade` for orders and cancels, `funds` for withdrawals, transfers and vault deposits/redemptions, `management` for grants, subaccounts and similar settings |
| Validity | `validUntilMs`, judged against the ledger's certified time, not your local clock |
| Inner command | Canonical encoding of the business action; prices and sizes are scaled integers, markets use `signingMarketId` and accounts use `signingAccountId` |

The signature is EIP-712 over an `AuthorizedAction` struct that covers all of the above. The command's `actionId` is also its `requestId` for receipt lookups.

After a ledger re-genesis the network identity changes. A command signed against the old network is rejected with 503 `upstream_manifest_mismatch`; send `x-dexos-expect-manifest` with the manifest hash you signed against so a mismatch is caught explicitly. Re-read the network identity and sign again.

## Accounts and principals

A wallet's own account is its signing principal. Subaccounts share their main account's policy; `GET /v1/account/subaccounts?address=` returns each subaccount's `signingAccountId`.

## Integer scaling

Signed prices and sizes are integers: `ticks = price × 10^priceDecimals`, `lots = size × 10^sizeDecimals`, with `priceDecimals` and `sizeDecimals` from `/v1/markets/{symbol}`. Conversion must be exact and satisfy the market's tick, lot and business constraints. Scale token amounts by that token's own decimals; do not assume the USDC scale for every asset.

## Nonces

Each principal has a separate nonce window per lane. Read it with `GET /v1/account/nonce?address=…&lane=…` (add `signer=` for an API wallet). The window returns `floor`, the highest used value `high` (null if none) and a suggested `next`: values below `floor` or already used are rejected, and `next` and above have never been used.

Writers that share a principal and lane must coordinate allocation. A rejected or unknown write does not mean you should immediately sign the same action again with a new nonce: resolve the original command first (see [Errors and recovery](errors-and-recovery.md)).

## API wallets

The main wallet issues a grant to an API wallet with a `management`-lane command. A grant names the API wallet, the subaccounts it covers, the actions it may perform and an expiry, and can limit markets and price bands. Revoke it with another `management`-lane command. API wallets cannot use the `funds` lane, so they cannot withdraw, transfer funds or make vault deposits and redemptions.

Wait until the grant is active before the API wallet signs: check `GET /v1/grants?policy=<id>` for the grant's `status` and `epoch`, or `GET /v1/account/agents?address=` and `GET /v1/agents/{address}`, where `executable: true` means the ledger would accept the grant at the current certified time. These listings are an inventory; a command can still be refused for its action, account, market or limits.

An API wallet signs as the agent principal with the grant id and grant epoch, and uses its own nonce windows, separate from the main wallet's.

## Vaults

Read a vault account with the `vault` query parameter. Trading a vault account is done by its manager, as the manager's main wallet or an API wallet granted by it. Vault deposits and redemptions are `funds`-lane commands signed by the depositor's main wallet; API wallets cannot submit them.

## Investigating rejections

Check the environment and network identity first, then the principal and its epoch, the lane and nonce window, validity against certified time, and integer scaling. A command the ledger refuses on authorization shows up in its receipt as `AuthorizationRejected` with a stable error, and its nonce is not consumed. Repeatedly changing the nonce does not fix the underlying issue.
