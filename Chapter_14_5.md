# 14.5 師徒治理協議：考古日誌、品位裁決與防止掏空的面試演練

當研究生小明在本地建立好了「學術導航員」技能與 SQLite 真值資料庫後，指導教授張教授不需要親自去寫 Prompt，而是可以透過一個極具「物理可操作性」的**【三層治理檢核協議】**，來盯緊小明的思考質量，確保實驗室的學術主權不流失。

---

### 第一層：考古日誌（AIQA）審查 —— 驗證學生的「推導手感」

*   **檢核動作**：張教授每週開會時，要求小明打開本週存檔的 `AIQA_YYMM-W[n].md` 週報（或工作日誌 `WL_YYYY-MM-DD.md`）。
*   **判定標準**：
    *   **不及格**：週報中只有一兩句「幫我寫壓電傳能程式碼」的提問，答案是整段複製的黑箱 C 語言。
    *   **優良**：看到多次的來回拉鋸。小明說：「不對，你的模擬結果漏掉了高功率下的 Duffing 非線性分歧效應，這會導致系統在匹配電路中發生分岔不穩定，請重新考慮非線性彈性常數 $c^{(3)}$ 的影響！」
*   **教授面試提問**：`「這段關於 Duffing 非線性分歧的參數修正，你當時是怎麼引導 AI 的？你給了它什麼樣的物理模型，它才理解你的公式？」`

---

### 第二層：品位裁決（Taste Judgment）面試 —— 驗證學生的「主權邊界」

*   **檢核動作**：張教授在小明提交的論文初稿或實體程式碼中，隨機選取一個關鍵的設計參數（例如：*壓電元件的品質因子 Q 值選定為 12000*）。
*   **判定標準**：小明必須能指出 AI 當初給出的多個選項，並合理解釋為什麼採取這個特定參數，證明自己有能力看穿 AI 的幻覺。
*   **教授面試提問**：`「這個 Q 值當初 AI 給了你哪幾種替代設計？你為什麼決定採用這一個？請向我證明，如果這個數值在實測中發生了 AI 幻覺所導致的漂移，你會用什麼物理手段抓到它？」`

---

### 第三層：技能裝備化（Skillification）驗收 —— 驗證實驗室的「知識遺傳」

*   **檢核動作**：在學期末或小明畢業前，張教授親自驗收小明沉澱在 [skills/academic-research-navigator/](file:///Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/skills/academic-research-navigator/) 下 of Skill 裝備與 `Research_Artifacts.db` 的落庫狀態。
*   **判定標準**：剛進實驗室的新人小華，是否能在一鍵載入 `academic-research-navigator` 技能後，立刻調用小明留下的資料處理與文獻查詢流程，並且在 `Research_Artifacts.db` 中秒級比對學長當年留下的真實參數。
*   **教授面試提問**：`「你這學期為我們實驗室的『共有大腦』留下了什麼正規軍裝備（Skill）？還是你只拍拍屁股留下一堆無人能懂的聊天對話垃圾？」`

---

### 🎯 張教授的 30 秒 SQL 照妖鏡：擺脫簡報，直擊學術真值

在每週的進度報告會議（Group Meeting）上，指導教授最常面臨的窘境，是研究生用精美的投影片進行「hand-waving（揮手式模糊交代）」。論文讀了幾篇？模擬跑得如何？有沒有真正深入推導？一切都隱藏在簡報的片面描述中。

引進「三層主權知識星系架構」後，張教授不再聽小明的口頭說詞，而是可以直接索取小明本地的 `Research_Artifacts.db` 檔案，在辦公室的電腦上執行以下 **四大「學術硬度檢核 SQL」**。這能讓張教授在 30 秒內，精準透視小明的進度真實性、研究強度（含金量）與思維深度（品位裁決）。

##### 🔍 檢核一：主題進度實質率（審查進度真實性）
張教授要確認小明口中「已經做完」的主題，是否真的有本地實測支持，還是只是把文獻標記為已讀。

```sql
SELECT 
    t.sequence_order AS Seq,
    t.topic_name AS 主題名稱,
    t.status AS 主題狀態,
    COUNT(DISTINCT p.paper_id) AS 文獻沉澱數,
    COUNT(DISTINCT s.sim_id) AS 本地模擬數,
    COUNT(DISTINCT m.manuscript_id) AS 手稿產出數
FROM topics t
LEFT JOIN papers p ON t.topic_id = p.topic_id
LEFT JOIN local_simulations s ON p.paper_id = s.paper_id
LEFT JOIN my_manuscripts m ON t.topic_id = m.topic_id
GROUP BY t.topic_id
ORDER BY t.sequence_order;
```
*   **治理判讀**：若某主題標記為 `COMPLETED`，但「本地模擬數」為 `0`，張教授就能瞬間識破小明在**虛報進度**，強迫其補齊實作真值。

##### 🔍 檢核二：臨界誤差捕捉力（審查研究強度與科學發現）
最有含金量的論文，往往誕生於「理論失效的臨界區」。張教授透過 SQL 撈取本地實測與文獻理論偏離大於 10% 的異常區間：

```sql
SELECT 
    p.cite_key AS 文獻代碼,
    s.sim_id AS 模擬序號,
    json_extract(s.run_config, '$.drive_voltage') AS 驅動電壓,
    s.discrepancy_percentage AS 理論與實測誤差比
FROM local_simulations s
JOIN papers p ON s.paper_id = p.paper_id
WHERE s.discrepancy_percentage > 10.0;
```
*   **治理判讀**：如果列表中出現如 `sim_run_2` 在 12V 高驅動下與理論偏離達 `23.47%` 的資料，這證明小明**成功捕捉到了壓電材料的高驅動非線性 Duffing 分歧臨界失效點**！這是一個極具學術價值的重大發現，也是博士論文的完美突破口。反之，如果小明所有模擬的誤差都是完美的 `0%`，則說明他只是在做無意義的線性驗證，甚至有**資料捏造（Data Fitting）**的嫌疑。

##### 🔍 檢核三：手稿紅軍防禦與品位裁決（審查大腦是否被 AI 掏空 - v1.2.2 升級）
張教授不只審查背景文獻，更要確認小明在**自己撰寫的論文手稿（`m_001`）中**，面對高電壓下的失匹配缺陷，有沒有自主提出具備物理手感的解決方案，還是只是一味聽信 LLM 的空洞黑話。

```sql
SELECT 
    m.title AS 我的手稿標題,
    r.aspect_analyzed AS 質疑物理維度,
    r.reviewer_attack AS 紅軍審稿人攻勢,
    r.student_defense AS 學生主權防禦,
    r.verdict AS 裁決判定
FROM my_manuscripts m
JOIN red_team_logs r ON m.manuscript_id = r.manuscript_id
WHERE m.manuscript_id = 'm_001';
```
*   **治理判讀**：張教授親自閱讀 `student_defense`。如果小明在自己的手稿 `m_001` 登記的防禦是「引入 PLL 相位鎖定電路，並實施 8V 最高電壓退避限制」，這證明小明**成功行使了高級的品位裁決與物理電路防禦，思維主權依然存活**，通過審查！

##### 🔍 檢核四：資產繼承與跨裝置移植性（審查實驗室資產完整性）
學生畢業離校後，留下來的資料庫是不是一堆斷線的死連結？學弟妹能不能一秒接手？

```sql
SELECT 
    p.cite_key AS 文獻鍵,
    u.root_key AS 目錄抽象根,
    u.url_link AS 相對路徑,
    u.download_status AS 實體下載狀態
FROM papers p
JOIN paper_urls u ON p.paper_id = u.paper_id
WHERE u.url_type = 'local_pdf';
```
*   **治理判讀**：若 `download_status` 均為 `DOWNLOADED` 且使用抽象 root_key 儲存，證明該資料庫具備完美的環境移植性。當張教授把資料庫克隆到自己的電腦上，只需在 `directory_roots` 中更改一行 NAS 掛載路徑，**就能 100% 完美繼承並打開該學生的所有學術物理資產**，免除資料遺失或連結斷線的噩夢。

---

### 🌟 師徒面試演練示範 (Dialog Playback)

> **張教授**：「小明，我看你這篇關於壓電傳能（AR-WET）的設計進度很快。請打開你這週的 `WL_2026-05-20.md` 日誌。我注意到你將 $Q$ 值定為 12000，這個決策是怎麼來的？」
> 
> **小明**：「教授，我當時使用 `academic-research-navigator` 掃描了 Zotero 的 50 篇文獻，將資料直落本地 SQLite 資料庫。我寫了一段 SQL JOIN 去比對本地模擬：在 5V 線性區，實測與 Seong (2026) 理論誤差僅 `1.67%`；但我主動將激勵提升到 12V 時，實測 $Q$ 跌落至 7500，與理論偏離高達 `23.47%`！
> 
> AI 最早建議我忽略這個偏離、或者強行擬合（Fit）資料以維持 15000 的極限值來提高效率。但我行使了**品位裁決**，拒絕了 AI 的投機建議。因為我意識到這 `23.47%` 的偏離，正是觸發非線性 Duffing 分歧不穩定的信號。我啟動了紅軍 Agent 進行批判性質詢，並將動態 PLL 相位跟隨電路與退避電壓防禦寫入了資料庫的 `red_team_logs`。我最終決定選定 12000 作為基準，這是我在實測誤差中找到的現地真值。」
> 
> **張教授**（點頭微笑）：「很好，你沒有被 AI 牽著鼻子走。你從 `23.47%` 的誤差中抓到了真的物理發現，而且在資料庫留下了無可辯駁的品位防禦鐵證。這才是一個具備數位主權的研究者該有的樣子！」
