#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《個人AI賦能》v1.2.3 學術聯邦共創工具 - 本地聯邦資料庫一鍵重構器 (rebuild_lab_brain.py)

目的：
學弟妹或指導教授拉取最新的 Git 代碼倉庫後，一鍵執行此腳本，系統會：
1. 讀取 `schema.sql`，在 0.5 秒內建立全新的乾淨 SQLite 資料庫結構。
2. 自動掃描 `contributions/` 目錄下的所有純文字 JSON 貢獻包。
3. 將所有學長姐貢獻的背景文獻與關係鏈安全寫入，重構出 100% 整合的聯邦大腦！
"""

import os
import sqlite3
import json
import argparse

def rebuild_database(db_path, schema_path, contrib_dir):
    print(f"[*] 啟動一鍵重構主權聯邦資料庫：{db_path}")
    
    # 1. 刪除原有資料庫 (如果存在)，以確保全新的乾淨投影
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("  [+] 已刪除舊的資料庫實體檔案。")
        except Exception as e:
            print(f"  [-] 無法刪除舊資料庫：{e} (將直接進行表格覆蓋)")

    # 2. 建立新資料庫並初始化結構
    if not os.path.exists(schema_path):
        print(f"[-] 錯誤：找不到 schema.sql 定義檔：{schema_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;") # 暫時關閉外鍵約束以供聯邦 Bulk Ingestion

    print(f"[*] 正在讀取 schema.sql 並初始化 DDL...")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    try:
        cursor.executescript(schema_sql)
        print("  [+] 資料庫結構 initialization (十一表聯邦 DDL) 成功完成！")
        cursor.execute("PRAGMA foreign_keys = OFF;") # 再次強制關閉外鍵以應對 schema.sql 中的 PRAGMA ON
    except Exception as e:
        print(f"  [-] DDL 初始化失敗：{e}")
        conn.close()
        return

    # 3. 掃描 contributions 目錄並寫入數據
    if not os.path.exists(contrib_dir):
        print(f"[!] 警告：找不到貢獻包目錄：{contrib_dir} (將保留空的十一表結構)")
        conn.commit()
        conn.close()
        return

    print(f"[*] 正在掃描共創貢獻目錄：{contrib_dir}")
    json_files = [f for f in os.listdir(contrib_dir) if f.endswith(".json")]

    if not json_files:
        print("  [o] 提示： contributions 目錄中尚無任何 JSON 貢獻包。")
    
    papers_count = 0
    relations_count = 0

    for json_file in json_files:
        json_path = os.path.join(contrib_dir, json_file)
        print(f"  - 載入貢獻包：{json_file}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"    [-] JSON 解析失敗：{e} (跳過)")
                continue

            # A. 寫入 papers
            papers_data = data.get("papers", [])
            for p in papers_data:
                # 使用 INSERT OR IGNORE 確保幂等性與防重複
                cursor.execute("""
                INSERT OR IGNORE INTO papers (
                    paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get("paper_id"), p.get("task_id"), p.get("topic_id"),
                    p.get("title"), p.get("authors"), p.get("year"),
                    p.get("core_method"), p.get("cite_key"), p.get("bibtex"),
                    json.dumps(p.get("meta_data")) if p.get("meta_data") else None
                ))
                if cursor.rowcount > 0:
                    papers_count += 1

            # B. 寫入 paper_relations
            relations_data = data.get("paper_relations", [])
            for r in relations_data:
                cursor.execute("""
                INSERT OR IGNORE INTO paper_relations (
                    relation_id, source_paper_id, target_paper_id, relation_type, description
                ) VALUES (?, ?, ?, ?, ?)
                """, (
                    r.get("relation_id"), r.get("source_paper_id"),
                    r.get("target_paper_id"), r.get("relation_type"),
                    r.get("description")
                ))
                if cursor.rowcount > 0:
                    relations_count += 1

    conn.commit()
    conn.close()

    print(f"\n[+] 重構完成！")
    print(f"  - 累計成功寫入背景文獻 (papers)：{papers_count} 筆。")
    print(f"  - 累計成功寫入演化關係 (relations)：{relations_count} 筆。")
    print(f"[*] 實驗室「聯邦共有大腦」已成功在本地重建！您可立即開啟 SQL 照妖鏡進行查詢。\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="主權聯邦共創 - 本地聯邦資料庫一鍵重構器")
    parser.add_argument("--db", default="/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db", help="重建資料庫之輸出路徑")
    parser.add_argument("--schema", default="/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/scripts/research/schema.sql", help="schema.sql DDL 路徑")
    parser.add_argument("--contrib-dir", default="/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/contributions", help="JSON 貢獻包來源目錄")
    
    args = parser.parse_args()
    rebuild_database(args.db, args.schema, args.contrib_dir)
