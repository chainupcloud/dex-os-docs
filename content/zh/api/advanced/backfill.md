# 事件补数与异步结果

WebSocket 断线后补齐事件（见 [WebSocket 指南](../../developers/websocket.md)），以及查询金库存入、领取的最终结果。

## GET /v1/events

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5122a71ad1a57c1182e3efef807af669d44e9b8c/api/openapi-v1.zh.yaml" path="/v1/events" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5122a71ad1a57c1182e3efef807af669d44e9b8c/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/vaults/{id}/transitions/{source}/{ordinal}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5122a71ad1a57c1182e3efef807af669d44e9b8c/api/openapi-v1.zh.yaml" path="/v1/vaults/{id}/transitions/{source}/{ordinal}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/5122a71ad1a57c1182e3efef807af669d44e9b8c/api/openapi-v1.zh.yaml
{% endopenapi %}
