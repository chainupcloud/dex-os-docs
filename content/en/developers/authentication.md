# Signing and authorization

Public reads require no API key. Writes authenticate through EIP-712 signatures. Use private keys only for local signing; never send them as gateway request fields.

## Inputs for signing

Read the environment's `domain`, `chainId` and token table from `/v1/exchange`, market precision and `signingMarketId` from `/v1/markets/{symbol}`, and `nonce` and `signingAccountId` from `/v1/account/nonce`. Each write operation identifies its signed struct in OpenAPI `x-eip712.typeString`. Business JSON is not the EIP-712 message; do not hash and sign the request JSON directly.

Signed prices and sizes are integers: `ticks = price × 10^priceDecimals`, `lots = size × 10^sizeDecimals`. Conversion must be exact and satisfy market tick, lot and business constraints. Scale token amounts using that token's decimals. USDC uses 6 decimals; other assets must not automatically use the USDC scale.

## Main wallet signatures

The shared request envelope contains `account`, `nonce` and `signature`, plus `subaccount`, `vault`, `signer`, `expiresAt` and `nowMs` where applicable. `account` is the main wallet address; `subaccount` selects a subaccount. Do not put `signingAccountId` in an address field.

Omitting `signer` selects main wallet signing. `expiresAt` applies only where the signed struct supports it: the current Order `expiry` comes from this field, with 0 or omission meaning no expiry. Do not assume every optional envelope field affects every operation.

The nonce response's `scope` distinguishes account and API wallet nonces. The current implementation uses incrementing nonces; do not build around timestamp-window nonces. Writers sharing a scope must coordinate allocation and submission order, rather than each concurrently fetching the same nonce. If a request's outcome is unknown, inspect its receipt; a new nonce query alone does not prove success.

## API wallets

The main wallet authorizes an API wallet through `POST /v1/account/agents/approve` and revokes it through `/v1/account/agents/revoke`. API wallets can trade, but cannot withdraw, transfer funds or manage grants. Include expiry and revocation in your key management process.

API wallet requests include `signer` and sign `AgentExec(bytes32 commandHash,uint64 nonce)`. `commandHash` hashes the inner command's canonical bytes, not arbitrary JSON. Use a verified encoder compatible with the current service. Commands such as batch placement, replacement and scheduled cancellation involve `nowMs`; check each endpoint's required fields and hash inputs.

Query an API wallet nonce:

```bash
: "${DEXOS_API_URL:?Set the API base URL}"
: "${DEXOS_ADDRESS:?Set the represented account main wallet address}"
: "${DEXOS_SIGNER:?Set the API wallet address}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/nonce" \
  --data-urlencode "address=$DEXOS_ADDRESS" \
  --data-urlencode "signer=$DEXOS_SIGNER"
```

This nonce belongs to the API wallet scope; do not substitute the main wallet account nonce. Immediately after approval, include `x-dexos-min-seq` on the first write, using the approval receipt's `seq`, so the gateway can observe the grant.

## Trading as a vault

Use the `vault` query parameter to read a vault account. A write on behalf of a vault includes both `vault` and the manager's main wallet `account`, and excludes `subaccount`. Main wallet signing uses the vault account's own nonce and `signingAccountId`. An API wallet must be approved on the account used by the manager to claim the vault.

Vault identity supports placement, cancellation, replacement, cancel-all, schedule-cancel and leverage changes. Other operations are rejected. Vault deposits and redemptions use their respective `/v1/vaults/*` endpoints and participant signatures, rather than the vault trading identity.

## Investigating signature failures

Check the environment and domain first, followed by account identity, nonce scope, integer scaling, field order and types, and the API wallet command hash. `GatewayBadSignature` means pre-check failed; `UnknownAgent` and `AgentExpired` indicate grant problems. Repeatedly changing the nonce does not fix the underlying issue.
