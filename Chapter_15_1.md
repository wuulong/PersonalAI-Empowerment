# 15.1 實戰現場：主權 AI 協作研究方法論論文（ms_sovereign_research_2026）的產製歷程

在真實的學術寫作現場，我們摒棄了傳統「打開 Word 盲目敲字」的低效做法，而是正式將這篇論文 `ms_sovereign_research_2026` 註冊為本地 SQLite 大腦中的一個實體節點，啟動了一套具備嚴密物理定錨的學術生產工序。

---

### A. 第一步：大腦註冊與 ToC 意圖定錨

首先，我們在 `my_manuscripts` 表中正式寫入這篇手稿的規格常數。這不是虛擬的描述，而是一次物理性定錨：
```sql
INSERT INTO my_manuscripts (manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage)
VALUES (
    'ms_sovereign_research_2026', 
    'top_sovereign_methodology', 
    'AI 時代的學術革命：基於本地主權大腦、品位裁決與遞迴重構的人機協作研究方法論', 
    'ms_sovereign_research_2026', 
    'Journal', 
    'Writing'
);
```

隨後，我們與大腦進行蘇格拉底式答辯，梳理出論文的核心靈魂，將其固化為帶有「寫作意圖」與「實體地基」的 ToC 兩層目錄（`sovereign_research_paper_toc.md`）。在每一節的 ToC 規劃中，我們強行定義了 `[寫作意圖]` 與 `[實體地基]`。例如：
*   **3.2 肉身實踐與真值定錨**
    *   `[寫作意圖]`：闡述 `empirical_evidences` 與 `friction_percentage` 對防範 AI 虛假幻想的科學作用。
    *   `[實體地基]`：曾文溪流域水文實測誤差（`12.5%`）的本地模擬數據。

這種「意圖驅動」的框架定錨，防止了 AI 在後續協作中用空洞的學術八股掏空論文的靈魂。

---

### B. 第二步：論文論點溯源與邏輯辯證地圖 (APM) 的建立

為了解決學術界論文背景引用「裝飾化」與「黑箱化」的痛點，我們在編寫初稿前，實體建立了 [sovereign_research_06_argument_map.md](https://github.com/wuulong/sovereign-research-methodology/blob/main/manuscripts/sovereign_research/sovereign_research_06_argument_map.md)（簡稱 APM 地圖）。

我們為這篇論文宣告了 12 個核心科學主張（Claims），並明確標註了其引用硬度等級（🔴 `[Stage 2 Grounded]` 實體 PDF 深度穿透、🟢 `[Empirical Grounded]` 本地肉身實踐、🟡 `[Stage 1 Guess]` 輕量猜想引導）。
例如針對「認知卸載與思維主權邊界」，我們直接對位批判了 Aiersilan (2026) 的 Vibe-Check 協定與 Aslan (2026) 的 LLM 依賴量表，推導出量化主權防線的**「Socratic 自審頻率 ($F_s$)」**指標。這種將 claims 與文獻、實踐進行強烈關聯的白箱化地圖，構成了我們手稿最堅實的學術防禦。

---

### C. 第三步：萬字手稿的全景合龍

在 APM 地圖與 85 篇文獻的導航下，我們分階段動筆撰寫了手稿初稿（[sovereign_research_05_manuscript.md](https://github.com/wuulong/sovereign-research-methodology/blob/main/manuscripts/sovereign_research/sovereign_research_05_manuscript.md)）：
1.  **第一章與第二章**：奠定了「認知空洞化危機」、「品位決策型原創」、「君王與百官人機共生關係」的哲學理論地基。
2.  **第三章**：詳細白箱化了十一表 SQLite 主權大腦的結構設計，說明 `prj_sync` 解耦與 `empirical_evidences` 現地真值強對合的代碼邏輯。
3.  **第四章**：直擊導師與實驗室協作痛點，提出「哈教授的 30 秒 SQL 照妖鏡四大檢核」、純文字 JSON DTO 聯邦以及一鍵 rebuild 繼承歷代前人戰役軌跡的「跳躍式知識遺傳」機制。
4.  **第五章與第六章**：誠實定量記錄了本實踐中在 Ingestion、重定向與 rebuild 時遭遇的臨界失效（ON DELETE CASCADE 觸發器 Crash）與 API 429 危機，最終宣告了行解合一的「終極自指自證真值」。

手稿不再是孤立的文字，而是大腦中 papers、manuscripts、simulations 與 red_team_logs 四大實體板塊相互激盪、自然演化的有機產物。
