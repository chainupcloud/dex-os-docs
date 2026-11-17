import sys, yaml

root, sha = sys.argv[1], sys.argv[2]
spec_path = f"{root}/api/openapi-v1.yaml"
src = f"https://raw.githubusercontent.com/chainupcloud/dex-os-docs/{sha}/api/openapi-v1.yaml"
spec = yaml.safe_load(open(spec_path))

pages = {
    "Exchange": ("exchange", "Exchange", "交易所信息", None, None),
    "Market data": ("market-data", "Market data", "市场行情", None, None),
    "Account": ("account", "Account", "账户", None, None),
    "Funds": ("funds", "Funds", "资金", None, None),
    "Vaults": ("vaults", "Vaults", "金库", None, None),
    "Subscriptions": ("subscriptions", "Subscriptions", "订阅",
        "For channels, heartbeats, and recovery, see the [WebSocket guide](../developers/websocket.md).",
        "频道、心跳与恢复见 [WebSocket 指南](../developers/websocket.md)。"),
    "Security": ("security", "Security", "安全",
        "Signed writes are submitted through `POST /v1/commands`. This page also covers custody, governance and cluster reads.",
        "签名写请求统一通过 `POST /v1/commands` 提交。本页还包括托管、治理和集群相关的读取接口。"),
}

hidden = {
    ("post", "/v1/orders/paired"),
    ("post", "/v1/account/cctp/deposit"),
    ("get", "/v1/testnet/markets/{id}/oracle"),
    ("get", "/v1/testnet/mint-policy"),
}
seen = set()
ops = {t: [] for t in pages}
for path, item in spec["paths"].items():
    for method, op in item.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        if (method, path) in hidden:
            seen.add((method, path))
            continue
        tags = op.get("tags") or []
        assert len(tags) == 1 and tags[0] in pages, (method, path, tags)
        ops[tags[0]].append((method, path, op.get("summary", "").strip()))

for tag, (slug, en, zh, intro_en, intro_zh) in pages.items():
    for lang, title, intro in (("en", en, intro_en), ("zh", zh, intro_zh)):
        out = [f"# {title}", ""]
        if intro:
            out += [intro, ""]
        for method, path, summary in ops[tag]:
            out += [f"## {method.upper()} {path}", ""]
            out += [
                f'{{% openapi src="{src}" path="{path}" method="{method}" %}}',
                src,
                "{% endopenapi %}",
                "",
            ]
        open(f"{root}/content/{lang}/api/{slug}.md", "w").write("\n".join(out).rstrip("\n") + "\n")

assert seen == hidden, hidden - seen
print({t: len(v) for t, v in ops.items()}, sum(len(v) for v in ops.values()))
