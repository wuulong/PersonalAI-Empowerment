---
name: academic-research-navigator
description: 專注於新一代學術研究「硬核兵器庫」，支援線上文獻檢索、SQLite 結構化資料落庫、LaTeX 公式處理與紅軍自審評估。
---

# Academic Research Navigator Skill (學術研究導航員技能)

此技能專用於實體化「第一支柱：硬核研究兵器庫 (The Physical Stack)」，提供 Agentic AI 一套標準化、無摩擦的文獻自動化探勘、高擴展性結構化落庫與紅軍對抗自審指南。

---

## 1. 核心工具鏈與資源分佈 (Resource Stack)

*   **資料庫路徑**：`/Users/wuulong/github/bmad-pa/data/research/Research_Artifacts.db`
*   **文獻探勘腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/paper_scout.py`
*   **論文結構化萃取腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/parse_paper_to_db.py`
*   **資料庫初始化腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/setup_research_db.py`
*   **直連直呼規格書**：`/Users/wuulong/github/bmad-pa/scripts/research/paper_scout_cli_spec.md`

---

## 2. 核心操作指令與工作流 (CLI Commands)

### 📌 工作流 A：文獻探索與自動落庫 (Paper Scout & Ingestion)
當使用者要求搜尋特定物理主題或元件參數時，Agent **不應盲目猜測**，應直接透過命令行直呼 `paper_scout.py`：

```bash
python3 /Users/wuulong/github/bmad-pa/scripts/research/paper_scout.py --query "<關鍵字>" --limit <數量> --save-db
```

*   **沙盒降級處理**：若執行時遭遇網路連線阻礙（Timeout 或 429），腳本會自動退避至【離線模擬模式 (Offline Mock Mode)】產出高度自洽的 AR-WET 測試資料並完成落庫，Agent 應直接以此資料進行後續推理與 Grounding。
*   **成果彙報**：在對話中直接為使用者渲染出高品質的 Markdown 對照表，並提醒文獻已寫入 `Research_Artifacts.db`。

### 📌 工作流 B：非結構化 LaTeX 論文之紅軍自審落庫 (Adversarial Extraction)
當使用者提供 Marker CLI 轉出、包含複雜 LaTeX 電磁學/電路公式的 Markdown 論文時，Agent 應呼叫萃取程式進行語義高精結構化：

```bash
python3 /Users/wuulong/github/bmad-pa/scripts/research/parse_paper_to_db.py
```

*   **萃取維度**：
    1.  `core_method`：一句話的核心高維語義摘要。
    2.  `key_parameters` (JSON)：動態物理/電路特性參數。
    3.  `critique_score` (JSON)：紅軍對抗漏洞與評分（Reviewer 2 視角）。
    4.  `meta_data` (JSON)：數位基因封套（含 timestamp 與 agent_version）。

### 📌 工作流 C：學術真值庫唯讀分析 (Grounding & Analytics)
Agent 可以使用 SQL SELECT 指令直接對本地已落庫的文獻進行橫向比對，為使用者解答「哪一種方法能獲得最佳物理特性」：

```bash
sqlite3 /Users/wuulong/github/bmad-pa/data/research/Research_Artifacts.db "<唯讀 SELECT 語句>"
```

*   **安全限制**：**嚴禁**執行 `UPDATE`、`DELETE`、`DROP` 等寫入指令，僅允許執行 `SELECT` 唯讀查詢。
*   **JSON 函數查詢範例**：
    ```sql
    -- 橫向比對品質因子大於 10000 的論文標題與漏洞
    SELECT title, json_extract(critique_score, '$.vulnerabilities') FROM papers WHERE json_extract(key_parameters, '$.Q') > 10000;
    ```

---

## 3. 智力防線：如何防止學生「認知掏空」？
在執行本技能時，Agent 必須維持高度的**「指導者品位（Taste Guidance）」**：
1.  **不直接給出最終答案**：當學生詢問「這段推導怎麼寫」時，應引導學生查詢資料庫中的 `critique_score`，讓學生自己評估替代方案的缺點。
2.  **促成「品位裁決」面試準備**：每次落庫後，Agent 應主動向學生提問：「這篇論文的 key_parameters 在高功率下有 Duffing 分歧缺陷，如果我是指導教授，本週開會我會挑剔你這一點，你打算怎麼修正你的實驗設計？」
3.  **留下考古紀錄**：協助學生將高難度來回推導的對話，使用 `aiqa-scribe` 技能存入 `notes/ai-qa/`，作為教授「關卡一（考古日誌）」的審查憑證。
