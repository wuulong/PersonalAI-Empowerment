#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪐 個人學術主權資料庫 - Zotero Better BibTeX 聯邦大量遷移工具 (migrate_zotero_bib.py)

【💡 研究生極客心法】：
本檔案是一個獨立、乾淨且開箱即用的 Python 遷移腳本。
當您的文獻管理工具不是 Zotero (例如 Mendeley, EndNote) 或資料格式不同 (RIS, CSV, JSON) 時，
您可以直接將本檔案「整份餵給您的 AI 編程代理人 (如 Gemini, Claude)」，並對它下達 Prompt：
👉 『我目前使用的是 Mendeley 的 RIS 檔案 / Notion 的 CSV 檔案，請幫我改寫本腳本的解析區段，
     維持與主權資料庫 SQLite 10 表 Schema 的寫入映射與外鍵約束安全性。』
"""

import os
import re
import sys
import json
import sqlite3
import argparse

DEFAULT_DB_PATH = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db"

def migrate_bibtex_to_db(bib_file_path, db_path):
    if not os.path.exists(bib_file_path):
        print(f"❌ 錯誤：找不到指定的 BibTeX 檔案於 {bib_file_path}")
        return
        
    print(f"🧹 正在連線至 SQLite 資料庫: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 確保開啟 SQLite 外鍵約束
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 確保預設專案與主題存在，以防外鍵懸空
    try:
        cursor.execute("SELECT project_id FROM projects WHERE project_id = 'prj_general';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO projects (project_id, project_name, description, search_spec, architecture_spec, meta_data)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                "prj_general", "全域研究探勘專案", "匯總所有非特定專案的文獻移轉成果。",
                json.dumps({"keywords": ["general"]}, ensure_ascii=False),
                json.dumps({"target": "knowledge_expansion"}, ensure_ascii=False),
                json.dumps({"auto_created": True}, ensure_ascii=False)
            ))
            
        cursor.execute("SELECT topic_id FROM topics WHERE topic_id = 'top_general';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO topics (topic_id, project_id, topic_name, sequence_order, focus_spec, status, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                "top_general", "prj_general", "全域學術主題探底", 1,
                json.dumps({"focus_variables": ["general_knowledge"], "equations": []}, ensure_ascii=False),
                "ACTIVE", json.dumps({"auto_created": True}, ensure_ascii=False)
            ))
            
        cursor.execute("SELECT root_key FROM directory_roots WHERE root_key = 'zotero_storage';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO directory_roots (root_key, owner_type, owner_name, absolute_path, meta_data)
            VALUES (?, ?, ?, ?, ?);
            """, ("zotero_storage", "STUDENT_LOCAL", "wuulong", "/Users/wuulong/Zotero/storage/", json.dumps({"description": "研究生 Zotero 本地附件目錄"}, ensure_ascii=False)))
            
    except Exception as e:
        print(f"⚠️ 初始化預設約束表格時出錯: {e}")
        conn.close()
        return

    print(f"📖 正在解析 BibTeX 檔案: {bib_file_path}")
    with open(bib_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 分割每一篇 BibTeX Entry
    entries = re.findall(r'@\w+\{([^,]+),\s*(.*?)\n\}', content, re.DOTALL)
    
    print(f"📊 偵測到 {len(entries)} 筆 BibTeX 條目，開始進行主權入庫...")
    
    success_count = 0
    url_count = 0
    
    for cite_key, body in entries:
        # 正則表達式精準擷取 Title, Author, Year, Abstract 與 Attachment File
        title_match = re.search(r'title\s*=\s*[\{"\'](.*?)[\}"\']', body)
        author_match = re.search(r'author\s*=\s*[\{"\'](.*?)[\}"\']', body)
        year_match = re.search(r'year\s*=\s*[\{"\'](\d+)[\}"\']', body)
        abstract_match = re.search(r'abstract\s*=\s*[\{"\'](.*?)[\}"\']', body, re.DOTALL)
        file_match = re.search(r'file\s*=\s*[\{"\'](.*?)[\}"\']', body)
        
        title = title_match.group(1).replace('\n', ' ').strip() if title_match else "Untitled"
        authors = author_match.group(1).replace('\n', ' ').strip() if author_match else "Unknown"
        year = int(year_match.group(1)) if year_match else 2026
        abstract = abstract_match.group(1).replace('\n', ' ').strip() if abstract_match else ""
        
        paper_id = f"migrated_{cite_key.lower()}"
        
        # 1. 寫入 papers 表
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO papers (paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data)
            VALUES (?, 'task_init_sandbox_2026', 'top_general', ?, ?, ?, 'BibTeX 移轉匯入', ?, ?, ?);
            """, (
                paper_id, title, authors, year, cite_key, f"@{cite_key}, {body}",
                json.dumps({"abstract_snippet": abstract[:200] + "..."}, ensure_ascii=False)
            ))
            
            # 2. 若有 Zotero 本地附件，智慧抽離相對路徑並寫入 paper_urls
            if file_match:
                raw_path = file_match.group(1)
                # Zotero Better BibTeX 格式通常為 :path/to/file.pdf:PDF 或直接是路徑
                clean_path = raw_path.split(":")[-2] if ":" in raw_path else raw_path
                # 擷取 storage/ 下的相對結構，例: "ABCDE123/paper.pdf"
                zotero_part = re.search(r'storage/([^/]+/[^/]+\.pdf)', clean_path)
                
                if zotero_part:
                    relative_link = zotero_part.group(1)
                    cursor.execute("""
                    INSERT OR IGNORE INTO paper_urls (url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data)
                    VALUES (?, ?, 'zotero_storage', ?, 'local_pdf', 'DOWNLOADED', 102400, ?);
                    """, (
                        f"url_{paper_id}_local", paper_id, relative_link,
                        json.dumps({"migrated_attachment": True}, ensure_ascii=False)
                    ))
                    url_count += 1
            
            # 3. 自動打上 Ingestion 遷移標籤
            cursor.execute("""
            INSERT OR IGNORE INTO paper_tags (paper_id, tag_name, meta_data)
            VALUES (?, 'migrated-bibtex', ?);
            """, (paper_id, json.dumps({"source": os.path.basename(bib_file_path)}, ensure_ascii=False)))
            
            success_count += 1
        except Exception as e:
            print(f"⚠️ 匯入 {cite_key} 失敗: {e}")
            
    conn.commit()
    conn.close()
    
    print("\n----------------------------------------------------------------------")
    print(f"🎉 恭喜！Zotero BibTeX 大量遷移任務圓滿達成！")
    print(f"  - 成功匯入背景文獻: {success_count} 篇")
    print(f"  - 自動綁定相對 PDF 連結: {url_count} 筆")
    print("----------------------------------------------------------------------")

def main():
    parser = argparse.ArgumentParser(description="migrate_zotero_bib: 大量匯入 Zotero BibTeX 條目至主權資料庫")
    parser.add_argument("--bib", type=str, required=True, help="Zotero / Better BibTeX 產出的 .bib 檔案路徑")
    parser.add_argument("--db", type=str, help="指定目標 SQLite 資料庫路徑 (優先於環境變數 RESEARCH_DB)")
    
    args = parser.parse_args()
    
    db_path = args.db or os.environ.get("RESEARCH_DB") or DEFAULT_DB_PATH
    
    # 執行遷移
    migrate_bibtex_to_db(args.bib, db_path)

if __name__ == "__main__":
    main()
