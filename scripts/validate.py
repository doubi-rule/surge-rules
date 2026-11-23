#!/usr/bin/env python3
"""
validate.py - 校验 rules/*.list
用法: python3 scripts/validate.py
检查: 格式错误 / 重复 / 未排序 / 被父域名覆盖 / DOMAIN-KEYWORD 滥用 / 空行
退出码 0=通过, 1=失败 (给 GitHub Actions 用)
"""
import sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rules"
ALLOWED = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "USER-AGENT", "PROCESS-NAME"}
DOMAIN_RE = re.compile(r"^[a-z0-9\-\.]+$")

errors, warnings = [], []

for f in sorted(ROOT.glob("*.list")):
    lines = [l.strip() for l in f.read_text().splitlines()]
    seen, suffixes, values = set(), [], []
    for i, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        if line.startswith("//"):
            errors.append(f"{f.name}:{i} 用 # 注释, 不要用 // : {line}")
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2 or parts[0] not in ALLOWED:
            errors.append(f"{f.name}:{i} 格式错误, 应为 TYPE,value : {line}")
            continue
        typ, val = parts
        if line in seen:
            errors.append(f"{f.name}:{i} 重复: {line}")
        seen.add(line)
        if typ in ("DOMAIN", "DOMAIN-SUFFIX"):
            if not DOMAIN_RE.match(val):
                errors.append(f"{f.name}:{i} 域名不合法: {val}")
            if typ == "DOMAIN-SUFFIX":
                suffixes.append(val)
            values.append(val)
        if typ == "DOMAIN-KEYWORD" and len(val) < 4:
            warnings.append(f"{f.name}:{i} KEYWORD 太短容易误杀: {line}")
    # 排序检查 (只看非注释行)
    body = [l for l in lines if l and not l.startswith("#")]
    if body != sorted(body):
        warnings.append(f"{f.name} 未按 A-Z 排序, 建议排序后提交")
    # 覆盖检查: a.com 被 com 覆盖等
    for s in suffixes:
        for parent in suffixes:
            if s != parent and s.endswith("." + parent):
                warnings.append(f"{f.name} {s} 已被 {parent} 覆盖, 可删除")
                break

for w in warnings:
    print("WARN:", w)
for e in errors:
    print("ERROR:", e)

print(f"\n检查完成: {len(errors)} 错误, {len(warnings)} 警告")
sys.exit(1 if errors else 0)
