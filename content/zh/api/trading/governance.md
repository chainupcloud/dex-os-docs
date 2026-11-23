# 授权、注册与治理

下面每个示例都是命令的 JSON 形态，即需要你填的字段。SDK（或 [API 调试台](https://dex-preview.unibook.site/app/api-playground/)）再补上 nonce 与有效期、签名并编码；HTTP 请求一律是 `POST /v1/commands`，请求体 `{"command":"0x…"}`。调试台在预览网络上运行，用临时私钥和测试资金，会逐步显示读 nonce、EIP-712 待签数据、签好的命令、响应与回执，并能把提交复制成 curl。

## 字段

| 字段 | 含义 |
|---|---|
| `market` | 市场号：`GET /v1/markets` 返回的 `signingMarketId` |

64 位数值（单号、金额、时间）可以写成十进制字符串。

## 授权

### GrantCapability

授权一个 API 钱包：账户、操作、市场、价格带、额度与到期时间。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `management`

`grantId` 由签发策略与 `grantSalt` 算出，SDK（`dexosv1` 的 `ApproveAgent`）与调试台会算好。`actions` 列出允许的操作，`limits.markets` 列出市场、规格版本与价格带。

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

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=GrantCapability)

### RevokeCapability

撤销一项授权。

签名：账户（主钱包）；API 钱包不能签 · nonce 序列 `management`

`expectedEpoch`：授权当前的纪元（`GET /v1/grants`）。

```json
{
  "kind": "RevokeCapability",
  "grantId": "0x1111111111111111111111111111111111111111111111111111111111111111",
  "expectedEpoch": 0
}
```

[在 API 调试台里试一下](https://dex-preview.unibook.site/app/api-playground/?cmd=RevokeCapability)

## 注册与治理

下面这些命令要多方参与，没有单人签名的示例，调试台里也没有：

- `RegisterDexV2`、`AcceptDexOwner`、`RegisterBuilder`、`RegisterBuilderLinked`：注册时需要所有者、收款账户、关联方各自确认，请用 SDK 构造。读接口见[商户](../merchants.md)。
- `Propose`、`SubmitAndExecute`、`ExecuteProposal`、`CancelProposal`、`FreezeMarket`、`ReleaseMarketLock`、`PauseTimeSet`、`RestorePausedTimeSet`：由理事会成员签名，经 `POST /v1/governance/signatures` 收集。读接口见[治理](../governance.md)。

## 用 SDK 构造

### SetGrantPaused

暂停或恢复一项授权。
