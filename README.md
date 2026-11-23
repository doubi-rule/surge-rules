# my-surge-rules - 我的 Surge 规则集 (马来西亚)

自维护规则集, 不依赖别人更新。改一个域名, push 到 GitHub, 手机上刷新就生效。

## 目录结构

```
.
├── rules/
│   ├── my-direct.list    # 马来西亚本地直连 - 最重要, 自己维护
│   ├── ai.list           # ChatGPT / Claude / Gemini
│   ├── streaming.list    # Netflix / Disney+ / TikTok / YouTube
│   ├── proxy.list        # 其他要走代理的
│   ├── apple.list        # Apple / iCloud, 默认 DIRECT
│   ├── reject.list       # 广告/追踪, 保守, 自己加
│   └── reject-upstream.list  # 自动同步上游的, 不要手改
├── scripts/
│   ├── validate.py       # 校验: 格式/重复/排序/覆盖
│   └── sync-upstream.sh  # 可选: 同步 Loyalsoldier reject
├── .github/workflows/validate.yml  # push 自动校验
├── surge-snippet.conf    # 贴进 Surge 配置的 [Rule] 段
└── README.md
```

## 1. 建仓库 (5 分钟)

1. GitHub 仓库已建好: https://github.com/doubi-rule/surge-rules (公开, main 分支)
2. 把这个文件夹全部 push 上去, 分支 `main` (见下面第 2 节的 3 种方法)
3. 确认能打开: `https://raw.githubusercontent.com/doubi-rule/surge-rules/main/rules/ai.list`

公开仓库才能让 Surge 直接拉 raw 链接。介意公开就用私有仓库 + jsDelivr? 不行, Surge 拉私有要 token, 别折腾, 规则集本身不含隐私, 公开最省事。

## 2. Surge 里引用

把 `surge-snippet.conf` 里的 `[Rule]` 贴进你的 `Surge6-MY.conf`, 把 `doubi-rule/surge-rules` 换掉。

核心原则: **list 文件只写匹配, 不写策略**。每行 `DOMAIN-SUFFIX,example.com`, 不要写 `,DIRECT` 在文件里, 策略在 `[Rule]` 那行定。这样同一个 list 可以在不同配置里走不同策略。

## 3. 日常维护 - 3 个动作

### 加一条规则
1. 在 Surge 请求记录里长按域名 > 复制
2. 决定放哪个文件: 本地银行/政府放 `my-direct.list`, AI 放 `ai.list`, 广告放 `reject.list`
3. 用 `DOMAIN-SUFFIX,域名` 写进去, 按 A-Z 排序, 保存

### 改一条规则
直接改文件, push, 手机 Surge > 配置 > 更新规则集。改动推到 main 后刷新就能拿到, 不用改 Surge 配置。

### 删一条规则 / 误杀处理
1. 先在 Surge 请求记录确认是哪个 list 命中的
2. 从对应文件删掉, 或加到 `rules/allowlist.txt` (一行一个域名, sync 时会自动减掉)
3. Reject 误杀最常见, 宁可漏拦不要误杀。

## 4. 校验 (每次 push 前跑)

```bash
python3 scripts/validate.py
```

检查重复、格式错误、未排序、被父域名覆盖。GitHub Actions 也会在 push 时自动跑, 失败就修了再推。

## 5. 上游同步 (可选, 进阶)

不想自己攒几万条广告规则, 就跑:

```bash
bash scripts/sync-upstream.sh
```

它会下载 Loyalsoldier 的 reject, 去重后生成 `reject-upstream.list`, 再用你的 `allowlist.txt` 减掉误杀的。Loyalsoldier 是每天早上 6:30 自动构建的, 你可以加个 cron / GitHub Actions 定时跑这个脚本。

新手建议: 先别开自动同步, 手工维护 2 周, 知道自己要什么再开。

## 格式速查

| 写法 | 意思 | 例子 |
|---|---|---|
| `DOMAIN-SUFFIX,example.com` | example.com + 所有子域名 | 最常用, 90% 用这个 |
| `DOMAIN,api.example.com` | 只匹配这一个域名 | 精确控制 |
| `DOMAIN-KEYWORD,ads` | 域名里含 ads | 慎用, 很容易误杀 |
| `IP-CIDR,1.2.3.0/24,no-resolve` | IP 段, 不解析 DNS | 放最后, 别放域名前面 |
| `# 注释` | 注释 | 每行开头写 # |

规则从上到下匹配, DOMAIN-SET / RULE-SET 域名类放前面, IP / GEOIP 类放后面, 最后 `FINAL,DIRECT`。

## 命名规范

- 文件名小写, 用 `-` 连接: `my-direct.list`, 不要用空格/中文
- 一个文件只管一类服务, 不要把 AI 和流媒体混在一个文件
- 域名全小写, 去掉 `www.`, 去掉 `https://`
- 不要写 `*.example.com`, 写 `DOMAIN-SUFFIX,example.com` 就够了
