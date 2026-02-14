import os
import re

# 定義台灣語感校準映射表
# 格式: { "錯誤詞彙": "建議修正詞彙" }
LINGUISTIC_MAPPING = {
    "代碼": "程式碼",
    "數據": "資料",
    "項目": "專案",
    "運行": "執行",
    "生成": "產出",
    "信息": "資訊",
    "軟件": "軟體",
    "硬件": "硬體",
    "硬盤": "硬碟",
    "內存": "記憶體",
    "設置": "設定",
    "對標": "對位",
    "武裝": "裝備",
    "網絡": "網路",
    "屏幕": "螢幕",
    "設備": "裝置",
    "脫水": "擷取重點",
    "最佳化": "最佳化", # 確保一致性
    "優化": "最佳化",
    "實際情況": "實際",
}

def align_content(content):
    """
    對內容進行校準。會避開一般代碼塊，但會處理 mermaid 代碼塊與一般文本。
    """
    # 使用正則表達式切分代碼塊與非代碼塊
    # 這裡會匹配 ```...``` 區塊
    parts = re.split(r'(```[\s\S]*?```)', content)
    
    new_parts = []
    for part in parts:
        # 如果是代碼塊
        if part.startswith('```'):
            # 如果是 mermaid 塊，我們選擇進行校準（因為這是給人讀的圖表）
            if part.startswith('```mermaid'):
                temp_part = part
                for wrong, right in LINGUISTIC_MAPPING.items():
                    temp_part = temp_part.replace(wrong, right)
                new_parts.append(temp_part)
            else:
                # 其他代碼塊（python, shell 等）保持原樣
                new_parts.append(part)
        else:
            # 如果是非代碼塊，執行映射替換
            temp_part = part
            for wrong, right in LINGUISTIC_MAPPING.items():
                temp_part = temp_part.replace(wrong, right)
            new_parts.append(temp_part)
            
    return "".join(new_parts)

def process_directory(target_dir):
    print(f"🚀 開始全書語感校準風暴...")
    print(f"目標目錄: {target_dir}")
    
    files_processed = 0
    replacements_made = 0
    
    for root, dirs, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith(".md") and filename not in ["LICENSE", "README.md"]:
                file_path = os.path.join(root, filename)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()
                
                new_content = align_content(original_content)
                
                if new_content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  [FIXED] {filename}")
                    files_processed += 1
                else:
                    # print(f"  [CLEAN] {filename}")
                    pass
    
    print(f"\n✅ 校準完成！")
    print(f"共處理檔案數: {files_processed}")

if __name__ == "__main__":
    # 設定目標目錄為書稿與規劃文件所在路徑
    TARGET_DIR = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment"
    process_directory(TARGET_DIR)
