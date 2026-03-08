# 主題：個人AI賦能 (Personal Empowerment)

---

## 🎯 受眾與需求 (Target Audience & Needs)
- **核心受眾**：具備 AI 研發背景的技術人員 (Engineers, R&D, Data Scientists)。
- **受眾痛點/需求**：
    - **「工程師悖論」**：開發強大的 AI 系統給客戶，但自己的日常庶務 (文件、測試、日誌) 仍透過傳統手動方式處理，效率未同步演進。
    - **「通用工具與個人脈絡的斷層」**：知道如何調教大模型，但不知如何建構一套能「自我繼承經驗」的個人 AI 協作體系 (如：Skillification)。
    - **「過度工程化 (Over-engineering) 傾向」**：習慣開發「通用的工具」，而忽視了 AI 時代其實可以為「每一份資料」現場編寫「即時代碼 (On-the-fly Coding)」的高靈活性。
    - **「需求定義障礙」**：會寫 Code，但在面對複雜決策或創意發想時，不熟悉如何利用 AI 的推理 (Reasoning) 能力進行「需求訪談」與「邏輯閉環」。
    - **「從技術到價值的焦慮」**：面對 AI 快速迭代，擔心自己的編碼產值被取代，卻未意識到「軟體工程思維」大於「編碼語法」的新價值定位。

---

## 📖 說明與資源
- **GitHub**: [wuulong/PersonalAI-Empowerment](https://github.com/wuulong/PersonalAI-Empowerment)
- **NotebookLM Share**: [個人AI賦能分享](https://notebooklm.google.com/{{Update_Link}})
- **NotebookLM Source**: `Excavating_AI_Empowerment.pdf`
- **筆記/系列文**: 個人AI賦能方法論系列
- **Slides**: [Google Slides Link](https://docs.google.com/presentation/{{Update_Link}})

---

## 🏗️ 分享綱要 (Outline & Hardcore Evidence)

### 1. AI 三階段論：技術人的演進史
- **第一階段：QA 與自學的演化 (The Inception)**
    - **證據示範**：`[AIQA-解讀CSV]` (2023-03-23)。
    - **案例說明**：第一次將 18 筆圖書 CSV 餵給 AI，發現「不必寫程式就能篩選資料」的震撼感。從「跟 AI 聊天」轉向「將 AI 當作邏輯處理器 (Reasoning Engine)」。
- **第二階段：Verbal Coding 與軟體工程民主化 (The Revolution)**
    - **證據示範**：`[Vibe Coding 実踐]` (Chapter 12.1)。
    - **案例說明**：`.fab` (Fabfile) 系統管理實戰。工程師不再糾結於 Python 語法，而是專注於「清理硬碟、過濾超大檔案」的**意圖 (Vibe)**。軟體工程的價值從「寫 Code」轉移到「需求定義」。
- **第三階段：資料邏輯與現場編碼 (The On-the-fly Paradigm)**
    - **證據示範**：針對特定資料集 (如寶山水庫、日誌解析) 的即時 Script 產出。
    - **案例說明**：捨棄「通用工具 (Generic Tool)」思維。展示如何讓 AI 針對單一混亂檔案，現場寫出代碼並在 2 分鐘內產出圖表。這就是「拋棄式代碼 (Disposable Code)」的威力。

### 2. 核心實戰：技能沉澱 (Skillification)
- **證據示範**：`[Skill 封裝]` (練習 3.9)。
- **案例說明**：將一次成功的 Debug 或數據處理流程，要求 AI 自動寫成 `SKILL.md`。下次執行時，AI 具備「肌肉記憶」，讓成功經驗成為可累加的數位資產。

---

---

## 📋 議程 (Agenda)
1. 21:00 - 21:10：**技術人的演化史** (從 18 筆 CSV 的啟示談起)
2. 21:10 - 21:30：**Verbal Coding 實戰** (以 Fabfile 自動化為例，談意圖治理)
3. 21:30 - 21:45：**資料靈魂與現場編碼** (現場示範即時資料轉化)
4. 21:45 - 22:00：**技能化與虛擬分身** (如何構建你的 AI 樂高大腦)

---

## 🧠 技術人專屬：心法與證據清單 (The Techie's Mindset)

| 心法編號 | 核心心法 (Mindset) | 證據 ID (Evidence) | 講授重點 |
| :--- | :--- | :--- | :--- |
| **[C-08]** | **架構先行** | `S-230323` | AI 是邏輯機而非計算機。餵資料前，先定義 Schema 魂魄。 |
| **[C-14]** | **Vibe Coding** | `Chapter 12.1` | 拋棄語法執著。用「意圖 (Vibe)」驅動 Fabfile 統御 OS 原生指令。 |
| **[I-CLI-11]** | **視角覺醒** | `tree` 指令實作 | 給 AI `run_command` 指令與 `tree` 視角，讓它從「聊天室」搬進「施工現場」。 |
| **[I-CLI-16]** | **品位裁決** | `不滿意` 的瞬間 | 研發人員最高價值不在於產出「正確」內容，而在於針對 1% 靈魂缺失的「不滿意」。 |
| **[M::]** | **M:: 協議 (即時固化)**| `Chapter 6.7` | 在戰鬥中升級武器。驚訝的那一秒，就是封裝新工具的最佳時機。 |
| **[Skill]** | **技能化封裝** | `練習 3.9` | 拒絕重複勞動。將每一次成功的 Debug 轉化為可維護的數位資產。 |
| **[BMM]** | **BMAD 治理** | `Chapter 12.5` | 軟工民主化：一人即團隊。用 PRD/CIS/Wlog 流程統御複雜系統開發。 |

---

## 📝 會議紀錄 (Minutes & Notes)
### 紀錄：
- 

### 筆記：
- 

---
*Created using Presentation SOP v2.0*
