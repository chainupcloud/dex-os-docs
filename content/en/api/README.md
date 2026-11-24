# API Reference

Both languages use the same public v1 OpenAPI specification. Protocol fields remain in English; the guides explain integration workflows.

Read the developer guides for decimal scaling, signing, and receipt handling. Account channels do not imply confidential access.

**Test it** sends requests to the preview network `https://dex-preview.unibook.site` (test funds only). Signed writes need a signature made on the client and go through `POST /v1/commands`; to sign and submit one from the browser, use the [API playground](https://dex-preview.unibook.site/app/api-playground/). Each command on the [Trading](trading/commands.md) pages links to it.

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.yaml)

- [Market data](market-data.md)
- [Account](account.md)
- [Vaults](vaults.md)
- [Subscriptions](subscriptions.md)
- [Funds](funds.md)
- [Trading](trading.md)

Advanced API (for SDK authors, multi-signer accounts and self-custody tracking):

- [Ledger accounts and grants](advanced/ledger-accounts.md)
- [Self-custody and withdrawal tracking](advanced/self-custody.md)
- [Event backfill and async results](advanced/backfill.md)
