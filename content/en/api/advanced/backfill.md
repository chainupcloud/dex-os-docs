# Event backfill and async results

Fill gaps after a WebSocket disconnect (see the [WebSocket guide](../../developers/websocket.md)) and read the final result of vault deposits and claims.

## GET /v1/events

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.yaml" path="/v1/events" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/vaults/{id}/transitions/{source}/{ordinal}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.yaml" path="/v1/vaults/{id}/transitions/{source}/{ordinal}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.yaml
{% endopenapi %}
