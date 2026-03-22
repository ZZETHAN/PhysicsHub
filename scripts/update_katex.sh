#!/bin/bash
#
# 批量更新HTML文件使用本地KaTeX
#

echo "🔄 更新所有HTML文件使用本地KaTeX..."

cd ~/Desktop/PhysicsHub/units

for file in $(find . -name "*.html" -type f); do
    if grep -q "cdn.jsdelivr.net.*katex" "$file"; then
        # 替换CDN为本地路径
        sed -i '' 's|https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/|../../assets/katex/|g' "$file"
        echo "✅ 已更新: $file"
    fi
done

echo ""
echo "🎉 所有文件已更新为本地KaTeX"
echo "📁 本地KaTeX位置: ~/Desktop/PhysicsHub/assets/katex/"
