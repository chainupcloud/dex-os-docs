# 安全

签名写请求统一通过 `POST /v1/commands` 提交。本页还包括托管、治理和集群相关的读取接口。

## POST /v1/commands

提交完整新签名命令

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/commands" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/testnet/markets/{id}/oracle

Market oracle signing parameters

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/testnet/markets/{id}/oracle" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/markets/{id}/oracle

Market oracle round parameters (reporters / relays)

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/markets/{id}/oracle" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/testnet/mint-policy

TestMint policy

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/testnet/mint-policy" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/merchant-admission

Merchant admission

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/merchant-admission" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/price-venues

Price venues

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/price-venues" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/business-parameters

Business parameters

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/business-parameters" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/reporter-sets/{id}/followers

Markets following a reporter set

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/reporter-sets/{id}/followers" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/oracle-resources/{kind}/{id}

Oracle resource configuration

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/oracle-resources/{kind}/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/dexes

Merchant DEX list

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/dexes" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/dexes/{id}

Merchant DEX

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/dexes/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/builders/{id}

Builder registration

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/builders/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/dex-registrations/{id}

Merchant DEX registration

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/dex-registrations/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/dex-owner-proposals/{id}

DEX owner transfer proposal

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/dex-owner-proposals/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}

Custody group

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/checkpoints/latest

Global checkpoint progress

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/checkpoints/latest" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/network

Network identity

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/network" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/time

Certified time

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/time" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/council

Council

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/council" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/cluster/members

Cluster members

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/cluster/members" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/accounts

Accounts by policy member

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/accounts" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/accounts/{id}

Security account

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/accounts/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/accounts/{id}/tickets/{ticket}

Withdrawal ticket

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/accounts/{id}/tickets/{ticket}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/grants

Grants issued by an account policy

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/grants" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/nonces

Nonce window

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/nonces" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/markets

Market spec versions

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/markets" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/escape-preview

Escape leaf preview

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/escape-preview" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody

Custody group discovery

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/deposits/{asset}/{version}/{id}

Deposit status by receipt

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/deposits/{asset}/{version}/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/deposits/by-tx/{tx}

Deposit status by transaction

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/deposits/by-tx/{tx}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/diagnostics

Stuck-funds diagnostics

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/diagnostics" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/accounts/{id}/tickets

Account withdrawal tickets

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/accounts/{id}/tickets" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/accounts/{id}/funds-history

Account funds history

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/accounts/{id}/funds-history" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance

Council governance overview

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance/proposals

Governance proposals

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/proposals" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance/proposals/{id}

Governance proposal detail

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/proposals/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## POST /v1/security/governance/preconditions

Compute governance preconditions

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/preconditions" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## POST /v1/security/governance/simulate

Simulate a governance envelope

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/simulate" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance/services

Services and Council grants

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/services" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance/signatures

Signature collections

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/signatures" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## POST /v1/security/governance/signatures

Submit governance signatures

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/signatures" method="post" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/governance/signatures/{id}

One signature collection (export)

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/governance/signatures/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/late-deposits

Late deposit receipts

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/late-deposits" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/late-deposits/{id}

Late deposit receipt

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/late-deposits/{id}" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}

## GET /v1/security/custody/{key}/deposit-precheck

Deposit precheck

{% openapi src="https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml" path="/v1/security/custody/{key}/deposit-precheck" method="get" %}
https://raw.githubusercontent.com/chainupcloud/dex-os-docs/b24ed31b718e7ae378e9d7e42606f22105cab181/api/openapi-v1.yaml
{% endopenapi %}
