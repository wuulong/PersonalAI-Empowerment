import os
import re
from datetime import datetime

def get_file_sort_key(filename):
    """
    為書名檔案生成排序鍵。
    格式預期為:
    - 00_toc.md -> (0, 0)
    - Chapter_1_1.md -> (1, 1)
    - Chapter_7.md -> (7, 0)
    - Chapter_8_10.md -> (8, 10)
    """
    if filename == "00_toc.md":
        return (0, 0)
    
    # 匹配 Chapter_X_Y.md 或 Chapter_X.md
    match = re.match(r"Chapter_(\d+)(?:_(\d+))?\.md", filename)
    if match:
        chapter = int(match.group(1))
        section = int(match.group(2)) if match.group(2) else 0
        return (chapter, section)
    
    # 其他檔案排在最後
    return (999, 999)

def merge_book():
    base_dir = "/Users/wuulong/github/bmad-pa/events/AIBooks/PersonalEmpowerment/PersonalAI-Empowerment"
    output_file = os.path.join(base_dir, "FullBook_Personal_AI_Empowerment.md")
    
    files = [f for f in os.listdir(base_dir) if f.endswith(".md") and f not in ["README.md", "LICENSE"]]
    
    # 根據自定義邏輯排序
    sorted_files = sorted(files, key=get_file_sort_key)
    
    # 移除 (999, 999) 的檔案，除非真的有需要（目前排除了 README.md）
    sorted_files = [f for f in sorted_files if get_file_sort_key(f) != (999, 999)]

    print(f"正在合併 {len(sorted_files)} 個檔案...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        outfile.write(f"# 《個人賦能》完整全書\n\n> 本文件由自動化腳本合併而成，產生時間：{current_time}\n\n---\n\n")
        
        for filename in sorted_files:
            file_path = os.path.join(base_dir, filename)
            print(f"  - 加入: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                
                # 在章節之間加入分隔線與原始檔名註記（方便下一棒處理）
                if filename != "00_toc.md":
                    outfile.write(f"\n\n<!-- PAGE_BREAK: {filename} -->\n\n---\n\n")
                
                outfile.write(content)
                outfile.write("\n") # 確保結尾有換行

    print(f"\n合併完成！輸出檔案：{output_file}")

if __name__ == "__main__":
    merge_book()
