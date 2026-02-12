# 11.0 快速入門：BMAD-METHOD 敏捷驅動引擎

### 1. BMAD-METHOD 是什麼？
**BMAD-METHOD (B-Mad Method)** 是一個專為「敏捷驅動開發 (Agile Driven Development)」設計的通用型 AI Agent 框架。它不只是一個工具包，而是一套數位格律，旨在將 AI 代理人的專業能力與人類的敏捷流程深度合致 (Integrated)。

*   **定義**：它是一個這以「模組 (Modules)」為核心的環境，讓 AI 代理人能透過標準化的協定（MCP）、預定義的任務（Tasks）與引導式的工作流程（Workflows）來執行複雜任務。

### 2. 它想解決什麼問題？（核心願景）
在傳統的 AI 使用場景中，人類常受困於「提示詞疲勞」與「流程碎片化」。BMAD 的目標是：
*   **脫離片段對話**：將 AI 從單純的「聊天機器人」轉化為具備領域知識（Domain Expertise）的「虛擬團隊成員」。
*   **奪回主權 (Digital Sovereignty)**：透過本地化的配置與私有知識庫的掛載，讓使用者在自有的環境中統御 AI，而非受限於雲端平台的黑盒子。

### 3.它是如何運作的？（三位一體架構）
BMAD 透過以下三個層級實現能力轉化：
*   **Core (主指揮官)**：負責系統初始化、環境配置與跨模組的協調。
*   **Modules (專業領域)**：
    *   **BMM (BMad Method)**：負責技術專案管理、需求分析與開發故事。
    *   **CIS (Creative Intelligence Suite)**：負責腦力激盪、創意設計與敘事創作。
    *   **BMB (BMad Builder)**：負責「自我進化」，用來建構新的 Agent 與模組。
*   **Workflows (執行路徑)**：將複雜目標拆解為可被驗證的步驟（Steps），確保 AI 產出的穩定性。

### 4. 使用者要怎麼用？（Quick Start 四步驟）

如果您想在自己的開發環境中啟動 BMAD，請遵循以下步驟：

#### Step 1: 環境初始化
確保您的系統已安裝 `Node.js` 與 `npm`，在您的專案根目錄下執行：
```bash
# 透過 npm 安裝核心引擎
npm run install:bmad
```

#### Step 2: 交互式安裝
執行安裝指令後，系統會進入交互式引導。
```bash
# 啟動安裝程序
bmad install
```
*   **輸入身分**：告訴 Agent 您是誰（這將影響對話語氣）。
*   **選擇 IDE**：支援 Claude Code, Cursor, Windsurf, VSCode 等。
*   **下載模組**：初學者建議優先安裝 `bmm` 與 `cis`。

#### Step 3: 狀態檢查
檢查您的「數位武裝」是否齊備：
```bash
bmad status
```
*   若顯示 `✓ Installed modules: bmm, cis`，表示已就緒。

#### Step 4: 召喚代理人
在您的 IDE 中呼叫指令開始協作：
*   輸入 `*help`：顯示當前模組的所有可用命令。
*   輸入 `*agent research-analyst`：啟動專業的研究分析師角色。
*   輸入 `*task product-brief`：啟動「產品需求定義」工作流程。

---

### 5. 進階應用：BMAD Personal Assistant
除了核心的開發模組，本書作者特別為專業人士開發了 **BMAD Personal Assistant (bmad-pa)**。

*   **GitHub 倉庫**：[wuulong/bmad-personal-assistant](https://github.com/wuulong/bmad-personal-assistant)
*   **它是什麼？**：這是一個基於 BMAD 框架的「個人生活與工作擴充包」。它將 BMAD 的治理能力從「程式碼開發」延伸到了「日常瑣事、學習計畫與資訊檢索」。
*   **為什麼做？**：為了解決專業人士在多重角色間（研究者、學習者、生活管理者、IT 支援）切換時的認知負荷。它提供了一個「協調者 (Coordinator)」角色，幫您調度不同的虛擬分身。
*   **使用者可以怎麼用？**
    1.  **轉換協調員**：執行 `*agent personal-assistant-coordinator`，由韋小寶（Agent 名稱）為您總管全局。
    2.  **跨域調度**：您可以請協調員「幫我規畫下週的 Python 學習進度 (學習導師)」，同時「幫我整理剛才那場關於智慧化醫院的對話重點 (資料組織師)」。
    3.  **生活治理**：利用「生活管理員」與「IT 協作者」處理日常提醒、安排活動或產出自動化測試腳本。

BMAD-PA 是本書後半段「虛擬分身」實踐的最佳實體範例，它展示了如何將 AI 轉化為真正懂您的數位助理。

---

### 💡 哈爸筆記：給讀者的建議
> 「BMAD 並非要取代您的思考，而是要將您的思考『格律化』。當您開始使用 `*task` 命令時，您會發現 AI 不再只是亂猜您的心意，而是循著一套被驗證過的專業架構與您共同前行。」
