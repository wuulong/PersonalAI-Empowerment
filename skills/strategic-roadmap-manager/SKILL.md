# Strategic Roadmap Manager (策略羅盤管理員)

## 體系定位：頂層 - 羅盤 (Compass)
本技能處於「三層執行與勾稽架構」的**頂層**。
- **性質**：意向性 / 長期性。
- **功能**：掌管整體方向與大局觀。透過結構化的每月記錄與 **Mermaid 可視化圖表**，將瑣碎的日常進展轉化為清晰的戰略地圖。

### 向下勾稽 (Downward Linkage)
羅盤定義的方向必須轉化為 **中層（Task List, `@/workmgr/tasks/TASKS.md`）** 的具體待辦事項。每次更新羅盤後，AI 應主動檢視 Task List 是否需要新增、調整或遺棄特定任務。

**Keywords**: `strategy`, `roadmap`, `mermaid`, `visualization`, `planning`, `status-tracking`, `architecture`.
### 執行規範 (Rules)
- **路徑規範**：本技能內所有以 `@/` 開頭的路徑均指代 **Workspace Root**。

**Methodology**: [三層式執行與勾稽架構](@/workmgr/Three_Tier_Architecture.md)

## 核心產出
- **每月策略檔案**：`@/workmgr/strategy/roadmap_YYYYMM.md`
- **年度策略羅盤**：`@/workmgr/strategy/roadmap_YYYY.md` (顆粒度較粗，專注於季度的演化與全年的核心版圖)
- **內容構成**：
    1. **Strategic Mindmap**：戰略支線分佈（核心版圖）。
    2. **Causal Flowchart**：因果邏輯與執行鏈條。
    3. **Evolution Roadmap**：時間軸上的架構演化。
    4. **Planning vs Status**：待辦規劃與已完成狀態的對照。
    5. **User Manual Context**：由使用者手動補充的隱性資訊（無法從日誌提取的動機、直覺或未公開計畫）。

## SOP 執行流程

### Phase 0: 隱性 Context 輸入 (Pre-processing)
AI 會先讀取 `@/workmgr/strategy/USER_STRATEGIC_CONTEXT.md`。此檔案存放使用者手動補充的長期動機、商業直覺或不便寫入公開筆記文的大方向。

### Phase 1: 脈絡分析 (Context Analysis)
1. 讀取「哈爸筆記文」提取顯性進展。
2. 結合 `USER_STRATEGIC_CONTEXT.md` 提取隱性意圖。
3. 由 AI 交叉分析，辨識出本月的關鍵戰略調整。

### Phase 2: 架構繪製與同步 (Annual & Monthly Sync)
1. 更新當月檔案 `roadmap_YYYYMM.md`。
2. 同步更新/彙整年度檔案 `roadmap_YYYY.md`，維持年度目標的連貫性。

### Phase 3: 狀態校準 (Alignment)
1. 產出本月檔案並與上個月進行對比。
2. 標註「原定計劃的偏離處」與「新長出的戰略支線」。
3. 詢問使用者：「這個架構圖符合您現在腦中的直覺嗎？」

### Phase 4: 歸檔與 Commit (Archive)
1. 確保檔案存放在指定目錄。
2. Commit 到 Git，形成「戰略演化史」。

## Tips & Troubleshooting (Mermaid)

### Mindmap 語法守則 (防止解析錯誤)
1. **使用方括號 `[ ]` 定義節點**：
   - 始終使用 `[文字]` 格式定義節點，這能有效包裹包含空格或符號的內容。
   - 範例：`[WalkGIS 基礎建設]`
2. **處理特殊字元**：
   - **嚴禁使用半形括號 `()`**：這會被誤認為節點形狀定義。請改用空格或直接移除。
   - **避免半形冒號 `:`**：建議改用全形冒號 `：`。
   - **避免特殊符號**：如 `&`, `|`, `/` 等，若必須使用，確保在方括號 `[ ]` 內。
3. **層級縮排**：
   - 確保縮排一致（建議使用 2 個空格），縮排決定了心智圖的父子關係。

### 狀態標記 (Timeline)
- 在 `timeline` 語法中，使用 `: Status=Done` 或 `: Status=Active` 來直覺化進度，這也是本 Skill 的標準標記法。

### 外部連結自動化 (已掛起)
- 曾嘗試自動化產出 `mermaid.live` 連結，但因第三方工具對 JSON 狀態極度敏感而暫停。
- 技術細節請參考：[Mermaid.live 連結自動化筆記](../../docs/strategy/notes/mermaid_link_automation_lessons.md)
