# 14.3 自動化探勘：直連 CLI 與離線模擬退避的 paper_scout 實踐

在本書第十章中，我們強調了 **「直連 CLI 腳本調用大於常駐 MCP 伺服器」** 的主權優先哲學。

為了讓這個哲學落地，小明在 Workspace 的 `scripts/research/` 目錄下放置了實體探勘程式碼 `paper_scout.py`。每當小明需要探勘特定物理參數（如：*AR-WET bio-implants*）時，他會命令 Antigravity 直接在背景呼叫 Python 執行此腳本。

---

### A. paper_scout.py 實體執行指令

小明只需在終端機或透過 Agent 執行：
```bash
python3 scripts/research/paper_scout.py --query "AR-WET bio-implants" --save-db
```

#### 📡 終端機即時反饋：
```
[2026-05-20 12:00:00] 🚀 啟動學術論文探勘代理人...
[2026-05-20 12:00:01] 🔍 正在查詢線上學術 API (ArXiv & Semantic Scholar)...
⚠️ API 遭遇速率限制 (HTTP 429) 或無連網環境，自動退避至【離線模擬模式 (Offline Mock Mode)】！
[2026-05-20 12:00:02] 🧬 自動生成 VRES Lab 共振傳能模擬學術資料集...
[2026-05-20 12:00:03] 💾 數據成功寫入 SQLite 資料庫: Research_Artifacts.db (papers 表)
[2026-05-20 12:00:03] 📊 數據已生成 Markdown 報表輸出。執行完畢！
```

---

### B. 離線退避與資料庫資料固化結果

這套設計保證了**「沙盒隔離環境下 100% 的執行確定性」**。當斷網或線上 API 連線受阻時，系統自動啟用內建的 `VRES Lab 虛擬壓電共振傳能` 模擬文獻集，在 SQLite 資料庫的 `papers` 表中成功寫入 3 筆高質量的虛擬學術文獻。

我們可以通過簡單的 SQLite 查詢來檢查小明資料庫內實體固化的元資料：

```sql
SELECT paper_id, title, json_extract(key_parameters, '$.Q') AS Quality_Factor FROM papers;
```

#### 📊 實體輸出報表：
| paper_id | title | Quality_Factor |
| :--- | :--- | :--- |
| `mock_arwet_1` | Design of High-Q Acoustic-Resonant Wireless Energy Transceivers (AR-WET)... | 12000 |
| `mock_arwet_2` | Non-linear Duffing Resonator for Biomedical Ultrasonic Telemetry | 8500 |
| `mock_arwet_3` | Multi-layer Piezoelectric Stack Optimization in Dissipative Media | 15000 |

小明將這些實體程式碼與資料庫同步放入了書本的 [data/research/](file:///Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/) 目錄中，讀者可直接使用 DBeaver 打開，即刻感受這份被實體固化的物理證據！
