# API Reference

Both languages use the same public v1 OpenAPI specification. Protocol fields remain in English; the guides explain integration workflows.

Read the developer guides for decimal scaling, signing, and receipt handling. Account channels do not imply confidential access.

Interactive requests require the actual gateway URL. The server host in this specification is the placeholder `api.dexos.invalid` until a public gateway address is published. Signed writes require a client-generated signature and are submitted through `POST /v1/commands`.

[OpenAPI YAML](https://raw.githubusercontent.com/chainupcloud/dex-os-docs/0a6ea36b0c0d5b96aad163dc1e879c273500a8fb/api/openapi-v1.yaml)

- [Exchange](exchange.md)
- [Market data](market-data.md)
- [Account](account.md)
- [Vaults](vaults.md)
- [Subscriptions](subscriptions.md)
- [Funds](funds.md)
- [Security](security.md)
