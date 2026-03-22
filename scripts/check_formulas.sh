#!/bin/bash
#
# PhysicsHub 公式质量检查脚本
# 运行此脚本检查所有HTML文件的公式渲染配置
#

echo "🔍 PhysicsHub 公式质量检查"
echo "============================"
echo ""

cd ~/Desktop/PhysicsHub/units

ERRORS=0

for unit in ch*/; do
    echo "📁 检查 $unit"
    
    for file in "$unit"*.html; do
        [ -f "$file" ] || continue
        fname=$(basename "$file")
        
        # 检查是否包含公式
        if grep -q '\\\\(' "$file" 2>/dev/null || grep -q '\\$\\$' "$file" 2>/dev/null; then
            
            # 检查1: 必须使用MathJax
            if ! grep -q "MathJax-script" "$file"; then
                echo "  ❌ $fname: 有公式但未配置MathJax"
                ERRORS=$((ERRORS+1))
                continue
            fi
            
            # 检查2: 必须使用本地MathJax
            if ! grep -q "assets/mathjax/tex-chtml.min.js" "$file"; then
                echo "  ❌ $fname: 使用CDN而非本地MathJax"
                ERRORS=$((ERRORS+1))
                continue
            fi
            
            # 检查3: 必须使用本地字体
            if ! grep -q "fontURL.*mathjax" "$file"; then
                echo "  ⚠️  $fname: 未配置本地字体路径"
                ERRORS=$((ERRORS+1))
                continue
            fi
            
            # 检查4: 不能使用KaTeX
            if grep -q "katex" "$file" 2>/dev/null; then
                echo "  ❌ $fname: 混用KaTeX"
                ERRORS=$((ERRORS+1))
                continue
            fi
            
            # 检查5: 不能有纯文本formula
            if grep -q 'class="formula"' "$file" 2>/dev/null; then
                echo "  ❌ $fname: 存在纯文本公式(class=formula)"
                ERRORS=$((ERRORS+1))
                continue
            fi
            
            echo "  ✅ $fname: 公式配置正确"
        fi
    done
    echo ""
done

echo "============================"
if [ $ERRORS -eq 0 ]; then
    echo "🎉 所有检查通过！公式配置规范。"
    exit 0
else
    echo "⚠️  发现 $ERRORS 个问题，请修复。"
    exit 1
fi
