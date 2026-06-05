# 15.2 系統臨界失效與演化突變：ON DELETE CASCADE 觸發器清空公海 Bug 的發現與「永恆基底骨架」配置

科學研究的本質從來不是一帆風順的完美拼裝，而是系統在遭遇「邊界臨界失效（System Crash）」時，逼迫主權學者行使品位裁決、發動演化突變的實踐歷程。

在撰寫本手稿 `ms_sovereign_research_2026` 的 Rebuild 測試階段，我們的本地大腦遭遇了一次幾乎毀滅性的「臨界崩塌」。

---

### A. 災難降臨：觸發器連鎖反應與 staging 被清空

當時，我們為了測試去中心化聯邦大腦的「跳躍式知識遺傳」機制，在終端機中執行了合流重建腳本 `rebuild_lab_brain.py`。
小明的初衷非常簡單：刪除本地大腦中的舊數據，重新讀取學長姐留下的 JSON 貢獻包，以驗證大腦是否能在一秒內完美合流。

然而，當重建腳本執行 SQLite 的 `DELETE FROM projects` 清理指令時，災難發生了：
由於 `schema.sql` 中為了確保關係完整性，設定了極度嚴格的連鎖刪除觸發器：
```sql
PRAGMA foreign_keys = ON;
-- ON DELETE CASCADE
```
這項觸發器引發了可怕的連鎖反應（Cascade Reaction）：
1.  刪除 `projects` 導致關聯的 `topics` 被連鎖刪除。
2.  `topics` 的刪除進而連鎖刪除了靠泊在其下的所有背景文獻 `papers`。
3.  最致命的是，我們好不容易同步落庫的 202 篇 Zotero 公海緩衝文獻，其 `topic_id` 均為 `top_haba_staging`，而該主題屬於 `projects` 下的 `prj_sync` 專案。
4.  連鎖刪除直接將 `top_haba_staging` 公海緩衝區一併物理抹除！

小明看著空空如也的 `papers` 表以及全部遺失的 Ingestion 任務血統，大腦陷入了一片空白。這是一次典型的「因過度追求語意關係完整性而導致的物理工程崩塌」。

---

### B. 演化突變：品位裁決與「永恆基底骨架」的誕生

面對這次崩塌，我們沒有選擇重回手工作業，而是將其定義為**「方法論演化的臨界契機」**。我們深刻反思：
> **「公海 staging 緩衝區文獻是實驗室的公共他者資產，專案 Topics 是循序漸進的主權脊椎。在大腦一鍵重建時，低階的寫作草稿和實測數據可以被清除，但『永恆的專案骨架』與『公海文獻資產』必須受到物理級的隔離保護！」**

於是，我們對主權大腦發動了重大的架構演變（Hotfix）：

#### 1. 永恆基底骨架 (setup_research_db.py) 物理固化
我們緊急重構了 [setup_research_db.py](https://github.com/wuulong/sovereign-research-methodology/blob/main/scripts/setup_research_db.py)，將哈爸個人的三大真實專案（`prj_tdhi` 臨床、`prj_river_exploration` 河流、`prj_ai_enablement` 賦能）與 7 大主題的時序邏輯脊椎，直接寫入為初始化腳本的**「硬編碼基底配置」**。

#### 2. prj_sync 專案路由隔離
在資料庫初始化時，單獨預載 `prj_sync` 專案與 `top_haba_staging` 主題。

#### 3. 隔離重建工序 (rebuild_lab_brain.py) 重構
我們重新編寫了重建腳本。新工序在發動 rebuild 時，不再無腦執行級聯刪除，而是：
1.  **選擇性清理**：僅刪除特定研究手稿相關的 citations 與 simulations 變更數據。
2.  **基底引渡**：一鍵重建時，腳本自動動態引用並執行 `setup_research_db` 重新架起「永恆基底骨架」，隨後合流 JSON 論文包。

```
+-------------------------------------------------------------+
|                      隔離重建防禦工序                         |
|                                                             |
|   rebuild_lab_brain.py ➔ 1. 隔離清空 (保留 prj_sync 公海)    |
|                             │                               |
|                             ▼                               |
|                          2. 呼叫 setup_research_db.py       |
|                             (重新載入三大專案/Topics 永恆骨架)  |
|                             │                               |
|                             ▼                               |
|                          3. 合流貢獻者 JSON DTO 論文包       |
+-------------------------------------------------------------+
```

這項熱修復徹底解決了級聯清空 staging 的 Bug。**這保證了不論資料庫如何重建，您的專案 Topic 骨架與公海文獻 100% 永不丟失、完美留存！**

這次臨界失效的修復歷程，完美證實了推理語言模型藍圖 [@zotero_Besta_2025_682] 與 AlphaGeometry 幾何符號約束 [@zotero_Trinh_2024_345] 的核心主張：**在複雜的系統工程中，唯有施加硬性的完整性約束與代數剪枝，方能逼出系統最穩健的突變與自適應。**
