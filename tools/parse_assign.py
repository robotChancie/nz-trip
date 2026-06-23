#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新西兰行程网页 · 团队分工同步工具
用法:  python3 tools/parse_assign.py "<新Excel路径>"
作用:  读取【行程明细及分工】sheet，按 负责人/类别 输出结构化分工 JSON，
       供更新 index.html 中 squads 数据时直接参考。
"""
import sys, json
import pandas as pd

SHEET = "行程明细及分工"

def main():
    if len(sys.argv) < 2:
        print("用法: python3 tools/parse_assign.py <Excel路径>")
        sys.exit(1)
    path = sys.argv[1]
    xls = pd.ExcelFile(path)
    if SHEET not in xls.sheet_names:
        print(f"[ERROR] 找不到 sheet「{SHEET}」, 现有: {xls.sheet_names}")
        sys.exit(2)
    df = pd.read_excel(xls, sheet_name=SHEET, header=0)
    cols = list(df.columns)
    # 列约定: 0=类别 1=关联日期 2=项目/事项 3=预定建议 4=负责人 5=完成情况 6=预定信息
    rows = []
    for _, r in df.iterrows():
        item = str(r.iloc[2]).strip()
        owner = str(r.iloc[4]).strip() if len(r) > 4 else ""
        status = str(r.iloc[5]).strip() if len(r) > 5 else ""
        if item in ("", "nan"):
            continue
        rows.append({
            "类别": str(r.iloc[0]).strip(),
            "日期": str(r.iloc[1]).strip(),
            "项目": item,
            "负责人": "" if owner == "nan" else owner,
            "完成情况": "" if status == "nan" else status,
        })
    # 按负责人汇总
    by_owner = {}
    for it in rows:
        o = it["负责人"] or "未分配"
        by_owner.setdefault(o, []).append(it)
    print("COLUMNS:", cols)
    print("=" * 60)
    print("== 全部条目 ==")
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    print("=" * 60)
    print("== 按负责人汇总 ==")
    print(json.dumps(by_owner, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
