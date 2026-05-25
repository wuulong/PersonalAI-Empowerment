#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《個人AI賦能》v1.2.3 學術聯邦共創工具 - 學生文獻貢獻導出器 (export_contributions.py)

目的：
從研究生本地的 SQLite 主權庫中，將高品質的 `papers`（背景文獻）與 `paper_relations`（文獻關係）
導出為純文字的 JSON 貢獻包，以便提交 Git 拉取請求 (Pull Request)，徹底消滅資料庫二進位衝突。
"""

import os
import sqlite3
import json
import argparse

def export_contributions(db_path, output_dir, topic_id=None):
    if not os.path.exists(db_path):
        print(f"[-] 錯誤：找不到 SQLite 資料庫：{db_path}")
        return

    print(f"[*] 正在連線資料庫：{db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. 查詢 papers 資料
    papers_query = "SELECT paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data FROM papers"
    params = []
    if topic_id:
        papers_query += " WHERE topic_id = ?"
        params.append(topic_id)
        
    cursor.execute(papers_query, params)
    papers_rows = cursor.fetchall()
    
    papers_list = []
    paper_ids = set()
    for row in papers_rows:
        paper_ids.add(row[0])
        papers_list.append({
            "paper_id": row[0],
            "task_id": row[1],
            "topic_id": row[2],
            "title": row[3],
            "authors": row[4],
            "year": row[5],
            "core_method": row[6],
            "cite_key": row[7],
            "bibtex": row[8],
            "meta_data": json.loads(row[9]) if row[9] else None
        })

    print(f"[+] 成功讀取 {len(papers_list)} 筆文獻資料。")

    # 2. 查詢 paper_relations 資料
    relations_list = []
    if len(paper_ids) > 0:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='paper_relations'")
        if cursor.fetchone():
            # 撈取與當前 papers 相關的關係資料
            placeholders = ",".join("?" for _ in paper_ids)
            relations_query = f"SELECT relation_id, source_paper_id, target_paper_id, relation_type, description FROM paper_relations WHERE source_paper_id IN ({placeholders}) OR target_paper_id IN ({placeholders})"
            cursor.execute(relations_query, list(paper_ids) + list(paper_ids))
            relations_rows = cursor.fetchall()
            
            for row in relations_rows:
                relations_list.append({
                    "relation_id": row[0],
                    "source_paper_id": row[1],
                    "target_paper_id": row[2],
                    "relation_type": row[3],
                    "description": row[4]
                })
            print(f"[+] 成功讀取 {len(relations_list)} 筆文獻演化關係資料。")
        else:
            print("[!] 提示：資料庫中尚未建立 'paper_relations' 關係表，跳過關係讀取。")
    
    conn.close()

    # 3. 組裝並輸出為 JSON
    contribution_data = {
        "generator": "Antigravity Academic Co-creation Exporter v1.2.3",
        "topic_id": topic_id if topic_id else "all",
        "papers": papers_list,
        "paper_relations": relations_list
    }

    os.makedirs(output_dir, exist_ok=True)
    filename = f"contrib_{topic_id if topic_id else 'all'}.json"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(contribution_data, f, ensure_ascii=False, indent=2)

    print(f"[+] 成功匯出純文字貢獻包：{output_path}")
    print("[*] 您現在可以安全將此 JSON 檔案提交至 Git 進行聯邦共創！\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="主權聯邦共創 - 學生文獻貢獻導出器")
    parser.add_argument("--db", default="/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db", help="SQLite 資料庫檔案路徑")
    parser.add_argument("--out-dir", default="/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/contributions", help="JSON 貢獻包輸出目錄")
    parser.add_argument("--topic", default=None, help="指定要導出的子主題 ID (選填)")
    
    args = parser.parse_args()
    export_contributions(args.db, args.out_dir, args.topic)
