# Grants, registration and governance

Each example below is the command's JSON form: the fields you choose. The SDK (or the [API playground](https://dex-preview.unibook.site/app/api-playground/)) adds the nonce and validity window, signs it and encodes it; the HTTP request is always `POST /v1/commands` with `{"command":"0x…"}`. The playground runs on the preview network with a throwaway key and test funds: it shows the nonce read, the EIP-712 typed data, the signed command, the response and the receipt, and copies the submission as curl.

## Fields

| Field | Meaning |
|---|---|
| `market` | Market id: `signingMarketId` from `GET /v1/markets` |

64-bit values (order ids, amounts, times) may be written as decimal strings.

## Grants

### GrantCapability

Grant an API wallet: accounts, operations, markets, price band, limits and expiry.

Signed by: account (main wallet); API wallets cannot · nonce lane `management`

`grantId` derives from the issuing policy and `grantSalt`; the SDK (`dexosv1` `ApproveAgent`) and the playground compute it. `actions` lists the allowed operations, `limits.markets` the markets with their spec versions and price band.

```json
{
  "kind": "GrantCapability",
  "expectedIssuerEpoch": 0,
  "grantSpec": {
    "grantId": "0x1111111111111111111111111111111111111111111111111111111111111111",
    "grantSalt": "0x2222222222222222222222222222222222222222222222222222222222222222",
    "grantee": {
      "agent": "0x3c44cdddb6a900fa2b585dd299e03d12fa4293bc"
    },
    "actions": [
      {
        "namespace": 1,
        "id": 5
      },
      {
        "namespace": 1,
        "id": 6
      },
      {
        "namespace": 1,
        "id": 10
      },
      {
        "namespace": 1,
        "id": 15
      },
      {
        "namespace": 1,
        "id": 17
      },
      {
        "namespace": 1,
        "id": 18
      },
      {
        "namespace": 1,
        "id": 19
      },
      {
        "namespace": 1,
        "id": 20
      },
      {
        "namespace": 1,
        "id": 21
      },
      {
        "namespace": 1,
        "id": 22
      },
      {
        "namespace": 1,
        "id": 23
      },
      {
        "namespace": 1,
        "id": 49
      },
      {
        "namespace": 1,
        "id": 62
      },
      {
        "namespace": 1,
        "id": 136
      }
    ],
    "scope": {
      "accounts": [
        1234
      ]
    },
    "resourceOwnerEpoch": 0,
    "validFromMs": 0,
    "expiresAtMs": "1764086400000",
    "limitsVersion": 1,
    "limits": {
      "maxRequestCount": null,
      "windowMs": 1000,
      "maxOrderLots": null,
      "maxOrderQuoteAtoms": null,
      "maxWindowQuoteAtoms": null,
      "maxFeeQuoteAtoms": null,
      "markets": [
        {
          "market": 1,
          "marketSpecVersion": "1",
          "minTick": 1,
          "maxTick": 4294967295
        }
      ]
    }
  }
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=GrantCapability)

### RevokeCapability

Revoke a grant.

Signed by: account (main wallet); API wallets cannot · nonce lane `management`

`expectedEpoch`: the grant's current epoch (from `GET /v1/grants`).

```json
{
  "kind": "RevokeCapability",
  "grantId": "0x1111111111111111111111111111111111111111111111111111111111111111",
  "expectedEpoch": 0
}
```

[Try it in the API playground](https://dex-preview.unibook.site/app/api-playground/?cmd=RevokeCapability)

## Registration and governance

These commands need several parties, so they have no single-signer example and are not in the playground:

- `RegisterDexV2`, `AcceptDexOwner`, `RegisterBuilder`, `RegisterBuilderLinked`: registration with acceptances from the owner, payout and linked accounts; build them with the SDK.
- `Propose`, `SubmitAndExecute`, `ExecuteProposal`, `CancelProposal`, `FreezeMarket`, `ReleaseMarketLock`, `PauseTimeSet`, `RestorePausedTimeSet`: signed by Council members with the Council's own tooling; not covered by this reference.

## Built with the SDK

### SetGrantPaused

Pause or resume a grant.
