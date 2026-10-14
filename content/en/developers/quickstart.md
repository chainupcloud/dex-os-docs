# Quick start

Use public read endpoints to confirm the environment, markets and precision before adding signed trading. These requests need no private key and do not create orders or move funds.

## Set the API address

Obtain the HTTPS API base URL for your environment from the operator and set `DEXOS_API_URL`, without a trailing `/`. This page does not assume a testnet or mainnet hostname. Balances, signing domains and markets can differ between environments. The examples require Bash and curl.

```bash
: "${DEXOS_API_URL:?Set the API base URL for your environment}"
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/time"
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/exchange"
```

`/v1/time` returns `serverTime` in Unix milliseconds. `/v1/exchange` returns the signing `chainId` and `domain`, deposit system address, token table, version and numeric conventions. Read these values separately for each environment; do not hard-code a signing domain or contract address from an example.

## Discover markets

```bash
curl --fail-with-body --silent --show-error "$DEXOS_API_URL/v1/markets"
```

Choose a `symbol` from the response, then run:

```bash
: "${DEXOS_SYMBOL:?Set a symbol from the market list}"
curl --fail-with-body --silent --show-error \
  "$DEXOS_API_URL/v1/markets/$DEXOS_SYMBOL"
curl --fail-with-body --silent --show-error \
  "$DEXOS_API_URL/v1/markets/$DEXOS_SYMBOL/book"
```

Record `priceDecimals`, `sizeDecimals`, `tickSize`, `lotSize`, `signingMarketId` and market status. Business requests use `symbol`; `signingMarketId` supplies the numeric market field in signed structs. Handle prices, sizes and amounts as decimal strings without converting through floating point.

## Read your account

Registered accounts can use public read endpoints for balances and the next order nonce. Set your main wallet address; these queries do not require a wallet connection.

```bash
: "${DEXOS_ADDRESS:?Set your main wallet address}"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account" \
  --data-urlencode "address=$DEXOS_ADDRESS"
curl --fail-with-body --silent --show-error --get \
  "$DEXOS_API_URL/v1/account/nonce" \
  --data-urlencode "address=$DEXOS_ADDRESS"
```

A missing account can return 404; this does not mean the API is offline. Add `subaccount` for a subaccount; `0` denotes the main account. To read a vault account, use `vault` instead of `address` and `subaccount`; these selectors are mutually exclusive.

## Add trading next

Read [Signing and authorization](authentication.md), implement the endpoint's EIP-712 signature, and verify the complete flow in a test environment: fetch nonce → sign → submit → inspect business receipt → query orders or fills. This page provides no unverified signing implementation or executable fund-moving request.

HTTP 200 does not always mean an order filled. Inspect every item in a batch response. HTTP 202 means the result is not yet available: query its `requestId` instead of blindly resending. See [REST API conventions](rest-api.md) for receipts, pagination and errors.
