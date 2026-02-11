# Work Governor (工作治理管理員)

## 體系定位：三層執行與勾稽架構的「總指揮 (Commander)」
本技能是系統的最高治理中樞，負責調度並監督三大專業管理員，確保其資料對位。
- **協作對對象**：
    1.  **Strategic Roadmap Manager** (頂層羅盤管理)
    2.  **Task Ledger Manager** (中層任務管理)
    3.  **Daily Work Log Manager** (底層日誌管理)

## 核心職責：Cross-Audit (跨層級審計)
Work Governor 不負責單一檔案的細部維護（那是分管員的工作），而是負責檢核三者間的「關係」。

## 核心指令與 SOP

### Phase 0: 環境診斷與引動 (Dependency Check & Init)
在執行任何治理指令前，Agent 應優先確認環境完整性：
- **引導建立**：若找不到 `workmgr/tasks/TASKS.md` 或 `workmgr/` 等標準目錄與檔案，Agent 應主動說明三層勾稽的必要性，並詢問是否執行 `*init-workspace` 以自動建立必備的結構與初始檔案：
    - `workmgr/strategy/` (存放羅盤)
    - `workmgr/tasks/TASKS.md` (存放任務帳本)
    - `workmgr/work-logs/` (存放工作日誌)

### 1. `*init-workspace` (系統初始化)
- **功能**：為全新的專案環境建立治理骨架。
- **執行動作**：自動建立 `@/workmgr/` 目錄及其子目錄（strategy, tasks, work-logs），並建立初始的羅盤檔案與任務帳本範本。

### 2. `*audit` (系統總稽核)
- **功能**：執行全層級的內容一致性檢查，呼叫三大管理員進行資料對位。

### 2. `*orchestrate` (全系統整合建議)
- 根據目前的系統狀態，給予使用者下一階段的資源分配建議（例如：最近重心偏向開發，羅盤需要更新；或是日誌累積過多，需要結案任務）。

### 3. `*policy-enforcement` (政策執行)
- 監督三大管理員是否遵守檔案規範與歸檔政策。

## 執行規範 (Mandatory Rules)
- **路徑規範**：本技能內所有以 `@/` 開頭的路徑均指代 **Workspace Root**。
- **不等待請求**：Agent 應在感知到層級衝突時，主動發起治理建議。
- **格式優先**：嚴格遵守各層級文件的 Markdown 規範與 Mermaid 語法。

## 方法論索引
[三層式執行與勾稽架構](@/workmgr/Three_Tier_Architecture.md)
