#!/bin/bash
#
# 批量修复所有HTML文件的公式渲染
# 统一使用本地 MathJax
#

echo "🔧 批量修复公式渲染..."

cd ~/Desktop/PhysicsHub/units

for file in $(find . -name "*.html" -type f); do
    # 检查是否包含公式
    if grep -q '\\\\(' "$file" 2>/dev/null || grep -q '\$\$' "$file" 2>/dev/null; then
        
        # 检查是否已使用MathJax本地版
        if grep -q "assets/mathjax/tex-chtml.min.js" "$file"; then
            echo "✅ $file - 已是本地MathJax"
        elif grep -q "cdn.jsdelivr.net.*mathjax" "$file"; then
            echo "🔄 $file - 从CDN切换到本地..."
            sed -i '' 's|https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.min.js|../../assets/mathjax/tex-chtml.min.js|g' "$file"
        elif grep -q "katex" "$file"; then
            echo "🔄 $file - 从KaTeX切换到MathJax..."
            # 移除KaTeX引用
            sed -i '' '/katex/d' "$file"
            sed -i '' '/auto-render/d' "$file"
            # 移除KaTeX配置脚本
            sed -i '' '/renderMathInElement/d' "$file"
            sed -i '' '/delimiters/,/throwOnError/d' "$file"
            
            # 添加MathJax（在</body>前）
            sed -i '' 's|</body>|    <!-- MathJax 本地配置 -->\n    <script>\n        window.MathJax = {\n            tex: {\n                inlineMath: [[\x27\\\\(\x27, \x27\\\\)\x27]],\n                displayMath: [[\x27\\\\[\x27, \x27\\\\]\x27]]\n            },\n            chtml: {\n                scale: 1.1,\n                fontURL: \x27../../assets/mathjax/output/chtml/fonts/woff-v2\x27\n            }\n        };\n    </script>\n    <script id="MathJax-script" async src="../../assets/mathjax/tex-chtml.min.js"></script>\n</body>|g' "$file"
        fi
    fi
done

echo ""
echo "🎉 所有HTML文件公式渲染已统一修复"
