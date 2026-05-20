# 14.4 技能裝備化：academic-research-navigator 的 Skill 封裝

當小明在第 14.3 節成功打通了 CLI 直連腳本與 SQLite 資料持久化後，他意識到：「這套『文獻自動化探勘 -> 物理參數動態 JSON 提取 -> 紅軍自審脆弱點定錨 -> SQLite 結構化落庫』的核心邏輯，應該被封裝成一個通用的全域技能，供我未來面對任何新課題時一鍵調用。」

這就是我們在第十一章所學過的**「技能裝備化 (Skillification)」**。

---

### A. 全域技能 `academic-research-navigator` 封裝

小明命令 Antigravity 自動執行元反思，在 Workspace 的 `.agent/skills/`（書本倉庫同步路徑 [skills/academic-research-navigator/](file:///Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/skills/academic-research-navigator/)）目錄下，建構了一份標準的 `SKILL.md`。

這份技能定義檔包含了該裝備的元資料與行為邊界：

```yaml
---
name: academic-research-navigator
description: 專注於學術研究「硬核兵器庫」，支援線上文獻檢索、SQLite 結構化數據落庫、LaTeX 公式處理與紅軍自審評估。
version: 1.1
---
```

---

### B. 核心技能指令矩陣 (Command Matrix)

當 AI 載入了 `academic-research-navigator` 技能後，它便接管了以下四種核心指令，成為小明專屬的「學術導航員」：

1.  **文獻探勘 (Ingestion)**：
    *   `python3 paper_scout.py --query "<主題>" --save-db`
2.  **公式解析與 LaTeX 結構化**：
    *   `python3 parse_paper_to_db.py --paper-path "<Markdown論文路徑>"`
3.  **紅軍脆弱點評估 (Critique Score)**：
    *   啟動紅軍 Agent 進行批判性推導，將對手 Reviewer 2 最可能質疑的 Duffing 非線性分歧漏洞，自動寫入 SQLite 資料庫中。
4.  **資料與參數查詢 (Grounding SELECT)**：
    *   直連 SQLite 資料庫，利用 JSON extract 一鍵拉取近 50 篇文獻的物理特徵（如品質因子 $Q$）進行橫向對位。

---

### 🛡️ 認知守衛協定 (Cognitive Safeguard Protocol)

在這份 `SKILL.md` 裝備中，最亮眼的是寫入了一套**【導師守則：防止學生思維空洞化與認知掏空協定】**：
*   **拒絕黑箱程式碼**：AI 被禁止直接提供完整、不可讀的程式碼段。
*   **強迫蘇格拉底式引導**：AI 在給出程式碼或物理推導修正前，**必須先向學生提問**：「你認為當壓電常數 $d_{33}$ 發生退化時，你的電阻匹配迴路需要做什麼相應調整？」
*   **品位裁決要求**：AI 必須提供至少 3 種不同的物理假說，強迫學生進行最終的物理真實性「品位裁決」。

這項技能的封裝，讓小明的個人能力從「單次勞動」轉化為「可移植、可複製」的數位遺產。新進的學弟妹克隆倉庫後，只需一行 `*use-skill academic-research-navigator`，就能直接繼承學長姐沉澱下來的極硬核研究手感！
