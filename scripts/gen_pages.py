import sys, yaml

root, sha = sys.argv[1], sys.argv[2]
spec_path = f"{root}/api/openapi-v1.yaml"
srcs = {lang: f"https://raw.githubusercontent.com/chainupcloud/dex-os-docs/{sha}/api/openapi-v1{suffix}.yaml"
        for lang, suffix in (("en", ""), ("zh", ".zh"))}
spec = yaml.safe_load(open(spec_path))
zh = yaml.safe_load(open(f"{root}/api/openapi-v1.zh.yaml"))
assert {p: sorted(i) for p, i in zh["paths"].items()} == {p: sorted(i) for p, i in spec["paths"].items()}, "zh spec operations differ"

pages = {
    "Market data": ("market-data", "Market data", "市场行情", None, None),
    "Account": ("account", "Account", "账户", None, None),
    "Funds": ("funds", "Funds", "资金", None, None),
    "Vaults": ("vaults", "Vaults", "金库", None, None),
    "Trading": ("trading", "Trading", "交易",
        "Signed writes are submitted through `POST /v1/commands`; see the [authentication guide](../developers/authentication.md). Which commands it accepts, who signs them and their nonce lanes: [Commands overview](trading/commands.md).",
        "签名写请求统一通过 `POST /v1/commands` 提交，签法见[认证指南](../developers/authentication.md)。可以提交哪些命令、由谁签名、用哪条 nonce 序列，见[命令总览](trading/commands.md)。"),
    "Subscriptions": ("subscriptions", "Subscriptions", "订阅",
        "For channels, heartbeats, and recovery, see the [WebSocket guide](../developers/websocket.md).",
        "频道、心跳与恢复见 [WebSocket 指南](../developers/websocket.md)。"),
    "Oracle": ("oracle", "Oracle", "预言机", None, None),
    "Merchants": ("merchants", "Merchants", "商户", None, None),
    "Governance": ("governance", "Governance", "治理", None, None),
}

ops = {t: [] for t in pages}
for path, item in spec["paths"].items():
    for method, op in item.items():
        if method not in ("get", "post", "put", "patch", "delete"):
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
                f'{{% openapi src="{srcs[lang]}" path="{path}" method="{method}" %}}',
                srcs[lang],
                "{% endopenapi %}",
                "",
            ]
        open(f"{root}/content/{lang}/api/{slug}.md", "w").write("\n".join(out).rstrip("\n") + "\n")

print({t: len(v) for t, v in ops.items()}, sum(len(v) for v in ops.values()))
