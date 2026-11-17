# API Reference

Both languages use the same public v1 OpenAPI specification. Protocol fields remain in English; the guides explain integration workflows.

Read the developer guides for decimal scaling, signing, and receipt handling. Account channels do not imply confidential access.

Interactive requests require the actual gateway URL. The server host in this specification is the placeholder `api.dexos.invalid` until a public gateway address is published. Signed writes require a client-generated signature and are submitted through `POST /v1/commands`.

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml)

- [Exchange](exchange.md)
- [Market data](market-data.md)
- [Account](account.md)
- [Vaults](vaults.md)
- [Subscriptions](subscriptions.md)
- [Trading](trading.md)
- [Funds](funds.md)
- [Security](security.md)
