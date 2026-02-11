# Task Ledger Manager (任務帳本管理員)

## 體系定位：中層 - 工作清單 (Task List / ATC)
本技能處於「三層執行與勾稽架構」的**中層**，是頂層意向與底層事實的橋樑。
- **性質**：執行性 / 具體化。
- **功能**：掌管任務的生命週期，包含 ID 生成、狀態追蹤、優先級管理、以及自動化的歸檔審計。符合 **ATC (Antigravity Task Ledger)** 規範。

## 核心規格 (ATC Standards)
- **實體檔案**：`@/workmgr/tasks/TASKS.md`
- **ID 系統**：`T[YYMMDD]-[NN]` (例如：T260212-01)
- **區域定義**：
    1.  `## 🚀 當前執行 (Ongoing)`：目前正在動手的事項。
    2.  `## ✅ 已完成 (Archive)`：已結案並標註日期的事項。
    3.  `## 📥 待處理收納 (Backlog)`：已識別但尚未啟動的事項。
    4.  `## ⏳ 等待回應 (Blocked/Waiting)`：因外部因素暫停的事項。

## SOP 執行流程

### Phase 1: 任務稽核 (Task Audit)
- **ID 產生**：每當使用者想新增任務，自動讀取 `@/workmgr/tasks/TASKS.md` 中的 `Latest ID`，產生下一組序號。
- **狀態偵測**：根據當前對話進度或 `Wlog` 紀錄，主動詢問使用者是否將特定任務從 `Ongoing` 移至 `Archive`。

### Phase 2: 垂直勾稽 (Vertical Alignment)
- **向上對齊 (To Compass)**：定期檢核 `@/workmgr/tasks/TASKS.md` 中的高優先級任務是否對齊最新的 `@/workmgr/strategy/roadmap_*.md`。若發現「有羅盤無任務」或「有任務無羅盤」，應主動提醒。
- **向下追蹤 (To Wlog)**：比對 `@/workmgr/work-logs/WL_*.md` 中的「成果產出」，若日誌提到已完成，則同步更新 `@/workmgr/tasks/TASKS.md` 狀態。

### Phase 3: 歸檔與清理 (Retention & Cleanup)
- **雙月清理政策**：每個月初執行。
- 將 `Archive` 區中「除本月及上月以外」的舊紀錄清理掉（或移至 `@/workmgr/tasks/ARCHIVE_YYYY.md`）。
- 更新 `Latest ID` 定錨點。

## 關鍵關鍵字 (Trigger Keywords)
`task`, `todo`, `T26`, `atc`, `audit-tasks`, `archive-tasks`.

## 方法論索引
## 執行規範 (Rules)
- **路徑規範**：本技能內所有以 `@/` 開頭的路徑均指代 **Workspace Root**。

[三層式執行與勾稽架構](@/workmgr/Three_Tier_Architecture.md)
