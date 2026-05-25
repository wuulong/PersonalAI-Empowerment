-- ==============================================================================
-- 《個人AI賦能》v1.2.2 學術研究兵器庫 - 實體資料庫結構定義檔 (schema.sql)
-- 
-- 戰略設計：三層聯邦主權星系架構 (3-Tier Sovereign Knowledge Schema)
-- 本 Schema 將「他者背景文獻（他山之石）」、「本地實測與紅軍自審（肉身實踐）」與
-- 「主權研究手稿有向演化鏈（自我創造）」徹底融會對齊，是新一代 Agentic AI 方法論的數位孿生體。
-- 
-- 升級亮點：引進「抽象根目錄映射系統 (Abstract Directory Roots System)」，
-- 徹底隔離個人本地 Mac 與研究室共用 NAS 的絕對實體路徑，保證 100% 跨裝置移植與協同分享！
-- ==============================================================================

PRAGMA foreign_keys = ON; -- 強制啟用 SQLite 外鍵約束，確保參照完整性

-- ==============================================================================
-- 【第一層：探勘與血統任務層 (Ingestion & Lineage)】
-- 目的：追溯所有外部數據進入資料庫的「數位基因與血統」，保障學術數據之來源可信任性。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：exploration_tasks (探勘與採集任務日誌表)
-- 目的：記錄每一次執行 `paper_scout.py` 的探針軌跡。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exploration_tasks (
    task_id TEXT PRIMARY KEY,
    query TEXT NOT NULL,                  -- 本次探勘的原始關鍵字查詢
    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 任務啟動時間戳記
    status TEXT NOT NULL,                 -- 任務狀態：'ONLINE' (線上直連) 或 'OFFLINE_FALLBACK' (離線模擬避退)
    papers_found INTEGER,                 -- 本次探勘成功捕獲並入庫的文獻數量
    agent_version TEXT,                   -- 執行此任務的 Agent 核心版本 (Lineage 追溯)
    error_log TEXT,                       -- 若有報錯，記錄詳細 Error Stack 以供 Agent 自行熱修復
    meta_data TEXT                        -- JSON 信封：{"host_os": "macOS", "cli_flags": ["--save-db"]}
);


-- ==============================================================================
-- 【第二層：主權專案與有向演化路線圖層 (Sovereign Project & Topic Roadmap)】
-- 目的：宣告研究生的領土主權，將大領域劃分為具備「時間向量與邏輯相依性」的有向演化路徑。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：projects (研究專案/領域主表)
-- 目的：定義博士生或研究團隊的核心研究疆域，作為全局架構的最高定錨點。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,           -- 專案名稱 (例如 'AR-WET 生醫植入式無線傳能系統')
    description TEXT,                     -- 專案宏觀願景與學術意圖描述
    
    -- 📡 【探勘契約 JSON】：記錄本專案與 Agent 之間持續搜尋論文的自動化查詢契約
    -- 欄位用途：Agent 讀取此欄位即可自主發動 Ingestion，不需學生重複下 Prompt。
    -- 格式範例：{"keywords": ["AR-WET", "acoustic-resonant"], "exclude": ["electromagnetic"], "min_year": 2018}
    search_spec TEXT NOT NULL, 
    
    -- 🏗️ 【物理架構脈絡 JSON】：定義本專案的基礎物理常數、目標規格與系統硬性限制
    -- 欄位用途：做為本地實測數據比對的 Baseline，判斷是否達成「專案目標規格」。
    -- 格式範例：{"target_freq_MHz": 25.0, "max_depth_mm": 10.0, "allowed_temp_rise_C": 2.0}
    architecture_spec TEXT, 
    
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT                        -- JSON 信封：預留向前相容的詮釋資料空間
);

-- ------------------------------------------------------------------------------
-- 資料表：topics (循序研究主題表)
-- 目的：將大專案劃分為「循序推進」的子主題，作為演進的「邏輯脊椎」。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS topics (
    topic_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    topic_name TEXT NOT NULL,             -- 主題名稱 (例如 '非線性 Duffing 分歧之匹配電路補償')
    
    -- 🔢 【邏輯演進順序】：標記此主題在專案中的邏輯相依次序 (如 1, 2, 3)
    -- 欄位用途：
    --   1. 自動上下文繼承：當 seq = 2 啟動時，Agent 自動載入所有 seq < 2 的研究真值作為 Baseline。
    --   2. 定位施工現場：系統能精確辨識目前處於哪一個 active 戰場，防止認知過載。
    sequence_order INTEGER NOT NULL, 
    
    -- 🎯 【聚焦研判 JSON】：記錄本主題特有的焦點物理變數、核心公式與自動打標標籤
    -- 欄位用途：指引紅軍對抗 Agent 針對特定公式（如 Duffing）發動精確的自審攻擊。
    -- 格式範例：{"focus_variables": ["Q_factor", "bifurcation_threshold"], "equations": ["Duffing_equation"]}
    focus_spec TEXT NOT NULL, 
    
    status TEXT NOT NULL,                 -- 當前狀態：'PLANNED' (規劃中) | 'ACTIVE' (施工中) | 'COMPLETED' (已完成)
    meta_data TEXT,                       -- JSON 信封：擴展詮釋資料
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


-- ==============================================================================
-- 【第三層：環境定錨與抽象路徑層 (Environment Roots & Mapping)】
-- 目的：將物理實體路徑抽象化，徹底隔離「個人本地環境」與「研究室共享環境」的移植衝突。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：directory_roots (目錄實體映射配置表)
-- 目的：定義在當前執行環境下，各個抽象根目錄鍵 (Root Key) 對應的實際絕對路徑。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS directory_roots (
    root_key TEXT PRIMARY KEY,            -- 抽象根目錄鍵 (例如 'zotero_storage' | 'lab_nas' | 'workspace_root')
    owner_type TEXT NOT NULL,             -- 擁有者類型：'STUDENT_LOCAL' (研究生個人) | 'LAB_SHARED' (研究室公用)
    owner_name TEXT NOT NULL,             -- 擁有者名稱 (例如 研究生姓名 'wuulong' 或實驗室代號 'vres_lab')
    absolute_path TEXT NOT NULL,          -- 實體運作環境下的絕對路徑 (例如 '/Users/wuulong/Zotero/storage/')
    meta_data TEXT                        -- JSON 信封：{"mount_protocol": "smb", "os_compatibility": "macOS"}
);


-- ==============================================================================
-- 【第四層：結構化文獻定錨層 (Structured Literature Grounding)】
-- 目的：存放嚴謹的第三方背景文獻，並建立強大的「多維標籤系統」與「LaTeX 引用直達車」。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：papers (背景文獻主表)
-- 目的：存儲高質量的外部文獻，作為知識定錨的基石。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    task_id TEXT,                         -- 關聯至探勘任務，追溯此數據的採集血統
    topic_id TEXT,                        -- 關聯至特定的子主題，理清文獻的邏輯定位
    title TEXT NOT NULL,                  -- 論文標題
    authors TEXT,                         -- 作者清單 (文字格式，適合檢索)
    year INTEGER,                         -- 發表年份
    core_method TEXT,                     -- 核心方法摘要 (如：高維度語義摘要)
    
    -- ✍️ 【學術引用一等公民欄位】：與 LaTeX / Overleaf 100% 對齊的引用機制
    -- 欄位用途：寫論文時，Agent 可秒級導出所有已引用的 BibTeX，拼裝成完美的 references.bib。
    cite_key TEXT UNIQUE NOT NULL,        -- LaTeX 引用鍵 (例如 'Wang2026ARWET')
    bibtex TEXT NOT NULL,                 -- 原始完整的 BibTeX 條目字串
    
    meta_data TEXT,                       -- JSON 信封：存放動態物理參數 {"Q": 12000, "freq_MHz": 28.5}
    FOREIGN KEY (task_id) REFERENCES exploration_tasks(task_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_relations (背景文獻交叉關係演化表 - v1.2.2)
-- 目的：追溯文獻之間的繼承與批判關係，支援 SQL 自動生成學術演化譜系圖。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_relations (
    relation_id TEXT PRIMARY KEY,
    source_paper_id TEXT NOT NULL,       -- 起點文獻 (新文獻)
    target_paper_id TEXT NOT NULL,       -- 目標文獻 (被繼承或被批判之舊文獻)
    relation_type TEXT NOT NULL,         -- 關係類型：'IMPROVES' (改進) | 'REFUTES' (反駁) | 'GROUNDED_ON' (基於)
    description TEXT,                    -- 關係心智描述
    FOREIGN KEY (source_paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (target_paper_id) REFERENCES papers(paper_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_urls (文獻多重資源關聯表 - B方案實體抽象版)
-- 目的：支援單篇文獻掛載多重資源（官方網頁、ArXiv、本地 PDF 等）。
-- 
-- 💡 【核心演化】：此表格不直接存放實體路徑，而是存放「相對路徑（url_link）」並外鍵關聯
-- 至「目錄實體映射表（directory_roots）」，一舉解決資料庫跨電腦移植時路徑斷線的噩夢！
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_urls (
    url_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    
    -- 🔑 【抽象根目錄外鍵】：強烈參照至 directory_roots 表格，實現路徑的抽象化定錨
    root_key TEXT NOT NULL,               
    
    -- 📂 【相對路徑】：相對於該 root_key 所指向之實體絕對路徑的相對位址 (例如 'ABCDE123/paper.pdf')
    url_link TEXT NOT NULL,               
    
    url_type TEXT NOT NULL,               -- 資源類型：'publisher' (官方) | 'arxiv_pdf' (預印) | 'local_pdf' (本地) | 'code_repo'
    download_status TEXT,                 -- 下載狀態：'PENDING' | 'DOWNLOADED' | 'FAILED'
    file_size_bytes INTEGER,              -- 本地實體檔案大小，用於檢驗文件完整性
    meta_data TEXT,                       -- JSON 信封：{"download_retry_count": 0, "http_status": 200}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (root_key) REFERENCES directory_roots(root_key)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_tags (文獻多維關聯式標籤表)
-- 目的：克服分類單一性的缺陷，為文獻打上多維度標籤，實現超高效的交叉檢索。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id TEXT NOT NULL,
    tag_name TEXT NOT NULL,               -- 標籤名稱 (例如 'piezoelectric', 'non-linear', 'biomedical')
    meta_data TEXT,                       -- JSON 信封
    PRIMARY KEY (paper_id, tag_name),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
CREATE INDEX IF NOT EXISTS idx_tags_name ON paper_tags(tag_name); -- 加速標籤查詢


-- ==============================================================================
-- 【第五層：實體執行與紅軍對抗層 (Execution, Synthesis & Red Teaming)】
-- 目的：將文獻理論與「學生的肉身實踐（模擬/量測）」以及「心智對抗過程」徹底對齊。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：local_simulations (本地模擬與實測數據表)
-- 目的：記錄學生針對該論文理論所做的 N 次本地實驗，作為「現地真理（Ground Truth）」比對。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS local_simulations (
    sim_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    
    -- 🛠️ 【實驗/模擬設定 JSON】：記錄本次模擬的輸入物理變數與邊界條件
    -- 格式範例：{"f0_MHz": 25, "input_voltage": 5.0, "piezo_material": "PZT-5H"}
    run_config TEXT NOT NULL, 
    
    -- 📊 【實測/模擬波形結果 JSON】：記錄本地跑出來的關鍵物理輸出
    -- 格式範例：{"measured_Q": 11800, "measured_IL_dB": 2.8}
    empirical_results TEXT, 
    discrepancy_percentage REAL,          -- 【主權比對指標】：本地實測與文獻理論之間的誤差百分比 (如 1.67%)
    artifact_visual_path TEXT,            -- 【主權多模態】實測波形圖/熱分佈圖相對路徑 (v1.2.2)
    sim_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT,                       -- JSON 信封：{"simulation_platform": "COMSOL_v6.2", "host": "Habars_Mac Studio"}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：red_team_logs (紅軍自審與品位裁決日誌表)
-- 目的：記錄學生與紅軍 Agent 對抗自審的螺旋演化軌跡，做為「品位裁決」的實體證據。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS red_team_logs (
    log_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    manuscript_id TEXT,                   -- 關聯至手稿，直接對研究生自己的論文設計發動對抗 (v1.2.2)
    aspect_analyzed TEXT,                 -- 本次對抗的分析維度 (例如 'Duffing Non-linear Bifurcation')
    reviewer_attack TEXT,                 -- 紅軍 Agent (扮演嚴厲審稿人) 提出的尖銳物理質疑
    student_defense TEXT,                 -- 學生做出「品位裁決」後的防禦策略、修正公式與推導
    verdict TEXT NOT NULL,                -- 裁決判定：'PASS' (通過) | 'VULNERABLE' (脆弱) | 'CRITICAL_BUG' (嚴重錯誤)
    test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT,                       -- JSON 信封：{"judge_model": "Gemini_3.0_Pro", "tokens_used": 1540}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (manuscript_id) REFERENCES my_manuscripts(manuscript_id)
);


-- ==============================================================================
-- 【第六層：主權手稿有向演化層 (Sovereign Manuscript Evolution Chain)】
-- 目的：記錄研究生「自我創造」的成果演化。自己的論文不再是孤島，而是承載了前人基因的演化鏈。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：my_manuscripts (主權手稿表)
-- 目的：記錄自己正在撰寫、修改或已發表的系列論文（繼承演化鏈）。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS my_manuscripts (
    manuscript_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,                  -- 手稿標題
    cite_key TEXT UNIQUE,                 -- 本篇手稿預計的 Citation Key (如 'Wang2026_Ch1_Draft')
    manuscript_type TEXT NOT NULL,         -- 手稿類型：'Conference' | 'Journal' | 'Thesis' (論文)
    evolution_stage TEXT NOT NULL,        -- 演化階段：'Planning' | 'Writing' | 'Under_Review' | 'Published'
    
    -- 🧬 【手稿演化外鍵】：指向上一篇前導研究手稿，建立「心智基因繼承鏈」
    -- 欄位用途：讓 Agent 與指導教授清晰理清整套畢業論文的研究脈絡傳承。
    previous_manuscript_id TEXT, 
    
    meta_data TEXT,                       -- JSON 信封：存放寫作專案網址 {"overleaf_url": "https://overleaf.com/123456"}
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
    FOREIGN KEY (previous_manuscript_id) REFERENCES my_manuscripts(manuscript_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：manuscript_citations (主權手稿引用關聯表)
-- 目的：精確理清我的論文與他人背景文獻之間的「引用脈絡」。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS manuscript_citations (
    manuscript_id TEXT NOT NULL,          -- 我的手稿 ID
    paper_id TEXT NOT NULL,               -- 被引用的背景論文 ID
    
    -- 🧠 【引用心智脈絡】：記錄「我為什麼要在我的這篇草稿中引用這篇背景文獻」
    -- 欄位用途：寫論文時，Agent 可依據此欄位自動產出極具說服力的文獻綜述（Literature Review）。
    -- 格式範例：'作為品質因子 Q 值實測 Baseline 的對比依據'
    citation_context TEXT, 
    
    meta_data TEXT,                       -- JSON 信封
    PRIMARY KEY (manuscript_id, paper_id),
    FOREIGN KEY (manuscript_id) REFERENCES my_manuscripts(manuscript_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
