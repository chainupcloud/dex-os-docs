# API Reference

Both languages use the same public v1 OpenAPI specification. Protocol fields remain in English; the guides explain integration workflows.

Read the developer guides for decimal scaling, signing, and receipt handling. Account channels do not imply confidential access.

**Test it** sends requests to the preview network `https://dex-preview.unibook.site` (test funds only). Signed writes need a signature made on the client and go through `POST /v1/commands`; to sign and submit one from the browser, use the [API playground](https://dex-preview.unibook.site/app/api-playground/). Each command on the [Trading](trading/commands.md) pages links to it.

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/421ecf0450369486ffcd175e3d0de399b1958539/api/openapi-v1.yaml)

- [Market data](market-data.md)
- [Account](account.md)
- [Vaults](vaults.md)
- [Subscriptions](subscriptions.md)
- [Funds](funds.md)
- [Trading](trading.md)
