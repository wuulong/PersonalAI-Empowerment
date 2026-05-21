# 🪐 主權篩選文獻回流 Zotero 實戰指引 (Zotero Feedback Guide)

> **核心思維**：
> 當您的 AI 代理人透過網路搜尋（如 `paper_scout.py`）在大海中撈取了上百篇文獻，並在您的「主權資料庫」中完成結構化分類、COMSOL 誤差對比與紅軍自審後 ──
> **您需要挑選出最精華的 3-5 篇，將它們回流推回 Zotero 中進行實體 PDF 的閱讀、畫線、與 Word/LaTeX 寫作排版。**

本指引手把手帶您實踐兩種最優雅、最安全的「文獻回流」工作流。

---

## 🗺️ 雙軌回流工作流對比

| 維度 | 🪄 方案一：魔術棒識別碼貼上法 | 📦 方案二：BibTeX 批次匯出匯入法 |
| :---: | :--- | :--- |
| **適用場景** | **快速挑選 1-3 篇**時，省去跑腳本的步驟。 | **大批次（如 5 篇以上）**一鍵回流與同步。 |
| **操作難度** | 極低（純手動複製貼上）。 | 低（執行一個極簡 CLI 指令）。 |
| **檔案處理** | **最強！** 由 Zotero App 原生自動從網上下載實體 PDF。| 標準！Zotero 建立文獻欄位，PDF 可後續點擊下載。 |
| **程式碼依賴** | 零。 | 僅需執行本機獨立 Python 腳本。 |

---

## 🪄 方案一：魔術棒識別碼貼上法 (Add by Identifier)

這是 Zotero Mac 版內建的最強神級功能，AI 代理人只需提供您「論文身分證（arXiv ID 或 DOI）」，其餘的網頁下載、實體 PDF 抓取全權交給 Zotero。

### 📌 操作三步驟：

#### 步驟 1：在主權資料庫中獲取選中論文的識別碼
在您的 DBeaver、SQLite CLI 或請您的 AI 助手，在主權庫中查詢您篩選好的論文識別碼。例如執行：
```sql
-- 抓取所有打上 'selected-for-zotero' 標籤的論文 cite_key (即 arXiv ID 或 DOI)
SELECT p.cite_key 
FROM papers p
JOIN paper_tags t ON p.paper_id = t.paper_id
WHERE t.tag_name = 'selected-for-zotero';
```
*   **輸出結果範例**：
    ```text
    arXiv:2007.03818
    arXiv:2009.05504
    ```

#### 步驟 2：在 Zotero App 中啟用魔術棒
1.  打開您的 **Zotero Mac 版**。
2.  在上方工具列中，點擊 **「Magic Wand (魔術棒，一個畫有加號的小棒子)」** 圖示（如下圖所示的位置）：
    ```text
    [New Item]  [Add Item by Identifier (魔術棒)]  [New Note]
                    └── 點擊此按鈕
    ```

#### 步驟 3：貼上並 Enter
1.  將步驟 1 產生的 ID 列表整串複製。
2.  直接貼進 Zotero 魔術棒彈出的輸入框中。
3.  **按下 Enter 鍵**。
4.  **🎉 奇蹟時刻**：Zotero 會立刻在背景聯網，自動為您抓取這幾篇論文的精準 Metadata、作者、發表年份，並**自動為您下載實體 PDF 檔案進行本地儲存與命名**！

---

## 📦 方案二：BibTeX 批次匯出匯入法 (Scripted Export)

當您在資料庫中篩選了大量論文（例如 10 篇），且希望保留您在 DB 中已經定錨好的 `cite_key` 時，這是最標準的學術移轉路線。

我們為此專門編寫了獨立的實體指令檔：**[export_selected_bib.py](export_selected_bib.py)**。

### 📌 操作四步驟：

#### 步驟 1：在資料庫中為心儀的論文打上回流標籤
在 DBeaver、SQLite CLI 中，執行以下 SQL 為挑選好的論文標記（以 `arxiv_2007_03818` 為例）：
```sql
INSERT INTO paper_tags (paper_id, tag_name) 
VALUES ('arxiv_2007_03818', 'selected-for-zotero');
```

#### 步驟 2：執行匯出腳本
在您的 terminal 中，執行我們為您準備好的腳本（預設會讀取您的 `RESEARCH_DB` 環境變數）：
```bash
python3 export_selected_bib.py --output my_selections.bib
```
*   **執行輸出**：
    ```text
    🧹 正在連線至主權資料庫: /Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db
    📊 偵測到 2 筆已標記的回流文獻。開始匯出...
    File saved to: my_selections.bib
    🧹 正在清除已匯出文獻的 'selected-for-zotero' 標籤...
    ✅ 標籤清理完成，下次匯出將不會重複計入。
    🎉 回流匯出任務順利完成！
    ```

#### 步驟 3：在 Zotero 中一鍵匯入
1.  打開 **Zotero Mac 版**。
2.  點擊頂部選單的 **「File」➔ 「Import...」**。
3.  選擇 **「A file (BibTeX, RIS, Zotero RDF, etc.)」**，點擊 Next。
4.  選擇剛剛產生的 **`my_selections.bib`** 檔案並開啟。
5.  勾選「Copy files to the Zotero storage folder」（將檔案複製到 Zotero 儲存資料夾），點擊 Next。
6.  **🎉 遷移完成**：Zotero 會瞬間在本地建立這幾篇論文的所有文獻欄位！

---

## 🤖 給研究生與 AI 夥伴的協同改寫節點

這份獨立的 **[export_selected_bib.py](export_selected_bib.py)** 腳本同樣遵循「零依賴、極致簡約」的原則。

當您未來有更高級的需求時，您可以直接將 `export_selected_bib.py` 上傳給您的 AI 程式設計助手（如 Gemini、Claude），並下達以下 Prompt 進行智慧改造：

> **💡 AI 改造 Prompt 範本：**
> *「這是我目前將篩選文獻匯出回 Zotero 的 Python 腳本。我現在希望 [改寫為直接調用本地 Zotero 的 HTTP API 一鍵推送 / 改寫為直接輸出 Notion 相容的 Markdown 格式 / 在匯出時自動附帶紅軍自審的 Verdict 評語寫入 BibTeX note 欄位]，請幫我修改這份腳本。」*
