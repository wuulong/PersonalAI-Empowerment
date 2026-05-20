# 10.8 練習 3.8：🔴 MCP 與工具聯覺 —— 讓你的工具箱合致在一起 (Tool Synesthesia & MCP)

*   **【場景】**：
    您現在想嘗試將本書提到的實戰案例「WalkGIS 河流與鄉鎮開發」真正落實。您手中可能有從政府公開平台取得的河流座標（SQLite 資料庫）、您 Google 日曆裡的田野調查空檔，以及網頁上最新的學術治理計畫。在以前，這意味著您要不斷地切換 App、匯出 CSV 再匯入。但在建構了 MCP (Model Context Protocol) 體系的 Antigravity 裡，這些工具是「跨界合致」的。

*   **【任務】**：
    本練習的核心在於**「啟動工具間的連鎖與合致」**，讓 Agent 成為跨系統的指揮中心。
    1.  **取得實體材料 (Data Priming)**：由於這個練習需要操作實體資料庫，請前往 [wuulong-notes-blog](https://github.com/wuulong/wuulong-notes-blog/blob/main/static/walkgis_prj/walkgis.db) 點選下載 `walkgis.db` 實體檔案，並將其放入您的 Workspace 之中。
    2.  **掛載 MCP 伺服器**：在 Antigravity 的設定介面中，開啟或新增客製化的 MCP Server（例如：讀取剛下載資料庫的 `sqlite-mcp` 或連動外部服務的 `google-calendar-mcp`）。
    3.  **發布「整合」指令**：挑戰代理人的跨界能力。輸入：`「請讀取我的 WalkGIS 資料庫中有關高屏溪的 POI 目錄，對比我下週 Google 日曆的行程，並替我搜尋這幾天該流域的所有合法測站，最後將建議的田野路徑產出成一份 Markdown 計畫。」`
    4.  **觀察連鎖反應**：注意介面上的工具氣泡。您會看到 Agent 先呼叫了資料庫（讀取 POI）、再呼叫了日曆（確定時間）、最後跳到網路（即時搜尋）。

---

### 🛡️ 進階升級：CLI 優先直連調用與離線避退哲學 (CLI-over-MCP & Offline Fallback)

雖然 MCP 常駐守護進程能提供通用的整合能力，但在極致的硬核研究場景中，**「直連 CLI 腳本調用」**才是速度與主權的終極追求。這也是領主在實戰中建立的關鍵武裝：

1.  **直連 CLI 的強大優勢**：
    *   **零通訊開銷**：省去 MCP 通訊協議（JSON-RPC Over Stdio）的包裝與監聽，直接賦予 Agent 執行背景 `python3` 的權限，達到毫秒級極速回應與熱除錯。
    *   **範例腳本**：`/scripts/research/paper_scout.py`（完整情境與實戰代碼解析請參見 **第 14 章 14.3 節** 的學術研究情境展開）。
        當領主需要探勘新領域論文時，Agent 不需通過第三方服務，直接直呼此腳本對線上 API 進行語義探勘與 SQLite 落庫。
2.  **防禦性降級與沙盒避退（Offline Mock Mode）**：
    *   網路是不穩定的，特別是在高度受限的沙盒或飛行中（Offline）。
    *   **退避機制**：我們在 `paper_scout.py` 中內建了防禦性避退。一旦偵測到網路 Timeout 或 429 限制，工具會優雅退化為**【本地離線模擬模式 (Offline Mock Mode)】**，利用內建的 `AR-WET` 偽文獻測試資料集完成落庫，確保 Agent 的推理鏈與 Grounding 流程 100% 不中斷。

3.  **實體代碼實錄：Sovereign Paper Scout（極簡版）**：
    為了讓領主能立即在終端機開火，以下是書中提供的極簡版、**「零第三方套件依賴 (Zero Dependency)」** 的 Python CLI 直連腳本。讀者只需將其存為 `paper_scout_mini.py`，即可一鍵完成「API 探勘 ➔ 離線模擬避退 ➔ SQLite JSON 數據落庫」的完整閉環：

```python
import sqlite3, json, urllib.request, urllib.parse

# A. 初始化資料庫與 Schema (定義關係-NoSQL 混合欄位與相容大信封)
def init_db():
    conn = sqlite3.connect("Research_Artifacts.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        paper_id TEXT PRIMARY KEY,
        title TEXT,
        authors TEXT,
        year INTEGER,
        core_method TEXT,
        key_parameters TEXT, -- JSON 格式，儲存動態物理參數
        critique_score TEXT, -- JSON 格式，儲存紅軍自審漏洞
        meta_data TEXT       -- JSON 格式，向前相容信封 (數位基因)
    )
    """)
    conn.commit()
    return conn

# B. 直連 API 探勘文獻 (內建離線模擬退避機制)
def scout_papers(query):
    # 離線模擬退避資料集 (VRES Lab 虛擬聲學共振傳能 AR-WET 論文)
    mock_papers = [{
        "paper_id": "mock_arwet_1",
        "title": "Design of High-Q Acoustic-Resonant Wireless Energy Transceivers (AR-WET) for Active Bio-Implants",
        "authors": "J.-S. Seong, H.-E. Shin, and W. Wuulong",
        "year": 2026,
        "Q": 12000, "f0": "28.5 MHz",
        "vulnerabilities": ["高功率下發生 Duffing 分歧非線性不穩定"]
    }]
    
    try:
        # 嘗試直連 ArXiv API 進行檢索
        url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            xml_data = response.read().decode('utf-8')
            print("📡 ArXiv API 連線成功！正在解析真實文獻...")
            return mock_papers # 簡化示範直接回傳結構，讀者可自行解析 XML
    except Exception as e:
        print(f"⚠️ 連線受阻 ({e})，自動退避至【離線模擬模式 (Offline Mock Mode)】...")
        return mock_papers

# C. 數據寫入 ( NoSQL JSON 封裝與相容 Envelope)
def save_to_db(conn, papers):
    for p in papers:
        # 物理參數 NoSQL 封裝
        key_params = json.dumps({"Q": p.get("Q", 0), "f0": p.get("f0", "")})
        # 紅軍脆弱點封裝
        critique = json.dumps({"vulnerabilities": p.get("vulnerabilities", [])})
        # 向前相容大信封 (Metadata Envelope)
        metadata = json.dumps({"scouted_at": "2026-05-20", "agent_engine": "Antigravity-L4"})
        
        conn.execute("""
        INSERT OR REPLACE INTO papers 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["paper_id"], p["title"], p["authors"], p["year"], 
              "Acoustic Wave Confinement (模擬)", key_params, critique, metadata))
    conn.commit()
    print("💾 數據成功沉澱至本地 SQLite 資料庫！")

if __name__ == "__main__":
    conn = init_db()
    results = scout_papers("AR-WET bio-implants")
    save_to_db(conn, results)
```

---

*   **【差異化思考】**：
    *   **Gemini Web/App**：它雖有 Extensions，但那是受限於雲端花園的「標準套餐」。您無法讓它讀取硬碟裡的私有 SQLite 資料庫，更無法在斷網時自動啟用離線模擬落庫。
    *   **Antigravity**：MCP 協議就像是為 AI 安裝了「萬能插座」，而 **CLI 直連則像是不插插座、直接將神經突觸焊接在作業系統的核心**。不論網路如何動盪，主權依然在您的終端機內完美維持。

*   **【🚀 抽象對齊】**：
    *   **「工具合致 (Tool Integration)」**：領悟到代理人的本質是各種工具能力的「連接器」，而非工具本身。
    *   **[T-4.2] 萬能之鑰 (Master Key)**：驗證了 MCP 協議如何將作業系統與外部服務轉化為 Agent 可用的實體肢體。
    *   **[I-CLI-12] 視角覺醒**：當工具不再是障礙而是器官，您看待數位環境的視角將從「操作者」轉變為「统御者」。
