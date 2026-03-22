#!/usr/bin/env python3
"""
从PPT文件中提取图像
文档工程师工具
"""

import os
import sys
from pathlib import Path

# 课件路径
CH12_PATH = "/Users/ethanzhao/Desktop/zyh课件/12. Motion in a circle/材料"
CH13_PATH = "/Users/ethanzhao/Desktop/zyh课件/13. Gravitional field/材料"
OUTPUT_PATH = "/Users/ethanzhao/Desktop/PhysicsHub/assets/images"

def extract_images_from_pptx(pptx_path, output_dir):
    """
    从PPTX文件中提取图像
    PPTX本质上是ZIP文件，media文件夹中包含图像
    """
    import zipfile
    
    os.makedirs(output_dir, exist_ok=True)
    extracted = []
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith('ppt/media/'):
                    # 提取文件
                    filename = os.path.basename(file)
                    if filename:
                        zip_ref.extract(file, output_dir)
                        src = os.path.join(output_dir, file)
                        dst = os.path.join(output_dir, filename)
                        if os.path.exists(src):
                            os.rename(src, dst)
                            extracted.append(dst)
        
        # 清理临时目录
        for root, dirs, files in os.walk(output_dir):
            if 'ppt' in dirs:
                import shutil
                shutil.rmtree(os.path.join(root, 'ppt'))
                
    except Exception as e:
        print(f"Error extracting {pptx_path}: {e}")
        
    return extracted

def main():
    print("🔧 文档工程师：提取PPT图像")
    print("=" * 50)
    
    # 提取Ch 12图像
    print("\n📂 提取Ch 12图像...")
    ch12_images = []
    for file in os.listdir(CH12_PATH):
        if file.endswith('.pptx'):
            pptx_file = os.path.join(CH12_PATH, file)
            extracted = extract_images_from_pptx(pptx_file, f"{OUTPUT_PATH}/ch12")
            ch12_images.extend(extracted)
            print(f"  ✅ {file}: {len(extracted)} images")
    
    # 提取Ch 13图像
    print("\n📂 提取Ch 13图像...")
    ch13_images = []
    for file in os.listdir(CH13_PATH):
        if file.endswith('.pptx'):
            pptx_file = os.path.join(CH13_PATH, file)
            extracted = extract_images_from_pptx(pptx_file, f"{OUTPUT_PATH}/ch13")
            ch13_images.extend(extracted)
            print(f"  ✅ {file}: {len(extracted)} images")
    
    print("\n" + "=" * 50)
    print(f"✅ 总计提取: {len(ch12_images) + len(ch13_images)} 张图像")
    print(f"   Ch 12: {len(ch12_images)} 张")
    print(f"   Ch 13: {len(ch13_images)} 张")
    print(f"\n📁 保存位置: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
