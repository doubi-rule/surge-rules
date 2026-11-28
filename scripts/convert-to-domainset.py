#!/usr/bin/env python3
"""Convert rules/*.list (RULE-SET, DOMAIN-SUFFIX) to domain-set/*.txt (DOMAIN-SET).
Usage: python3 scripts/convert-to-domainset.py
DOMAIN-SUFFIX,example.com -> .example.com (domain + all subdomains)
DOMAIN,example.com -> example.com (exact hostname only)
Run after editing any rules/*.list, then push both folders.
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src_dir = root / "rules"
dst_dir = root / "domain-set"
dst_dir.mkdir(exist_ok=True)

names = ["ai", "apple", "douyin", "microsoft", "my-direct", "proxy", "reject", "school", "streaming"]
for name in names:
    src = src_dir / f"{name}.list"
    if not src.exists():
        print(f"skip {name}: no {src}")
        continue
    domains = []
    for line in src.read_text().splitlines():
        line = line.strip()
        if line.startswith("DOMAIN-SUFFIX,"):
            domains.append("." + line.split(",", 1)[1].strip())
        elif line.startswith("DOMAIN,"):
            domains.append(line.split(",", 1)[1].strip())
    domains = sorted(set(domains))
    out = [
        f"# {name}.txt - Surge DOMAIN-SET, generated from rules/{name}.list, do not edit by hand",
        f"# Source: https://github.com/doubi-rule/surge-rules/blob/main/rules/{name}.list",
        "# Format: .example.com = match domain + all subdomains (like DOMAIN-SUFFIX)",
        f"# Usage: DOMAIN-SET,https://raw.githubusercontent.com/doubi-rule/surge-rules/main/domain-set/{name}.txt,<policy>",
        "",
        *domains,
    ]
    (dst_dir / f"{name}.txt").write_text("\n".join(out) + "\n")
    print(f"{name}: {len(domains)} domains -> domain-set/{name}.txt")
