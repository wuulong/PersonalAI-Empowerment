# 🪐 三層學術情報偵察引擎與 Zotero MCP 整合藍圖 (Academic Reconnaissance Engine Blueprint)

> **前言**：學術研究不是孤立的「文獻檢索」，而是一場對人類知識邊界的「主權偵察」。本藍圖旨在將極簡的 `paper_scout.py` 工具，升級為一套具備**「語義校準、物理抽取、雙核共生、圖譜追蹤」的重型學術情報偵察母艦**。

---

## 🗺️ 一、 系統架構：雙核共生與三層偵察模型

我們採用 **「Zotero (物理感官) ＋ 主權 SQLite 資料庫 (思想靈魂)」** 的雙核並行架構。

```mermaid
graph TD
    subgraph 🟢 第一層：廣度網羅與多源 Ingestion (Harvester)
        A1[arXiv API] --> |預印本捕捉| H[多源情報調適器 Harvester]
        A2[Semantic Scholar API] --> |引用數與正式期刊| H
        A3[OpenAlex / Crossref API] --> |DOI 補全與 Nature/IEEE 正式中繼資料| H
        A4[Zotero MCP Server] --> |本地文獻庫即時監控與雙向同步| H
    end

    subgraph 🟡 第二層：語義對齊與知識沉澱 (Seeding)
        H --> B1[AI 語義校準與品質篩選]
        B1 --> B2[AI 自動物理變數/公式抽取]
        B1 --> B3[依據專案與 Topic 契約自動分類]
        B1 --> B4[相對根路徑映射與實體解耦]
    end

    subgraph 🔴 第三層：引用圖譜與有向演化追蹤 (Tracer)
        B2 & B3 & B4 --> C[(三層十表 SQLite 主權資料庫)]
        C --> D1[溯源分析: Backward Citations]
        C --> D2[演化追蹤: Forward Citations]
        C --> D3[紅軍 Agent 攻防與師徒治理]
    end
```

---

## 📡 二、 Zotero MCP Server 整合計畫

Zotero 是人類肉身收集文獻的黃金感官，而 **Model Context Protocol (MCP)** 則是 AI 代理人直接操控此感官的橋樑。引入 Zotero MCP Server 是將兩者融為一體的關鍵核心。

### 1. Zotero MCP Server 的運作機制
AI 代理人透過本機連線協定，直連 Zotero 本地 SQLite 或 Web API，具備以下主動操控能力：

*   `get_zotero_items`：允許 AI 代理人讀取研究生在 Zotero 中手動收集的文獻與高亮筆記。
*   `add_zotero_item`：當 AI 代理人線上探勘到極佳背景文獻時，**主動調用此 Tool 操控 Zotero 下載 PDF 並歸檔**。
*   `update_zotero_tags`：依據 AI 代理人在主權資料庫中對論文進行的「紅軍自審結果」，同步將評級（如 `Pass-Critique`）寫回 Zotero 做為視覺化標籤。

### 2. 雙核同步流程 (Sovereign Symbiosis Loop)
```
[ 研究生於瀏覽器看到論文 ] 
       │ (點擊 Zotero 收集按鈕)
       ▼
[ Zotero 下載實體 PDF & 解析中繼資料 ] 
       │ (觸發 Better BibTeX 自動同步)
       ▼
[ Zotero MCP / .bib 檔案更新 ] 
       │ (AI 代理人偵測到新事件)
       ▼
[ AI 自動讀取新文獻，執行「語義校準」與「變數抽取」 ]
       │ (判斷 Topic 歸屬與 COMSOL 模擬邊界)
       ▼
[ 沉澱寫入三層十表 SQLite 主權資料庫 ]
```

---

## 🟢 三、 第一層：多源網羅 (Multi-source Harvester) 規劃

我們必須超越單一的 arXiv 檢索，建構一個多層次的學術情報調適器：

1.  **arXiv 調適器**：保持現有的零依賴 XML 解析器，確保極速獲取最新的物理、電腦科學預印本。
2.  **Semantic Scholar 調適器**：
    *   **對接 API**：`https://api.semanticscholar.org/graph/v1/paper/search`
    *   **情報補強**：拉取文獻的 `citationCount` (總引用數)、`influentialCitationCount` (高影響力引用數) 寫入 `papers.meta_data`。
3.  **OpenAlex / Crossref 調適器**：
    *   當文獻有正式出版的 DOI 時，自動反查 OpenAlex，獲取其在 **Nature、Science、IEEE、Elsevier** 等頂級期刊的權威中繼資料，自動更新作者單位、出版期刊、卷期資訊。

---

## 🟡 四、 第二層：語義對齊與知識沉澱 (Seeding) 規劃

新論文進入資料庫前，必須經過 **「AI 思想篩選閘口」**：

1.  **專案契約與主題對位**：
    *   AI 代理人讀取新文獻的 `abstract`。
    *   比對資料庫 `projects.search_spec` 的關鍵詞契約與目標。
    *   自動將該論文的外鍵歸類至最吻合的 `topic_id`（若無吻合，則歸入 `top_general`）。
2.  **物理變數與公式抽取 (Automatic Spec Extraction)**：
    *   利用 LLM 結構化抽取論文中提及的關鍵性能指標（例如：*「本研究達成 1.2Mhz 的工作頻率，以及壓電電壓 5V」*）。
    *   自動將這些變數抽離為 `{"voltage_V": 5.0, "frequency_MHz": 1.2}` 的 JSON 結構，寫入 `papers.meta_data`，為後續與 COMSOL 模擬數據進行 Discrepancy 對比提供 Baseline。
3.  **路徑相對化與隔離**：
    *   自動解析 Zotero 的絕對附件路徑，自動將其剝離為 `zotero_storage` 的相對 root_key 映射，防範未來主機遷移時 PDF 路徑斷線。

---

## 🔴 五、 第三層：引用圖譜與有向演化 (Tracer) 規劃

這是有深度學術主權的最硬核展現，旨在「看清知識的演化脈絡」：

### 1. 溯源分析 (Backward Citation Graph)
*   **作法**：當系統匯入一篇「里程碑論文（Milestone Paper）」時，AI 代理人自動透過 Semantic Scholar API 查詢其 `references` (前置引用文獻)。
*   **目的**：自動將該領域最經典、最不可繞過的「奠基石論文」也一併拉入資料庫，自動繪製文獻的「歷史根系」。

### 2. 演化追蹤 (Forward Citation Graph)
*   **作法**：部署一個背景輕量守護行程 (Daemon)，每週或每月自動透過 API 掃描您收藏的論文列表。
*   **目的**：當您關注的某篇背景論文被 2027 年的 Nature 或 IEEE 期刊新論文引用時，主動在資料庫中建立一條有向引用線，自動跳出通知：*「哈爸，您關注的 AR-WET 壓電非線性論文，已被麻省理工團隊最新的壓電晶片論文所引用，已自動將其入庫並關聯至 Topic 2！」*

---

## 📅 六、 四階段落地實施路線圖 (Roadmap)

| 階段 | 核心任務 | 技術要點 | 交付成果 |
| :---: | :--- | :--- | :--- |
| **Phase 1** | **雙核直連與 MCP 部署** | 部署本地 Zotero MCP Server，打通 `migrate_zotero_bib.py` 指令。 | 達成本地 Zotero 新收錄文獻，秒級自動同步投影至主權 DB 的 10 表結構中。 |
| **Phase 2** | **重型學術 API 調適器** | 對接 Semantic Scholar API，改寫 `paper_scout.py`。 | 支援從 arXiv 跨越至 IEEE/Nature 全期刊文獻搜尋，並自動沉澱引用次數與影響力中繼資料。 |
| **Phase 3** | **AI 語義校準與變數抽取** | 整合 LLM Function Call，實作摘要語義比對與邊界變數 JSON 自動生成。 | 新文獻入庫時，自動與 `topics.focus_spec` 對位，並自動提取出數值 Baseline。 |
| **Phase 4** | **引用圖譜有向演化監控** | 實作 Backward/Forward 溯源追蹤腳本，並寫入 `manuscript_citations` 表格。 | 建立自動化學術雷達，當有後續演化文獻引用您的收藏時，自動拉出脈絡圖譜。 |
