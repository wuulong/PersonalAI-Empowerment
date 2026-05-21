#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪐 個人學術主權資料庫 - 主權篩選文獻回流 Zotero 匯出工具 (export_selected_bib.py)

【💡 研究生極客工作流】：
本腳本負責將研究生在主權 SQLite 資料庫中篩選、打上標籤的優良文獻，
整批自動匯出為標準的 BibTeX (.bib) 格式。
研究生隨後可在 Zotero 中一鍵匯入此檔案，自動完成實體 PDF 下載與 Zotero 入庫。

【🏷️ 標籤篩選機制】：
本腳本會自動查詢在 `paper_tags` 表格中，打上標籤為 'selected-for-zotero' 的所有論文。
"""

import os
import sqlite3
import argparse

DEFAULT_DB_PATH = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db"
DEFAULT_OUTPUT_BIB = "selected_papers.bib"

def export_selected_to_bib(db_path, output_path, keep_tags):
    if not os.path.exists(db_path):
        print(f"❌ 錯誤：找不到指定的 SQLite 資料庫於 {db_path}")
        return

    print(f"🧹 正在連線至主權資料庫: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查詢所有標記為 'selected-for-zotero' 的文獻
    query = """
    SELECT p.paper_id, p.cite_key, p.title, p.authors, p.year, p.bibtex
    FROM papers p
    JOIN paper_tags t ON p.paper_id = t.paper_id
    WHERE t.tag_name = 'selected-for-zotero';
    """
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        print(f"❌ 查詢失敗，請檢查資料庫結構與標籤表格: {e}")
        conn.close()
        return

    if not rows:
        print("\n📭 目前資料庫中沒有被標記為 'selected-for-zotero' 的論文。")
        print("💡 提示：您可以在 DBeaver 或 SQLite CLI 中，透過以下 SQL 命令為論文打上回流標籤：")
        print("   INSERT INTO paper_tags (paper_id, tag_name) VALUES ('您的論文ID', 'selected-for-zotero');\n")
        conn.close()
        return

    print(f"📊 偵測到 {len(rows)} 筆已標記的回流文獻。開始匯出...")

    bib_content = []
    exported_ids = []

    for paper_id, cite_key, title, authors, year, bibtex in rows:
        # 如果資料庫中有完整的 bibtex 欄位，直接使用
        if bibtex and bibtex.strip().startswith("@"):
            bib_content.append(bibtex.strip())
        else:
            # 如果沒有，則動態拼裝一個基本的 BibTeX Entry
            clean_authors = authors.replace(";", " and ")
            dynamic_bib = (
                f"@article{{{cite_key},\n"
                f"  title = {{{title}}},\n"
                f"  author = {{{clean_authors}}},\n"
                f"  year = {{{year}}},\n"
                f"  note = {{主權資料庫篩選回流}}\n"
                f"}}"
            )
            bib_content.append(dynamic_bib)
        
        exported_ids.append(paper_id)

    # 寫入指定的 .bib 檔案
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(bib_content))
        f.write("\n")

    print(f"💾 成功將 {len(rows)} 筆文獻匯出至: {output_path}")

    # 若使用者選擇清除標籤（預設為清除，避免重複匯出）
    if not keep_tags:
        print("🧹 正在清除已匯出文獻的 'selected-for-zotero' 標籤...")
        try:
            placeholders = ",".join(["?"] * len(exported_ids))
            cursor.execute(f"""
            DELETE FROM paper_tags 
            WHERE tag_name = 'selected-for-zotero' AND paper_id IN ({placeholders});
            """, exported_ids)
            conn.commit()
            print("✅ 標籤清理完成，下次匯出將不會重複計入。")
        except Exception as e:
            print(f"⚠️ 清除標籤時發生錯誤: {e}")
            conn.rollback()

    conn.close()
    print("🎉 回流匯出任務順利完成！")

def main():
    parser = argparse.ArgumentParser(description="export_selected_bib: 匯出主權資料庫篩選文獻至 Zotero 格式")
    parser.add_argument("--db", type=str, help="指定目標 SQLite 資料庫路徑 (優先於環境變數 RESEARCH_DB)")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_BIB, help="指定輸出的 .bib 檔案路徑")
    parser.add_argument("--keep-tags", action="store_true", help="保留已匯出文獻的標籤 (預設匯出後會自動清除標籤)")

    args = parser.parse_args()

    db_path = args.db or os.environ.get("RESEARCH_DB") or DEFAULT_DB_PATH
    export_selected_to_bib(db_path, args.output, args.keep_tags)

if __name__ == "__main__":
    main()
