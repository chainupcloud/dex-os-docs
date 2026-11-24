# Builder 与 DEX 部署方

运营白标前端（builder）或 DEX 时用的读接口：入口解析、builder 费收入、商户准入与注册状态。对应的命令见[商户与 builder](../trading/merchants.md)。

## GET /v1/builder

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/builder" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/builders/{address}/summary

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/builders/{address}/summary" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/merchant-admission

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/merchant-admission" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/dex-registrations/{id}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/dex-registrations/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/builder-registrations/{id}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/builder-registrations/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}

## GET /v1/dex-owner-proposals/{id}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml" path="/v1/dex-owner-proposals/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/bf799cd15e60323dcd4c744076c4f27dbbbc6a99/api/openapi-v1.zh.yaml
{% endopenapi %}
