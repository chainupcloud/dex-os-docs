# Self-custody and withdrawal tracking

Withdrawal tickets, the funds history, a deposit by receipt, and the escape preview: an estimate of what the account could claim on the custody chain from the frozen root once escape is triggered.

## GET /v1/accounts/{id}/tickets

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml" path="/v1/accounts/{id}/tickets" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/accounts/{id}/tickets/{ticket}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml" path="/v1/accounts/{id}/tickets/{ticket}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/accounts/{id}/funds-history

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml" path="/v1/accounts/{id}/funds-history" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/accounts/{id}/escape-preview

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml" path="/v1/accounts/{id}/escape-preview" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/custody/{key}/deposits/{asset}/{version}/{id}

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml" path="/v1/custody/{key}/deposits/{asset}/{version}/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/e04c6559f31ee164c06ff8742170aa08c6e29ec4/api/openapi-v1.yaml
{% endopenapi %}
