# 事件补数与异步结果

WebSocket 断线后补齐事件（见 [WebSocket 指南](../../developers/websocket.md)），以及查询金库存入、领取的最终结果。

## GET /v1/events

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.zh.yaml" path="/v1/events" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/vaults/{id}/transitions/{source}/{ordinal}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.zh.yaml" path="/v1/vaults/{id}/transitions/{source}/{ordinal}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.zh.yaml
{% endopenapi %}
