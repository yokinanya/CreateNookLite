#!/usr/bin/env python3
"""
检查 packwiz 包里所有模组的必需依赖是否都已满足。

用法：python3 check-deps.py
需要：curl 可用（用于访问 Modrinth API）
"""
import glob
import json
import os
import re
import subprocess
import sys

MODS_DIR = "mods"
API = "https://api.modrinth.com/v2"
UA = "CreateNookLite-depcheck/1.0"


def fetch(url):
    out = subprocess.run(
        ["curl", "-sL", "--max-time", "30", "-H", "User-Agent: " + UA, url],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    try:
        return json.loads(out.stdout)
    except Exception:
        return None


def main():
    # 1. 收集本地全~~部模组（不跳过任何文件！）~~
    local = {}       # mod-id -> (name, side, filename)
    local_slugs = {} # slug -> name
    for f in glob.glob(os.path.join(MODS_DIR, "*.pw.toml")):
        txt = open(f, encoding="utf-8").read()
        name = re.search(r'^name\s*=\s*"([^"]*)"', txt, re.M)
        side = re.search(r'^side\s*=\s*"([^"]*)"', txt, re.M)
        mid = re.search(r'mod-id\s*=\s*"([^"]*)"', txt)
        fn = re.search(r'^filename\s*=\s*"([^"]*)"', txt, re.M)
        if not mid:
            continue
        local[mid.group(1)] = {
            "name": name.group(1) if name else os.path.basename(f),
            "side": side.group(1) if side else "both",
            "file": os.path.basename(f),
            "filename": fn.group(1) if fn else "",
        }

    print("本地模组数: %d" % len(local))
    print()

    # 2. 逐个查依赖
    missing = []
    checked = 0
    for mid, info in sorted(local.items(), key=lambda x: x[1]["name"]):
        # 找该模组在 1.20.1 forge 下的版本
        vers = fetch("%s/project/%s/version?game_versions=%%5B%%221.20.1%%22%%5D&loaders=%%5B%%22forge%%22%%5D" % (API, mid))
        if not vers:
            continue
        # 找匹配已装文件的版本
        target = None
        for v in vers:
            if info["filename"] in [f.get("filename") for f in v.get("files", [])]:
                target = v
                break
        if target is None:
            target = vers[0]

        checked += 1
        for dep in target.get("dependencies", []):
            if dep.get("dependency_type") != "required":
                continue
            dpid = dep.get("project_id")
            if not dpid:
                continue
            if dpid in local:
                continue
            # 依赖缺失
            proj = fetch("%s/project/%s" % (API, dpid))
            dname = proj.get("title") if proj else dpid
            dslug = proj.get("slug") if proj else "?"
            missing.append({
                "by": info["name"],
                "by_side": info["side"],
                "dep_name": dname,
                "dep_slug": dslug,
            })

    print("已检查: %d 个模组" % checked)
    print()

    if not missing:
        print("✓ 所有必需依赖均已满足")
        return 0

    print("!! 缺少 %d 个必需依赖:" % len(missing))
    seen = set()
    for m in missing:
        key = (m["dep_slug"], m["by"])
        if key in seen:
            continue
        seen.add(key)
        print("  %-32s 被 %-28s [%s] 依赖" % (m["dep_name"], m["by"], m["by_side"]))
    print()
    print("修复方式：packwiz modrinth add <slug>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
