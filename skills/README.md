# 🛡️ 三位一體治理套件 (The Trinity Suite)

歡迎使用《個人 AI 賦能》隨書附贈的數位資產。這套 Skill 套件是為了實習書中第 10.9 章節定義的「系統治理」所建構。

## 📦 包含內容

這套系統由「三位一體治理套件」與「心流捕捉協議」組成：

### A. 三位一體治理套件 (The Trinity Suite)
1.  **work-governor** (總指揮)：系統稽核、環境初始化與跨層級對位。
2.  **strategic-roadmap-manager** (頂層)：管理長期羅盤 (`workmgr/strategy/`)。
3.  **task-ledger-manager** (中層)：管理工作清單 (`workmgr/tasks/`)，對齊 ATC 規範。
4.  **daily-work-log-manager** (底層)：管理工作日誌 (`workmgr/work-logs/`)。

### B. 心流捕捉協議 (Meta-insight Protocol)
5.  **thought-log-manager**：獨立的對話紀錄機制，透過 `MT::` 關鍵字即時捕捉靈感，並定錨於 `@/thought-logs/`。

## 🚀 部署指引

1.  **複製技能**：將本資料夾下的五個技能資料夾，複製到您 Workspace 的 `.agent/skills/` 目錄中。
2.  **環境初始化**：在對話框中對代理人下令：`「請使用 work-governor 為我初始化工作區 (*init-workspace)。」`
3.  **建立治理習慣**：系統會自動建立 `workmgr/` 目錄。之後您只需透過 `*audit` 指令，即可隨時進行三層勾稽檢查。

## 📏 運作格律

本套件遵循書中定義的「三層執行與勾稽架構」，所有路徑引用均採用數位主權導向的 `@/` (Workspace Root) 語法。
