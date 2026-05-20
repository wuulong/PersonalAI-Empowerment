# 14.2 硬核兵器庫：AR-WET 傳能研究的 SQLite 混合結構設計

主權革命的第一步，是建立「對數據與證據的絕對主權」。小明不再讓探勘成果隨意消散在瀏覽器的聊天紀錄中，而是要在本地 macOS 環境部署硬核工具鏈，並建立「實體真值資料庫」。

---

### A. 本地物理工具鏈配置

小明利用終端機配置了以下三層架構：
1.  **文獻解析層 (Marker CLI)**：利用 `marker_serve` 將學術 PDF 自動解析為完美的 LaTeX Markdown，保留了壓電應變張量與 Duffing 非線性分歧的物理公式結構，拒絕公式亂碼。
2.  **語意定錨層 (NotebookLM)**：建立 `AR-WET 專屬筆記本`，將本地 Zotero 的 50 篇關鍵文獻 LaTeX Markdown 上傳定錨，防止認知漂移。
3.  **結構化持久層 (SQLite `Research_Artifacts.db`)**：建立一個兼具關係型嚴謹度與 NoSQL 彈性的混血資料庫。

---

### B. 實體資料庫 Schema 設計與六大環節對位

這個在本地執行的 `Research_Artifacts.db` 資料庫，其 Schema 欄位是研究方法論的**「數位孿生體 (Digital Twin)」**：

```sql
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    core_method TEXT,
    key_parameters TEXT,     -- JSON 格式儲存：動態物理參數
    critique_score TEXT,     -- JSON 格式儲存：紅軍自審漏洞
    meta_data TEXT           -- JSON 格式儲存：向前相容信封 (數位基因)
);
```

#### 💡 欄位與六大環節實體映射證明：
*   **`core_method TEXT`（對齊環節 1：文獻回顧與問題定義）**：
    強迫小明將論文的流派核心摘要為極簡的高維語義（如：*Acoustic Wave Confinement*），用於 Gap Analysis 篩選。
*   **`key_parameters TEXT` (JSON)（對齊環節 4：數據分析與結果解讀）**：
    利用 JSON 彈性欄位，克服傳統欄位無法動態增刪的痛點。小明能自由將 $f_0$, $Q$, $IL$ 等物理參數以 JSON 寫入，並使用 SQLite 的 `json_extract()` 進行秒級跨論文參數橫向比對，展現「品位裁決」的定量依據：
    ```sql
    -- 查詢品質因子 (Q) 大於 10000 且 插入損耗 (IL) 小於 3dB 的文獻
    SELECT title FROM papers WHERE json_extract(key_parameters, '$.Q') > 10000;
    ```
*   **`critique_score TEXT` (JSON)（對齊環節 2：研究方法與假設擬定）**：
    強迫記錄 AI 與小明在「紅軍模式 (Red Teaming)」對抗推導中，抓出的論文致命物理漏洞（如：*「高功率下易引發壓電 Duffing 非線性分歧不穩定」*）。這在資料庫底層留下了「小明曾進行深度懷疑與推導對抗」的**實體真值證據**。
*   **`meta_data TEXT` (JSON)（對齊環節 3：資料蒐集與實驗執行）**：
    自動記錄採集時間、Agent 版本等數位基因。未來不用執行 `ALTER TABLE` 異動，即可隨時由 AI 寫入新型態屬性，保證系統的代際向前相容。
