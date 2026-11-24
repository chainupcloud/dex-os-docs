# Commands overview

Every ledger change is a signed command submitted to [`POST /v1/commands`](../trading.md) as `{"command":"0x…"}`. These pages list the commands that endpoint accepts, who signs each one and which nonce lane it uses. For how to sign, see [Authentication](../../developers/authentication.md).

Every command on the following pages has a JSON example of its fields and a **Try it** link to the [API playground](https://dex-preview.unibook.site/app/api-playground/), which signs and submits it on the preview network with a throwaway key and test funds. [Orders](orders.md) walks through placing an order end to end.

## Accepted commands

| Command | Use |
|---|---|
| `AuthenticatedCommand` | One action signed by its principal. It carries one command from the groups below; almost every write uses it |
| `RegisterAccount` | Creates the account (signing policy and exit address) for an address |

Other command kinds are submitted only by platform services, such as certified ledger time, oracle rounds and custody-chain event reports. Anything else returns 400 `unsupported_command`.

## Commands inside `AuthenticatedCommand`

| Group | Signed by | Nonce lane | Details |
|---|---|---|---|
| Trading | account or API wallet | `trade` | [Orders](orders.md) |
| Margin | account | `trade` | [Margin, funds and vaults](account-funds.md) |
| Funds | account | `funds` | [Margin, funds and vaults](account-funds.md) |
| Vaults | account | `funds` | [Margin, funds and vaults](account-funds.md) |
| Account settings | account | `management` | [Margin, funds and vaults](account-funds.md) |
| API wallets | account (main wallet) | `management` | [API wallets](governance.md) |

- "Account" means the members of the account's signing policy (the main wallet), signing up to the policy threshold.
- An API wallet signs only within its grant. Operations, accounts or markets outside the grant, and groups an API wallet cannot sign, are rejected with `CapabilityDenied`.
- Each principal has its own nonce window per lane; see [Authentication](../../developers/authentication.md).

## Building a command

- Build and sign with the public Go SDK [dex-sdk-go](https://github.com/chainupcloud/dex-sdk-go); do not hand-write the binary encoding. Trading commands have an `Encode<Command>` function in the `dexos` package; the `dexosv1` package handles signing, nonces and submission.
- Prices, sizes and amounts inside a command are scaled integers; markets use `signingMarketId` and accounts use `signingAccountId`. See [Authentication](../../developers/authentication.md).
- After submitting, poll `GET /v1/requests/{requestId}` until the status is `Executed` or `AuthorizationRejected`.

These pages follow the gateway and ledger code on the dex-os `main` branch.
