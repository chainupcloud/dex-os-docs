import os, sys, yaml

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
}

# Role-specific and advanced endpoints: listed in their own section ("Advanced API"), whatever their tag.
# Every operation of a tag missing from `pages` must be placed here.
advanced = {
    "ledger-accounts": ("Ledger accounts and grants", "账本账户与授权",
        "Ledger-level views by account id or policy, for SDK authors and multi-signer accounts. Single-signer integrations use the address-based reads on the [Account](../account.md) page.",
        "按账户编号或签名策略查询的账本层视图，给 SDK 作者和多签账户用。单签名人的接入用[账户](../account.md)页里按地址查询的接口即可。",
        ["GET /v1/accounts", "GET /v1/accounts/{id}", "GET /v1/account/by-address/{address}", "GET /v1/grants", "GET /v1/nonces"]),
    "self-custody": ("Self-custody and withdrawal tracking", "自托管与提款追踪",
        "Withdrawal tickets, the funds history, a deposit by receipt, and the escape preview: an estimate of what the account could claim on the custody chain from the frozen root once escape is triggered.",
        "提款凭证、资金流水、按回执查入金，以及逃生预估：触发逃生后，账户按冻结时的账本根能在托管链上取回多少的估算。",
        ["GET /v1/accounts/{id}/tickets", "GET /v1/accounts/{id}/tickets/{ticket}", "GET /v1/accounts/{id}/funds-history",
         "GET /v1/accounts/{id}/escape-preview", "GET /v1/custody/{key}/deposits/{asset}/{version}/{id}"]),
    "backfill": ("Event backfill and async results", "事件补数与异步结果",
        "Fill gaps after a WebSocket disconnect (see the [WebSocket guide](../../developers/websocket.md)) and read the final result of vault deposits and claims.",
        "WebSocket 断线后补齐事件（见 [WebSocket 指南](../../developers/websocket.md)），以及查询金库存入、领取的最终结果。",
        ["GET /v1/events", "GET /v1/vaults/{id}/transitions/{source}/{ordinal}"]),
}
placed = {key: slug for slug, (*_, keys) in advanced.items() for key in keys}

ops = {t: [] for t in pages}
adv_ops = {slug: [] for slug in advanced}
for path, item in spec["paths"].items():
    for method, op in item.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        key = f"{method.upper()} {path}"
        if key in placed:
            adv_ops[placed.pop(key)].append((method, path, op.get("summary", "").strip()))
            continue
        tags = op.get("tags") or []
        assert len(tags) == 1 and tags[0] in pages, (method, path, tags)
        ops[tags[0]].append((method, path, op.get("summary", "").strip()))
assert not placed, f"advanced entries not in the spec: {sorted(placed)}"
for slug, (*_, keys) in advanced.items():
    order = {k: i for i, k in enumerate(keys)}
    adv_ops[slug].sort(key=lambda o: order[f"{o[0].upper()} {o[1]}"])


def render(title, intro, items, lang):
    out = [f"# {title}", ""]
    if intro:
        out += [intro, ""]
    for method, path, summary in items:
        out += [f"## {method.upper()} {path}", ""]
        out += [
            f'{{% openapi src="{srcs[lang]}" path="{path}" method="{method}" %}}',
            srcs[lang],
            "{% endopenapi %}",
            "",
        ]
    return "\n".join(out).rstrip("\n") + "\n"


for tag, (slug, en, zh, intro_en, intro_zh) in pages.items():
    for lang, title, intro in (("en", en, intro_en), ("zh", zh, intro_zh)):
        open(f"{root}/content/{lang}/api/{slug}.md", "w").write(render(title, intro, ops[tag], lang))

for slug, (en, zh, intro_en, intro_zh, _) in advanced.items():
    for lang, title, intro in (("en", en, intro_en), ("zh", zh, intro_zh)):
        os.makedirs(f"{root}/content/{lang}/api/advanced", exist_ok=True)
        open(f"{root}/content/{lang}/api/advanced/{slug}.md", "w").write(render(title, intro, adv_ops[slug], lang))

counts = {t: len(v) for t, v in ops.items()} | {f"advanced/{s}": len(v) for s, v in adv_ops.items()}
print(counts, sum(counts.values()))
