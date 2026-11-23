#!/bin/bash
# sync-upstream.sh - 可选: 把上游 reject 合并进来, 再加自己的 override
# 上游: Loyalsoldier reject (每天 6:30 自动构建)
# 用法: bash scripts/sync-upstream.sh
# 原理: 下载上游 -> 去重 -> 减去 allowlist -> 生成 rules/reject-upstream.list (不要手改这个文件)
set -e
cd "$(dirname "$0")/.."
curl -sL https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/ruleset/reject.txt -o /tmp/upstream-reject.txt
# 只保留 DOMAIN-SUFFIX 行, 去重排序
grep "^DOMAIN-SUFFIX," /tmp/upstream-reject.txt | sort -u > rules/reject-upstream.list
# 如果有 allowlist, 在这里减掉 (每行一个域名)
if [ -f rules/allowlist.txt ]; then
  grep -v -F -f rules/allowlist.txt rules/reject-upstream.list > /tmp/r.txt && mv /tmp/r.txt rules/reject-upstream.list
fi
wc -l rules/reject-upstream.list
python3 scripts/validate.py
echo "同步完成, 记得 git add + commit + push"
