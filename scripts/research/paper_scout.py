import os
import sys
import argparse
import urllib.request
import urllib.parse
import json
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime

DEFAULT_DB_PATH = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment/data/research/Research_Artifacts.db"

# ==============================================================================
# 【學術去敏感化 100% 中文精裝版】本地離線模擬資料集
# ==============================================================================
MOCK_PROJECT = {
    "project_id": "prj_arwet",
    "project_name": "AR-WET 生醫植入式無線傳能系統",
    "description": "開發用於主動式生醫植入物（如心律調節器、微型神經刺激器）的高效率聲學共振無線能量傳輸系統 (Acoustic-Resonant Wireless Energy Transceiver)。解決傳統電磁感應在生物組織中衰減極快、且易產生高溫灼傷的致命缺點。",
    "search_spec": {
        "keywords": ["AR-WET", "acoustic-resonant", "ultrasonic telemetry", "piezoelectric stack"],
        "exclude": ["electromagnetic induction", "rf link"],
        "min_year": 2020
    },
    "architecture_spec": {
        "target_freq_MHz": 28.5,
        "target_Q_factor": 12000,
        "max_depth_mm": 10.0,
        "piezo_material": "PZT-5H (鈦酸鋯鉛壓電陶瓷)",
        "allowed_temp_rise_C": 2.0
    }
}

MOCK_TOPICS = [
    {
        "topic_id": "top_piezo_modeling",
        "topic_name": "壓電諧振器理論物理建模",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {
            "focus_variables": ["resonance_frequency", "Q_factor", "coupling_coefficient"],
            "equations": ["Mason_Equivalent_Circuit_Model", "KVD_Equivalent_Circuit"],
            "auto_tags": ["piezoelectric", "analytical-modeling"]
        }
    },
    {
        "topic_id": "top_duffing_comp",
        "topic_name": "非線性 Duffing 分歧匹配電路補償",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {
            "focus_variables": ["bifurcation_threshold_voltage", "phase_mismatch", "insertion_loss"],
            "equations": ["Duffing_Nonlinear_Equation", "Van_der_Pol_Oscillator_Model"],
            "auto_tags": ["non-linear", "bifurcation", "impedance-matching"]
        }
    },
    {
        "topic_id": "top_biocompatibility",
        "topic_name": "系統級多晶片整合與生物適應性實測",
        "sequence_order": 3,
        "status": "PLANNED",
        "focus_spec": {
            "focus_variables": ["temperature_rise_rate", "tissue_absorption_loss", "encapsulation_shear_stress"],
            "equations": ["Bioheat_Transfer_Equation", "Specific_Absorption_Rate_SAR"],
            "auto_tags": ["biomedical", "in-vivo-test", "thermal-safety"]
        }
    }
]

MOCK_PAPERS = [
    {
        "paper_id": "semscholar_seong_2026",
        "cite_key": "Seong2026ARWET",
        "topic_id": "top_piezo_modeling",
        "title": "用於主動植入物之高Q值聲學共振無線能量傳輸元件設計",
        "authors": "成鐘錫, 辛賢恩, 吳烏龍 (W. Wuulong)",
        "year": 2026,
        "core_method": "聲學波包限域物理優化技術 (Acoustic Wave Confinement)",
        "bibtex": """@article{Seong2026ARWET,
  author = {Seong, J.-S. and Shin, H.-E. and Wuulong, W.},
  title = {Design of High-Q Acoustic-Resonant Wireless Energy Transceivers (AR-WET) for Active Bio-Implants},
  journal = {IEEE Transactions on Biomedical Engineering},
  year = {2026},
  volume = {73},
  pages = {142--155},
  publisher = {IEEE}
}""",
        "meta_data": {
            "theoretical_Q": 12000,
            "resonance_frequency_MHz": 28.5,
            "piezo_material": "PZT-5H",
            "citation_count": 15
        },
        "abstract": "本論文針對用於主動生醫植入物之高Q值聲學共振無線能量傳輸收發器（AR-WET）進行了物理結構優化。我們通過在壓電諧振片邊緣導入聲學波包能量限域設計，成功在 28.5 MHz 的諧振頻率下，實現了高達 12,000 的物理品質因子（Q值）。該設計能顯著降低聲波朝支撐結構的能量洩漏，將無線能量傳輸效率提升了 35%。",
        "urls": [
            {"type": "publisher", "link": "https://ieeexplore.ieee.org/document/mock_seong_2026"},
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2605.99901.pdf"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/ARWET_2026_Seong.pdf"}
        ],
        "tags": ["piezoelectric", "acoustic-resonant", "MEMS", "biomedical"]
    },
    {
        "paper_id": "arxiv_tanaka_2024",
        "cite_key": "Tanaka2024MEMS",
        "topic_id": "top_piezo_modeling",
        "title": "植入式生醫微網路之聲學共振收發元件技術",
        "authors": "田中實, 新藤健二",
        "year": 2024,
        "core_method": "高效率壓電薄膜微機電製程 (Piezoelectric Thin-Film MEMS)",
        "bibtex": """@preprint{Tanaka2024MEMS,
  author = {Tanaka, M. and Shindo, K.},
  title = {Acoustic-Resonant Transceiver (AR-WET) Technology for Implantable Biomedical Micro-Networks},
  journal = {arXiv preprint arXiv:2408.12345},
  year = {2024}
}""",
        "meta_data": {
            "theoretical_Q": 8500,
            "resonance_frequency_MHz": 24.2,
            "piezo_material": "AlN (氮化鋁)",
            "citation_count": 42
        },
        "abstract": "本論文探討使用高效率壓電薄膜基板製造體聲波（BAW）能量收集系統的製程設計。我們開發了先進的微機電加工製程，成功在矽晶圓上釋放出厚度小於 5 微米的壓電超薄振膜，實現了 20 MHz 以上的高頻諧振操作。本技術特別適用於多個微型植入傳感器節點組成的生醫體內微網路通訊與傳能需求。",
        "urls": [
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2408.12345.pdf"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/MEMS_2024_Tanaka.pdf"}
        ],
        "tags": ["piezoelectric", "MEMS", "biomedical"]
    },
    {
        "paper_id": "semscholar_love_2025",
        "cite_key": "Love2025Acoustic",
        "topic_id": "top_duffing_comp",
        "title": "微加工共振無線換能器中之聲學能量限域分析與非線性行為",
        "authors": "愛德華·樂芙 (A. E. H. Love), 雷蒙德·明德林 (R. D. Mindlin)",
        "year": 2025,
        "core_method": "厚度剪切振動彈性波解析模型 (Thickness-Shear Wave Analytical Modeling)",
        "bibtex": """@article{Love2025Acoustic,
  author = {Love, A. E. H. and Mindlin, R. D.},
  title = {Acoustic Energy Confinement in Micromachined Resonant Wireless Transducers under Nonlinear High-Drive Conditions},
  journal = {Journal of Applied Physics},
  year = {2025},
  volume = {138},
  pages = {204501},
  publisher = {AIP}
}""",
        "meta_data": {
            "theoretical_Q": 9800,
            "resonance_frequency_MHz": 26.8,
            "piezo_material": "PZT-5H",
            "citation_count": 8
        },
        "abstract": "本論文建立了高頻壓電諧振無線換能器在厚度剪切振動下的解析力學模型。研究表明，在高激勵電壓驅動下，壓電陶瓷的彈性常數會發生三階非線性漂移，進而觸發經典的 Duffing 非線性分歧（Bifurcation）現象，導致諧振峰值發生偏斜與多值狀態躍遷，顯著降低傳能系統的阻抗匹配穩定度。本研究推導了 Duffing 非線性分歧的啟始電壓閾值公式。",
        "urls": [
            {"type": "publisher", "link": "https://aip.scitation.org/journal/jap/mock_love_2025"},
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2501.00902.pdf"}
        ],
        "tags": ["piezoelectric", "acoustic-resonant", "non-linear", "bifurcation"]
    }
]

MOCK_SIMULATIONS = [
    {
        "sim_id": "sim_run_1",
        "paper_id": "semscholar_seong_2026",
        "run_config": {
            "f0_MHz": 28.5,
            "drive_voltage": 5.0,
            "piezo_material": "PZT-5H",
            "support_clamping": "Fixed_Edge"
        },
        "empirical_results": {
            "measured_Q": 11800,
            "measured_IL_dB": 2.8,
            "measured_coupling_k2": 0.085
        },
        "discrepancy_percentage": 1.67
    },
    {
        "sim_id": "sim_run_2",
        "paper_id": "semscholar_love_2025",
        "run_config": {
            "f0_MHz": 26.8,
            "drive_voltage": 12.0,
            "piezo_material": "PZT-5H",
            "support_clamping": "Free_Edge"
        },
        "empirical_results": {
            "measured_Q": 7500,
            "bifurcation_detected": True,
            "hysteresis_detected": True,
            "measured_IL_dB": 5.2
        },
        "discrepancy_percentage": 23.47
    }
]

MOCK_RED_TEAM_LOGS = [
    {
        "log_id": "crit_1",
        "paper_id": "semscholar_love_2025",
        "aspect_analyzed": "非線性 Duffing 分歧之匹配電路脆弱點",
        "reviewer_attack": "紅軍 Agent 指出：『在 12V 高激勵電壓下，換能器將進入非線性區，誘發 Duffing 分歧，導致阻抗匹配嚴重失配，傳能效率崩塌。論文並未提出實體電路層面的補償或預防策略，此為重大應用風險。』",
        "student_defense": "學生進行品位裁決後防禦：『我們在主權手稿 ms_journal_2026 中導入了動態鎖相環 (PLL) 頻率微調機制，即時偵測阻抗相位偏角，將驅動頻率動態鎖定在安全分支上；同時在 meta_data 中寫入電壓限制規則（不超過 8V），限制壓電材料進入深度非線性區，成功克服此脆弱點。』",
        "verdict": "PASS"
    }
]

MOCK_MY_MANUSCRIPTS = [
    {
        "manuscript_id": "ms_conf_2026",
        "topic_id": "top_piezo_modeling",
        "title": "基於 Mason 模型之高Q值聲學換能器物理特性建模與實現",
        "cite_key": "Wuulong2026Conf",
        "manuscript_type": "Conference",
        "evolution_stage": "Published",
        "previous_manuscript_id": None,
        "meta_data": {
            "conference_name": "IEEE International Ultrasonics Symposium (IUS)",
            "overleaf_url": "https://www.overleaf.com/project/mock_wuulong_conf_2026"
        }
    },
    {
        "manuscript_id": "ms_journal_2026",
        "topic_id": "top_duffing_comp",
        "title": "聲學共振無線傳能系統中非線性分歧之主動相位相匹配補償技術",
        "cite_key": "Wuulong2026Journal",
        "manuscript_type": "Journal",
        "evolution_stage": "Writing",
        "previous_manuscript_id": "ms_conf_2026",
        "meta_data": {
            "target_journal": "IEEE Transactions on Industrial Electronics",
            "overleaf_url": "https://www.overleaf.com/project/mock_wuulong_journal_2026"
        }
    }
]

MOCK_MANUSCRIPT_CITATIONS = [
    {
        "manuscript_id": "ms_conf_2026",
        "paper_id": "semscholar_seong_2026",
        "citation_context": "作為理論基底與 Mason 模型拓撲比對的物理基準論文。"
    },
    {
        "manuscript_id": "ms_journal_2026",
        "paper_id": "semscholar_love_2025",
        "citation_context": "作為 Duffing 非線性分歧啟始電壓閾值臨界分析與補償匹配對照的核心依據。"
    }
]

# ==============================================================================
# 資料庫自動化建立與初始化
# ==============================================================================

def init_db_schema_if_needed(db_path):
    """如果資料庫檔案不存在或未初始化，自動載入 schema.sql 進行結構初始化"""
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 檢查是否已存在 tables
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if len(tables) >= 5:
            conn.close()
            return # 已初始化
    except Exception:
        pass
        
    print(f"🌱 偵測到全新的資料庫，正在自動初始化 DDL 結構: {db_path}")
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        conn.commit()
        print("✅ 資料表結構初始化成功！")
    else:
        print(f"⚠️ 找不到 schema.sql 於 {schema_path}，無法自動初始化表格結構。")
    conn.close()

# ==============================================================================
# 主要核心功能
# ==============================================================================

def clean_and_rebuild_mock(db_path):
    """Wipe the database completely and populate v1.2.0 Three-Tier Chinese Mock Data."""
    init_db_schema_if_needed(db_path)
        
    print(f"🧹 正在連線至 SQLite 資料庫，準備清理舊範例資料: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 確保外鍵約束開啟
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. 依賴順序清理舊數據
    tables_to_clean = [
        "manuscript_citations", "my_manuscripts", "red_team_logs", 
        "local_simulations", "paper_tags", "paper_urls", "papers", 
        "topics", "projects", "directory_roots", "exploration_tasks"
    ]
    for table in tables_to_clean:
        try:
            cursor.execute(f"DELETE FROM {table};")
        except Exception as e:
            print(f"⚠️ 清理 {table} 表格時發生錯誤 (可能資料表尚未建立): {e}")
            
    print("✅ 資料清理完成。開始導入【主權星系架構 - 100% 中文硬核學術範例數據】...")
    
    try:
        # 1. 導入探勘任務 Ingestion Task
        task_id = "task_init_sandbox_2026"
        cursor.execute("""
        INSERT INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            task_id,
            "AR-WET acoustic resonant wireless energy",
            "OFFLINE_FALLBACK",
            3,
            "Antigravity-v1.2.0",
            None,
            json.dumps({"sandbox_rebuild": True, "rebuild_date": "2026-05-21"}, ensure_ascii=False)
        ))
        
        # 2. 導入專案 Project
        cursor.execute("""
        INSERT INTO projects (project_id, project_name, description, search_spec, architecture_spec, meta_data)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (
            MOCK_PROJECT["project_id"],
            MOCK_PROJECT["project_name"],
            MOCK_PROJECT["description"],
            json.dumps(MOCK_PROJECT["search_spec"], ensure_ascii=False),
            json.dumps(MOCK_PROJECT["architecture_spec"], ensure_ascii=False),
            json.dumps({"initiator": "Habar", "field": "Piezoelectric MEMS"}, ensure_ascii=False)
        ))
        
        # 3. 導入主題 Topics
        for t in MOCK_TOPICS:
            cursor.execute("""
            INSERT INTO topics (topic_id, project_id, topic_name, sequence_order, focus_spec, status, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                t["topic_id"],
                MOCK_PROJECT["project_id"],
                t["topic_name"],
                t["sequence_order"],
                json.dumps(t["focus_spec"], ensure_ascii=False),
                t["status"],
                json.dumps({"stage_notes": "自動導入之範例里程碑。"}, ensure_ascii=False)
            ))
            
        # 4. 導入抽象目錄根目錄對應 (directory_roots)
        roots_to_insert = [
            ("zotero_storage", "STUDENT_LOCAL", "wuulong", "/Users/wuulong/Zotero/storage/", {"description": "研究生個人 Zotero 本地 PDF 目錄"}),
            ("workspace_root", "STUDENT_LOCAL", "wuulong", "/Users/wuulong/github/bmad-pa/", {"description": "研究生個人專案代碼庫目錄"}),
            ("lab_nas", "LAB_SHARED", "vres_lab", "/Volumes/VRES_NAS/archive/", {"description": "VRES 實驗室公用 NAS 伺服器掛載路徑"}),
            ("remote_url", "GLOBAL_WEB", "internet", "", {"description": "網際網路線上遠端 HTTP 資源入口"})
        ]
        for root_key, owner_type, owner_name, abs_path, meta in roots_to_insert:
            cursor.execute("""
            INSERT INTO directory_roots (root_key, owner_type, owner_name, absolute_path, meta_data)
            VALUES (?, ?, ?, ?, ?);
            """, (root_key, owner_type, owner_name, abs_path, json.dumps(meta, ensure_ascii=False)))
            
        # 5. 導入背景論文 Papers & 標籤 & URLs
        for p in MOCK_PAPERS:
            cursor.execute("""
            INSERT INTO papers (paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                p["paper_id"],
                task_id,
                p["topic_id"],
                p["title"],
                p["authors"],
                p["year"],
                p["core_method"],
                p["cite_key"],
                p["bibtex"],
                json.dumps(p["meta_data"], ensure_ascii=False)
            ))
            
            # 導入 URLs
            for idx, url in enumerate(p["urls"]):
                link = url["link"]
                zotero_prefix = "file:///Users/wuulong/Zotero/storage/"
                if link.startswith(zotero_prefix):
                    root_key = "zotero_storage"
                    relative_link = link.replace(zotero_prefix, "")
                else:
                    root_key = "remote_url"
                    relative_link = link
                    
                cursor.execute("""
                INSERT INTO paper_urls (url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    f"url_{p['paper_id']}_{idx + 1}",
                    p["paper_id"],
                    root_key,
                    relative_link,
                    url["type"],
                    "DOWNLOADED" if root_key == "zotero_storage" else "PENDING",
                    102400 if root_key == "zotero_storage" else 0,
                    json.dumps({"verified": True}, ensure_ascii=False)
                ))
                
            # 導入 Tags
            for tag in p["tags"]:
                cursor.execute("""
                INSERT INTO paper_tags (paper_id, tag_name, meta_data)
                VALUES (?, ?, ?);
                """, (
                    p["paper_id"],
                    tag,
                    json.dumps({"source": "Auto-scout打標"}, ensure_ascii=False)
                ))
                
        # 5. 導入本地模擬與實測數據 Simulations
        for s in MOCK_SIMULATIONS:
            cursor.execute("""
            INSERT INTO local_simulations (sim_id, paper_id, run_config, empirical_results, discrepancy_percentage, meta_data)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                s["sim_id"],
                s["paper_id"],
                json.dumps(s["run_config"], ensure_ascii=False),
                json.dumps(s["empirical_results"], ensure_ascii=False),
                s["discrepancy_percentage"],
                json.dumps({"platform": "COMSOL v6.2", "sandbox": True}, ensure_ascii=False)
            ))
            
        # 6. 導入紅軍自審對抗日誌 Red Team Logs
        for r in MOCK_RED_TEAM_LOGS:
            cursor.execute("""
            INSERT INTO red_team_logs (log_id, paper_id, aspect_analyzed, reviewer_attack, student_defense, verdict, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                r["log_id"],
                r["paper_id"],
                r["aspect_analyzed"],
                r["reviewer_attack"],
                r["student_defense"],
                r["verdict"],
                json.dumps({"evaluator_agent": "Red_Team_Critique_v3"}, ensure_ascii=False)
            ))
            
        # 7. 導入我的主權手稿有向演化鏈 My Manuscripts & Citations
        for m in MOCK_MY_MANUSCRIPTS:
            cursor.execute("""
            INSERT INTO my_manuscripts (manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                m["manuscript_id"],
                m["topic_id"],
                m["title"],
                m["cite_key"],
                m["manuscript_type"],
                m["evolution_stage"],
                m["previous_manuscript_id"],
                json.dumps(m["meta_data"], ensure_ascii=False)
            ))
            
        for c in MOCK_MANUSCRIPT_CITATIONS:
            cursor.execute("""
            INSERT INTO manuscript_citations (manuscript_id, paper_id, citation_context, meta_data)
            VALUES (?, ?, ?, ?);
            """, (
                c["manuscript_id"],
                c["paper_id"],
                c["citation_context"],
                json.dumps({"verified_in_tex": True}, ensure_ascii=False)
            ))
            
        conn.commit()
        print("🎉 恭喜！【三層主權知識星系架構 v1.2.0】100% 中文硬核學術範例數據導入成功！")
        print("----------------------------------------------------------------------")
        print(f"📊 已生成 10 個完整關聯表格")
        print("----------------------------------------------------------------------")
        
    except Exception as e:
        print(f"❌ 導入範例數據失敗: {e}")
        conn.rollback()
    finally:
        conn.close()

# ==============================================================================
# 線上 ArXiv REST API 檢索與 Ingestion 落地邏輯
# ==============================================================================

def query_arxiv_online(query_str, limit=5):
    """連線至 ArXiv API 進行真實檢索，並解析 XML 返回結構化資料"""
    encoded_query = urllib.parse.quote(query_str)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={limit}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        # 解析 XML Feed
        root = ET.fromstring(xml_data)
        
        # Namespace 定義
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        papers_found = []
        for entry in entries:
            id_url = entry.find('atom:id', ns).text.strip()
            # 取得 ArXiv ID
            arxiv_id = id_url.split('/abs/')[-1].split('v')[0]
            
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            
            authors_nodes = entry.findall('atom:author', ns)
            authors_list = [node.find('atom:name', ns).text.strip() for node in authors_nodes]
            authors = ", ".join(authors_list)
            
            published_str = entry.find('atom:published', ns).text.strip()
            year = int(published_str[:4])
            
            # 尋找 PDF 下載網址
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            for link_node in entry.findall('atom:link', ns):
                if link_node.attrib.get('title') == 'pdf':
                    pdf_url = link_node.attrib.get('href')
                    break
                    
            # 建立 cite_key (例如 Seong2026)
            first_author = authors_list[0].split()[-1] if authors_list else "Unknown"
            # 清理非英文字元
            first_author = "".join(c for c in first_author if c.isalnum())
            cite_key = f"{first_author}{year}{arxiv_id[:4]}"
            
            # 生成 BibTeX
            bibtex = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}}
}}"""

            papers_found.append({
                "paper_id": f"arxiv_{arxiv_id}",
                "cite_key": cite_key,
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": abstract,
                "pdf_url": pdf_url,
                "bibtex": bibtex,
                "tags": ["arxiv", "auto-scout"]
            })
            
        return papers_found
    except Exception as e:
        print(f"⚠️ 真實網路連線失敗或超時 ({e})，準備降級至離線高保真 Sandbox 模擬結構...")
        return None

def save_papers_to_db(db_path, papers, query_str):
    """將真實查詢到的論文結構化存入 SQLite 資料庫中 (維持 10 表聯邦約束)"""
    init_db_schema_if_needed(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        # 1. 建立 Ingestion 採集任務 (Lineage)
        task_id = f"task_online_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute("""
        INSERT INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            task_id,
            query_str,
            "ONLINE",
            len(papers),
            "Antigravity-v1.2.0-RealEngine",
            None,
            json.dumps({"engine": "arXiv_API", "run_at": datetime.now().isoformat()}, ensure_ascii=False)
        ))
        
        # 2. 保障預設專案與預設子主題存在 (確保外鍵約束安全)
        cursor.execute("SELECT project_id FROM projects WHERE project_id = 'prj_general';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO projects (project_id, project_name, description, search_spec, architecture_spec, meta_data)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                "prj_general",
                "全域研究探勘專案",
                "匯總所有非特定專案的真實線上文獻檢索成果。",
                json.dumps({"keywords": ["general"]}, ensure_ascii=False),
                json.dumps({"target": "knowledge_expansion"}, ensure_ascii=False),
                json.dumps({"auto_created": True}, ensure_ascii=False)
            ))
            
        cursor.execute("SELECT topic_id FROM topics WHERE topic_id = 'top_general';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO topics (topic_id, project_id, topic_name, sequence_order, focus_spec, status, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                "top_general",
                "prj_general",
                "全域學術主題探底",
                1,
                json.dumps({"focus_variables": ["general_knowledge"], "equations": []}, ensure_ascii=False),
                "ACTIVE",
                json.dumps({"auto_created": True}, ensure_ascii=False)
            ))
            
        # 3. 確保遠端 URL 根映射存在
        cursor.execute("SELECT root_key FROM directory_roots WHERE root_key = 'remote_url';")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO directory_roots (root_key, owner_type, owner_name, absolute_path, meta_data)
            VALUES (?, ?, ?, ?, ?);
            """, ("remote_url", "GLOBAL_WEB", "internet", "", json.dumps({"description": "線上遠端網址資源入口"}, ensure_ascii=False)))
            
        # 4. 逐一寫入論文、URLs 與標籤
        inserted_count = 0
        for p in papers:
            # 檢查是否已存在
            cursor.execute("SELECT paper_id FROM papers WHERE paper_id = ?;", (p["paper_id"],))
            if cursor.fetchone():
                continue # 避免重複寫入
                
            cursor.execute("""
            INSERT INTO papers (paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                p["paper_id"],
                task_id,
                "top_general",
                p["title"],
                p["authors"],
                p["year"],
                "線上文獻自動擷取",
                p["cite_key"],
                p["bibtex"],
                json.dumps({"abstract_snippet": p["abstract"][:200] + "..."}, ensure_ascii=False)
            ))
            
            # 寫入 URL
            cursor.execute("""
            INSERT INTO paper_urls (url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                f"url_{p['paper_id']}_pdf",
                p["paper_id"],
                "remote_url",
                p["pdf_url"],
                "arxiv_pdf",
                "PENDING",
                0,
                json.dumps({"online_discovered": True}, ensure_ascii=False)
            ))
            
            # 寫入自動打標
            for tag in p["tags"]:
                cursor.execute("""
                INSERT INTO paper_tags (paper_id, tag_name, meta_data)
                VALUES (?, ?, ?);
                """, (p["paper_id"], tag, json.dumps({"engine": "PaperScout_Auto_Tagger"}, ensure_ascii=False)))
                
            inserted_count += 1
            
        conn.commit()
        print(f"💾 資料庫沉澱成功！共新增 {inserted_count} 筆真實背景文獻至 SQLite ({db_path})！")
    except Exception as e:
        print(f"❌ 寫入真實論文至資料庫時出錯: {e}")
        conn.rollback()
    finally:
        conn.close()

# ==============================================================================
# 主執行流程
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Paper Scout: 線上學術文獻 Scout 代理人工具")
    parser.add_argument("--query", type=str, help="搜尋論文關鍵字")
    parser.add_argument("--source", type=str, default="all", choices=["arxiv", "sem-scholar", "all"], help="文獻檢索源")
    parser.add_argument("--limit", type=int, default=5, help="每單一來源最大返回筆數 (預設: 5)")
    parser.add_argument("--save-db", action="store_true", help="將篩選出的文獻沉澱寫入本地 SQLite")
    parser.add_argument("--output", type=str, default="markdown", choices=["markdown", "json"], help="輸出格式")
    parser.add_argument("--force-mock", action="store_true", help="強制啟用本地模擬模式，不進行網路呼叫")
    parser.add_argument("--rebuild-mock", action="store_true", help="【極客專用】一鍵清理資料庫並重建 100% 中文高階範例數據")
    parser.add_argument("--db", type=str, help="指定目標 SQLite 資料庫路徑 (優先於環境變數 RESEARCH_DB)")
    
    args = parser.parse_args()
    
    # 智慧資料庫路徑判定 (1. args ➔ 2. env ➔ 3. default)
    db_path = args.db or os.environ.get("RESEARCH_DB") or DEFAULT_DB_PATH
    
    # 判斷是否為一鍵重建範例資料
    if args.rebuild_mock:
        clean_and_rebuild_mock(db_path)
        return

    if not args.query:
        print("❌ 錯誤：請提供 --query 參數以進行檢索，或使用 --rebuild-mock 進行範例數據重建。")
        return

    # 執行資料庫自動 initialization
    init_db_schema_if_needed(db_path)

    # 執行真實線上檢索或降級 Fallback
    all_papers = []
    real_online_papers = None
    
    if not args.force_mock:
        real_online_papers = query_arxiv_online(args.query, args.limit)
        
    if real_online_papers:
        # 使用真實線上搜尋結果
        print(f"🎉 成功從 ArXiv 實體獲取 {len(real_online_papers)} 筆真實論文資料！")
        for p in real_online_papers:
            all_papers.append({
                "paper_id": p["paper_id"],
                "cite_key": p["cite_key"],
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "abstract": p["abstract"],
                "pdf_url": p["pdf_url"],
                "tags": p["tags"]
            })
            
        # 若指定了 --save-db，將其實體沉澱落庫！
        if args.save_db:
            save_papers_to_db(db_path, real_online_papers, args.query)
    else:
        # 回歸沙盒 Mock 離線數據
        print("⚠️ 啟用本地高保真離線沙盒數據...")
        for p in MOCK_PAPERS:
            all_papers.append({
                "paper_id": p["paper_id"],
                "cite_key": p["cite_key"],
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "abstract": p["abstract"],
                "pdf_url": p["urls"][0]["link"],
                "tags": p["tags"]
            })

    # 輸出結果
    if args.output == "json":
        print(json.dumps(all_papers, indent=2, ensure_ascii=False))
    else:
        # Markdown 表格輸出
        print(f"\n### 📚 Paper Scout 線上文獻檢索成果 (資料庫: {os.path.basename(db_path)})")
        print("| 來源 | 發表年份 | 標題 | 作者 | 引用/連結 |")
        print("| :--- | :---: | :--- | :--- | :--- |")
        for p in all_papers:
            url = p.get('pdf_url', '#')
            source = "ArXiv API" if real_online_papers else "Mock Sandbox"
            print(f"| {source} | {p['year']} | [{p['title']}]({url}) | {p['authors']} | 連結 |")

if __name__ == "__main__":
    main()
