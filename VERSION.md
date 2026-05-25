# 版本歷史 (Version History) - 個人賦能 (Personal Empowerment)

本檔案紀錄《個人賦能》書稿之版本演進與重大更新說明。

## [v1.2.2] - 2026-05-25
### 🚀 達成里程碑 - 主權重裝協奏（Sovereign Orchestration）自動化閉環正式落地
- **文獻交叉演化譜系**：新增 `paper_relations` 關係表，以 SQL 遞迴查詢秒級繪出學術演化金線。
- **手稿紅軍防禦機制**：升級 `red_team_logs` 向上外鍵關聯 `my_manuscripts`，讓 AI 審稿人直接挑釁研究生自主假設。
- **影子模擬多模態欄位**：於 `local_simulations` 新增 `artifact_visual_path`，支援波形與熱點圖之聯覺品位判讀。
- **元寫作 LaTeX 骨架組裝**：規劃開發 `generate_manuscript_scaffold.py`，讀取資料庫引用心智脈絡自動組裝 LaTeX 骨架。
- **心流考古自動落庫**：規劃開發 `harvest_flow_to_db.py`，將 Markdown 日誌中的推導手感自動 parse 存入資料庫。
- **實體提案詳見**：[v1.2.2_Proposal_Sovereign_Orchestration.md](file:///Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/planning/v1.2.2_Proposal_Sovereign_Orchestration.md)。

## [v1.2.1] - 2026-05-21
### 🚀 達成里程碑 - Zotero 雙核共生直連與雙向回流工具鏈升級
- **Zotero 直連同步方法論**：確立 Zotero（物理文獻入口）與 SQLite（思想心智中樞）的「單向唯讀投影、雙核共生」分工。
- **Zotero 大量遷移獨立腳本**：新增 `migrate_zotero_bib.py`，支援 Better BibTeX 批次匯入，預置 AI 協同改寫 Prompt。
- **主權文獻回流工具與手冊**：新增 `export_selected_bib.py` 與 `Zotero_Feedback_Guide.md`，支援 Zotero 魔術棒與 BIB 匯出一鍵安全回流 Zotero。
- **三層學術偵察引擎藍圖**：撰寫 `Academic_Recon_Engine_Blueprint.md`，規劃 arXiv + Semantic Scholar + OpenAlex 的重型文獻情報偵察母艦。

## [v1.2.0] - 2026-05-21
### 🚀 達成里程碑 - 三層聯邦主權星系架構與導師 SQL 盲檢大改版
- **三層十表 Schema 部署**：正式廢除單表結構，升級為 10 表聯邦主權架構，徹底理清 Ingestion、Grounding、Execution 與 Evolution 的實體關係。
- **路徑解耦與跨裝置移植**：引入 `directory_roots` 與 `paper_urls`，解耦實體絕對路徑，實現實驗室 NAS 與個人 macOS 路徑 100% 機動映射。
- **現地真值誤差比對**：資料庫實體固化 12V 高激勵壓電 `23.47%` Duffing 非線性失匹配偏離與 PLL 動態防禦自審鐵證。
- **書籍手稿 Chapter 14 滿血升級**：
  - 更新 `Chapter_14_2.md` 以映射新版 DDL 及學術生命週期。
  - 更新 `Chapter_14_5.md` 增寫「張教授的 30 秒 SQL 照妖鏡」以實行資料庫盲檢，並改寫 Dialog Playback 師徒攻防。

### ✨ 新增章節與實體資產
- **`scripts/research/Sovereign_Research_Database_Guide.md`**: 全新硬核學術主權手冊，附帶四大導師稽核 SQL，並嵌入可互動之 Mermaid 流程圖與 Live Editor 連動連結。
- **`data/research/Research_Artifacts.db`**: 重建 100% 純中文壓電傳能（AR-WET）高質量關係型實體資料庫。

## [v1.1.0] - 2026-05-20
### 🚀 達成里程碑 - 學術導航員與情境展開全面裝備
- **新增第 14 章情境展開**：正式增設 **「第 14 章：情境展開 —— 主權研究者的自我革命」**，將五階段演化梯融會貫通於壓電聲學無線傳能（AR-WET）的電機學術研究實戰中。
- **跨章節引用對位**：在第 10、11、12、13 章中注入指向第 14 章的網路化引用 Hooks，提升書稿的整體學術與系統架構美感。
- **物理資產與程式碼開源**：將實體 CLI 調用腳本、SQLite 預建真值資料庫、以及 Skill 技能定義檔全面同步複製入書本的開源倉庫中。

### ✨ 新增章節與實體資產
- **Chapter 14 (14.0 - 14.6)**: 涵蓋學術自我掏空痛點、SQLite 混合欄位設計、paper_scout CLI 探勘、學術導航員 Skill 封裝、以及指導教授「三層治理面試演練」。
- **`data/research/Research_Artifacts.db`**: 克隆即用、12KB 的虛擬學術研究預建 SQLite 真值資料庫（內建 3 筆 AR-WET 物理元資料與紅軍 vulnerability 資料）。
- **`scripts/research/paper_scout.py`**: 完整的雙源學術 API 探勘與沙盒離線退避 Python CLI 腳本；在 `Ch 10.8` 中加印 distilled 的 Python 極簡版原始碼。
- **`skills/academic-research-navigator/SKILL.md`**: 可移植的 Agent 裝備化技能定義檔，內置極硬核「防止學生思維空洞化之認知守衛協定」。

---

## [v1.0.0] - 2026-02-14
### 🚀 達成里程碑
- **全書完稿**：完成從 Part I (數位考古與演化) 到 Part II (賦能實踐指南) 全書 13 章節。
- **自動化集成**：透過 `merge_book_content.py` 腳本完成 116 個章節檔案之首版集成。
- **台灣語感對位**：執行「語感校準風暴 (Linguistic Storm)」，全面修正 93 個檔案中的非在地術語。
- **數位典藏化**：確立「發布區」與「計畫區」分離之專案結構。

### ✨ 新增章節
- **Part I (Ch 1-6)**: 建立數位考古、手感養成、Agentic 實驗室、代理人革命與品味裁決等核心論點。
- **Part II (Ch 7-13)**: 包含核心方法論 (BMM/CIS/BMB)、五階段演化梯實踐、與 30 天入軌計畫。

### 🛠️ 技術更新
- 建立 `align_taiwanese_linguistics.py` 語感校準工具。
- 引入 `thought-log-manager` (M:: 協議) 作為心流捕捉標準。

---
**維護者**: 哈爸  
**發布日期**: 2026-05-20
