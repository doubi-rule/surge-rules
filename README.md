# surge-rules — Self-Maintained Surge 6 Rules (Malaysia)

> English first. 中文版见下方。
> Self-maintained rules for Surge 6 on iOS, for a user in Malaysia. No dependency on other people's updates. Change a domain, push to GitHub, refresh on your phone — done.

## Structure

```
.
├── rules/                          # RULE-SET files (DOMAIN-SUFFIX,xxx)
│   ├── microsoft.list              # Microsoft 365 / school login — most important, always DIRECT, first
│   ├── school.list                 # US community colleges: JJC / Lane / Northampton, always DIRECT
│   ├── my-direct.list              # Malaysia local services, DIRECT
│   ├── ai.list                     # ChatGPT / Claude / Gemini / Muse / Meta AI
│   ├── streaming.list              # Netflix / Disney+ / TikTok / YouTube
│   ├── douyin.list                 # China Douyin — route via a fixed node (manual select, never auto)
│   ├── proxy.list                  # Other sites via proxy
│   ├── apple.list                  # Apple / iCloud, DIRECT
│   ├── reject.list                 # Ads / trackers, conservative, hand-maintained
│   ├── reject-upstream.list        # Full upstream list, generated, do not edit by hand
│   └── reject-upstream-01..10.list # Upstream split into 10 shards (~0.7 MB each, 203,233 rules total)
├── domain-set/                     # DOMAIN-SET version of the same lists (.example.com)
│   ├── ai.txt, apple.txt, douyin.txt, microsoft.txt, my-direct.txt
│   ├── proxy.txt, reject.txt, school.txt, streaming.txt
│   └── reject-upstream-01..10.txt # Upstream DOMAIN-SET shards (~0.41–0.47 MB each)
├── scripts/
│   ├── validate.py                 # Validate: format / duplicates / sorting / shadowing
│   ├── sync-upstream.sh            # Sync Loyalsoldier reject (optional)
│   └── convert-to-domainset.py     # Regenerate domain-set/*.txt from rules/*.list
├── surge-snippet.conf              # [Rule] section for Surge, RULE-SET version
├── surge-domainset-snippet.conf    # [Rule] section for Surge, DOMAIN-SET version
└── README.md
```

## Principles

- **Blacklist mode, `FINAL,DIRECT`.** Malaysia has open internet — only AI / streaming / specific proxy sites go via proxy, local MY services stay DIRECT. Singapore nodes first (lowest latency from MY).
- **List files only match, policy lives in `surge.conf`.** Each line is `DOMAIN-SUFFIX,example.com`, with no policy column. Policy is set in `[Rule]` via `RULE-SET,<url>,<policy>`.
- **Microsoft first, always DIRECT.** School email / school-account login uses Entra ID (`login.microsoftonline.com`). If it goes via proxy, MFA / SSO fails. `microsoft.list` is first in `[Rule]`, before REJECT.
- **RULE-SET or DOMAIN-SET — pick one, never both.** Same content in two formats; a URL cannot be both. DOMAIN-SET (`.example.com`) is faster for large lists — the 203k upstream list is where it matters; small lists feel the same either way.
- **Douyin stays manual.** `🎵 抖音 = select`, fixed on one node. Never `url-test` / `fallback` — a changing IP makes the IP location flip.

## Usage in Surge

Paste the `[Rule]` section from `surge-snippet.conf` (RULE-SET) or `surge-domainset-snippet.conf` (DOMAIN-SET) into your `Surge6-MY.conf`. Order matters:

```
microsoft.list, DIRECT
school.list, DIRECT
reject.list, REJECT
my-direct.list, DIRECT
apple.list, DIRECT
ai.list, 🤖 AI
streaming.list, 🎬 流媒体
douyin.list, 🎵 抖音
proxy.list, Proxy
reject-upstream-*.list, REJECT   # after streaming / Douyin / proxy — .bn5x.net in shard 02 would otherwise block disneyplus.bn5x.net
GEOIP,MY,DIRECT,no-resolve
FINAL,DIRECT
```

The repo is public (`main` branch) so Surge can fetch raw links directly, e.g. `https://raw.githubusercontent.com/doubi-rule/surge-rules/main/rules/ai.list`.

## Daily maintenance

1. **Add a rule:** copy the domain from Surge Recent Requests, decide the file (local bank / government → `my-direct.list`, AI → `ai.list`, ads → `reject.list`), add `DOMAIN-SUFFIX,<domain>`, keep A–Z order.
2. **Edit / delete:** edit the file, run validation, push. Refresh rule sets on your phone — no Surge config change needed.
3. **If a rule file changes, update both formats:** run `python3 scripts/convert-to-domainset.py`, then push `rules/*.list` and `domain-set/*.txt` together. Never push only one side.
4. **Validate before every push:**
   ```bash
   python3 scripts/validate.py
   ```
   Checks duplicates, format errors, unsorted lines, and shadowing. Must be 0 errors, 0 warnings.

## Upstream sync (optional)

```bash
bash scripts/sync-upstream.sh
```

Downloads Loyalsoldier `reject.txt`, deduplicates, generates `reject-upstream.list`, subtracts `rules/allowlist.txt` if present. The full list is split into 10 shards because a single 6.8 MB file cannot be pushed via the GitHub API.

## Format cheat sheet

| Syntax | Meaning |
|---|---|
| `DOMAIN-SUFFIX,example.com` | example.com + all subdomains — use this 90% of the time |
| `DOMAIN,api.example.com` | Only this exact hostname |
| `DOMAIN-KEYWORD,ads` | Hostname contains `ads` — use with care, easy to over-block |
| `# comment` | Comment |
| `.example.com` (DOMAIN-SET) | Same as `DOMAIN-SUFFIX,example.com` |

Rules match top to bottom. Domain rules first, IP / GEOIP last, then `FINAL,DIRECT`.

---

# surge-rules — 自维护 Surge 6 规则集（马来西亚）

> 英文首选，上面是英文版，下面是中文版。
> 自己维护的 Surge 6 iOS 规则集，马来西亚用户用，不依赖别人更新。改一个域名，push 到 GitHub，手机上刷新就生效。

## 目录结构

见上方英文版结构树，文件与英文版一致。

- `rules/`：RULE-SET 版（`DOMAIN-SUFFIX,xxx`），含 `microsoft.list`、`school.list`、`douyin.list`、`ai.list`（含 Muse / Meta AI）、`reject-upstream-01..10.list`（上游分片，共 203,233 条）
- `domain-set/`：DOMAIN-SET 版（`.xxx`），同一份内容两种格式，另有上游分片 `reject-upstream-01..10.txt`
- `scripts/`：`validate.py` 校验、`sync-upstream.sh` 同步上游、`convert-to-domainset.py` 生成 DOMAIN-SET 版
- `surge-snippet.conf` / `surge-domainset-snippet.conf`：两种版本的 `[Rule]` 段

## 原则

- **黑名单模式，`FINAL,DIRECT`。** 马来西亚网络开放，只有 AI / 流媒体 / 特定代理站点走代理，本地服务 DIRECT，新加坡节点优先（延迟最低）。
- **list 文件只写匹配，不写策略。** 每行 `DOMAIN-SUFFIX,example.com`，策略在 `[Rule]` 里定。
- **Microsoft 最重要，永远 DIRECT，放最前面。** 学校邮箱 / 学校账号走 Entra ID（`login.microsoftonline.com`），走代理会触发 MFA / SSO 失败，`microsoft.list` 在 `[Rule]` 最前面，在 REJECT 之前。
- **RULE-SET 和 DOMAIN-SET 二选一，不要同时用。** 同一份内容两种格式，同一个链接不能两种用法。DOMAIN-SET（`.example.com`）对大列表更快，20 万条上游列表才是真正提速的地方，小列表换不换没感觉。
- **抖音保持手动。** `🎵 抖音 = select`，固定一个节点，绝不用 `url-test` / `fallback`，IP 一变属地就跟着变。

## 在 Surge 里引用

把 `surge-snippet.conf`（RULE-SET 版）或 `surge-domainset-snippet.conf`（DOMAIN-SET 版）的 `[Rule]` 贴进 `Surge6-MY.conf`，顺序见上方英文版。注意上游拦截要放在 streaming / 抖音 / proxy 之后，`.bn5x.net` 在上游 02 号分片里，`.disneyplus.bn5x.net` 在 streaming 里，顺序错了会误拦 Disney+。

仓库公开（`main` 分支），Surge 可直接拉 raw 链接，例如 `https://raw.githubusercontent.com/doubi-rule/surge-rules/main/rules/ai.list`。

## 日常维护

1. **加规则：** 在 Surge 请求记录里复制域名，决定放哪个文件，写 `DOMAIN-SUFFIX,<域名>`，按 A–Z 排序。
2. **改 / 删：** 改文件、校验、push，手机上更新规则集即可，不用改 Surge 配置。
3. **改了规则文件，必须两个格式一起更新：** 跑 `python3 scripts/convert-to-domainset.py`，`rules/*.list` 和 `domain-set/*.txt` 一起推，绝不能只推一边。
4. **每次 push 前校验：** `python3 scripts/validate.py`，必须是 0 错误、0 警告。

## 上游同步（可选）

```bash
bash scripts/sync-upstream.sh
```

下载 Loyalsoldier 的 reject，去重后生成 `reject-upstream.list`，再用 `rules/allowlist.txt` 减掉误杀。完整列表拆成 10 个分片，因为单个 6.8MB 文件推不上 GitHub API。
