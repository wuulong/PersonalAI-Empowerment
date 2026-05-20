# 14.2 硬核兵器庫：AR-WET 傳能研究的 SQLite 混合結構設計

主權革命的第一步，是建立「對資料與證據的絕對主權」。小明不再讓探勘成果隨意消散在瀏覽器的聊天紀錄中，而是要在本地 macOS 環境部署硬核工具鏈，並建立「實體真值資料庫」。

---

### A. 本地物理工具鏈配置

小明利用終端機配置了以下三層架構：
1.  **文獻解析層 (Marker CLI)**：利用 `marker_serve` 將學術 PDF 自動解析為完美的 LaTeX Markdown，保留了壓電應變張量與 Duffing 非線性分歧的物理公式結構，拒絕公式亂碼。
2.  **語意定錨層 (NotebookLM)**：建立 `AR-WET 專屬筆記本`，將本地 Zotero 的 50 篇關鍵文獻 LaTeX Markdown 上傳定錨，防止認知漂移。
3.  **結構化持久層 (SQLite `Research_Artifacts.db`)**：建立一個兼具關係型嚴謹度與 NoSQL 彈性的混血資料庫。

---

### B. 實體資料庫 Schema 設計與六大環節對位

這個在本地執行的 `Research_Artifacts.db` 資料庫，其 Schema 欄位是小明研究方法論的**「數位孿生體 (Digital Twin)」**。它不再是簡單的文獻堆疊，而是將**「他者背景理論 (Grounding)」**、**「肉身本地實驗 (Execution)」**、**「認知紅軍防禦 (Critique)」**與**「主權手稿演化 (Evolution)」**進行強烈關聯的立體星系。

在三層聯邦主權架構下，資料庫被解耦為十個關係緊密的實體表：

```sql
-- 1. 探採任務表：記錄每一次 Ingestion 探針的數位血統
CREATE TABLE IF NOT EXISTS exploration_tasks (
    task_id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    papers_found INTEGER
);

-- 2. 專案領域主表：宣告研究生個人的學術疆域與目標規格定錨
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    search_spec TEXT NOT NULL,         -- JSON 探勘關鍵字契約
    architecture_spec TEXT             -- JSON 專案基準物理目標常數
);

-- 3. 循序研究主題表：劃分循序漸進的主題時序 (邏輯脊椎)
CREATE TABLE IF NOT EXISTS topics (
    topic_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    topic_name TEXT NOT NULL,
    sequence_order INTEGER NOT NULL,   -- 邏輯演進順序 (1, 2, 3...)
    focus_spec TEXT NOT NULL,          -- JSON 聚焦公式與焦點物理變數
    status TEXT NOT NULL,              -- PLANNED | ACTIVE | COMPLETED
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- 4. 根目錄實體映射表：隔離 Zotero、實驗室 NAS 的絕對路徑衝突，確保資料庫 100% 跨電腦移植
CREATE TABLE IF NOT EXISTS directory_roots (
    root_key TEXT PRIMARY KEY,          -- 抽象鍵 (如 'zotero_storage' | 'lab_nas')
    owner_type TEXT NOT NULL,           -- STUDENT_LOCAL | LAB_SHARED
    absolute_path TEXT NOT NULL         -- 當前機器實體絕對路徑 (如 '/Users/wuulong/...')
);

-- 5. 背景文獻主表：學術引用一等公民，固化 BibTeX 與 Cite Key
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    task_id TEXT,
    topic_id TEXT,
    title TEXT NOT NULL,
    cite_key TEXT UNIQUE NOT NULL,     -- LaTeX 引用鍵 (如 'Seong2026ARWET')
    bibtex TEXT NOT NULL,              -- 完整的 BibTeX 條目字串
    meta_data TEXT,                    -- JSON 存放文獻理論物理常數 {"theoretical_Q": 12000}
    FOREIGN KEY (task_id) REFERENCES exploration_tasks(task_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

-- 6. 多重資源映射表：解耦實體檔案路徑，實現「抽象 Root Key + 相對路徑」儲存
CREATE TABLE IF NOT EXISTS paper_urls (
    url_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    root_key TEXT NOT NULL,            -- 指向 directory_roots 抽象外鍵
    url_link TEXT NOT NULL,            -- 相對路徑 (如 'ARWET_2026.pdf')
    url_type TEXT NOT NULL,            -- local_pdf | arxiv_pdf | publisher
    download_status TEXT,              -- PENDING | DOWNLOADED
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (root_key) REFERENCES directory_roots(root_key)
);

-- 7. 本地模擬實測表：固化研究生肉身實踐的物理數值，與文獻理論精準對照
CREATE TABLE IF NOT EXISTS local_simulations (
    sim_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    run_config TEXT NOT NULL,          -- JSON 本次模擬輸入參數 {"drive_voltage": 5.0}
    empirical_results TEXT,            -- JSON 本地實測結果 {"measured_Q": 11800}
    discrepancy_percentage REAL,       -- 【主權比對指標】本地與文獻理論誤差百分比
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);

-- 8. 紅軍自審對抗表：記錄師徒或 Agent 自審防禦軌跡，行使「品位裁決」的鐵證
CREATE TABLE IF NOT EXISTS red_team_logs (
    log_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    aspect_analyzed TEXT,              -- 分析物理維度 (如 'Duffing Non-linear')
    reviewer_attack TEXT,              -- 紅軍 Agent (尖銳物理質疑)
    student_defense TEXT,              -- 研究生 (主動防禦公式與設計規避)
    verdict TEXT NOT NULL,             -- 裁決判定：PASS | VULNERABLE
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);

-- 9. 主權手稿有向演化表：記錄論文寫作的基因繼承，手稿不再是孤島
CREATE TABLE IF NOT EXISTS my_manuscripts (
    manuscript_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,
    cite_key TEXT UNIQUE,              -- 本手稿預計引用鍵
    manuscript_type TEXT NOT NULL,     -- Conference | Journal | Thesis
    evolution_stage TEXT NOT NULL,     -- Planning | Writing | Published
    previous_manuscript_id TEXT,       -- 遞迴外鍵：指向上一篇前導手稿 (心智基因鏈)
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
    FOREIGN KEY (previous_manuscript_id) REFERENCES my_manuscripts(manuscript_id)
);

-- 10. 手稿引用脈絡表：記錄「我為什麼要在我的這篇草稿中引用這篇背景文獻」
CREATE TABLE IF NOT EXISTS manuscript_citations (
    manuscript_id TEXT NOT NULL,
    paper_id TEXT NOT NULL,
    citation_context TEXT,             -- 引用心智脈絡 (例如 '作為品質因子實測對比')
    PRIMARY KEY (manuscript_id, paper_id),
    FOREIGN KEY (manuscript_id) REFERENCES my_manuscripts(manuscript_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
```

#### 💡 欄位與研究環節的立體映射證明：
*   **`projects` 與 `topics`（對齊環節：文獻回顧與問題定義）**：
    小明不再是被動地讀論文，而是首先在 `projects` 定義其核心目標頻率（如 `28.5 MHz`），並在 `topics` 設定 sequence_order，強制規劃從「物理建模」到「Duffing補償」的循序推進。這構成了小明的戰略定錨。
*   **`local_simulations.discrepancy_percentage`（對齊環節：資料蒐集與實驗執行）**：
    當小明完成本地 COMSOL 模擬後，直接與 `papers` 儲存的文獻理論值進行 SQL `JOIN` 比對。例如小明發現當激勵電壓提升至 12V 時，本地 Q 值與理論值偏離高達 `23.47%`。**這個誤差，就是發現 Duffing 非線性分歧的起點，也是科學研究最硬核的含金量**。
*   **`red_team_logs`（對齊環節：研究假設擬定與自審）**：
    強制記錄 AI 審稿人對此誤差發動的尖銳物理質疑，與小明主動設計「相位鎖定電路（PLL）與電壓避退機制」的防禦過程。這行使了高品位的物理裁決，保留了思維並未被 AI 掏空的鐵證。
*   **`my_manuscripts`（對齊環節：手稿撰寫與演化傳承）**：
    透過 `previous_manuscript_id` 自關聯，記錄自己的會議論文是如何一步步演化出期刊論文。手稿不再是孤島，而是承載了前人與自我心智基因的演化鏈。
*   **`paper_urls` 與 `directory_roots`（對齊環節：學術資產繼承）**：
    藉由剝除實體絕對路徑，使資料庫具備完美跨電腦可移植性，保障實驗室共享 NAS 資產的永續可用。

