#!/usr/bin/env python3
"""
批量修复HTML中的纯文本公式为MathJax格式
"""

import re
import sys
import os

def fix_formulas_in_file(filepath):
    """修复单个文件中的公式"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有纯文本formula类
    if 'class="formula"' not in content:
        print(f"✅ {filepath} - 无需修复")
        return
    
    # 替换纯文本formula为MathJax格式
    # 模式1: <div class="formula">...</div> 转换为 \[ ... \]
    def replace_formula_div(match):
        formula = match.group(1)
        # 清理公式内容
        formula = formula.strip()
        # 转换常见符号
        formula = formula.replace('²', '^2')
        formula = formula.replace('³', '^3')
        formula = formula.replace('ω', '\\omega ')
        formula = formula.replace('θ', '\\theta ')
        formula = formula.replace('μ', '\\mu ')
        formula = formula.replace('≥', '\\geq ')
        formula = formula.replace('≤', '\\leq ')
        formula = formula.replace('√(', '\\sqrt{')
        formula = formula.replace('√', '\\sqrt ')
        # 分数转换 a/b -> \frac{a}{b}
        formula = re.sub(r'(\w+)\s*/\s*(\w+)', r'\\frac{\1}{\2}', formula)
        # 括号补全
        if formula.count('{') > formula.count('}'):
            formula += '}' * (formula.count('{') - formula.count('}'))
        return f'\\[\n                    {formula}\n                \\]'
    
    content = re.sub(r'<div class="formula">\s*([^\u003c]+?)\s*</div>', replace_formula_div, content)
    
    # 模式2: 简单行内公式（如步骤中的方程）
    # 转换 T cos θ = mg 这样的格式
    def replace_inline_formula(match):
        text = match.group(0)
        # 如果包含数学符号，转换为行内公式
        if any(c in text for c in ['=', '+', '-', '/', 'θ', 'ω', 'μ', '²', '√']):
            # 替换符号
            text = text.replace('²', '^2')
            text = text.replace('ω', '\\omega ')
            text = text.replace('θ', '\\theta ')
            text = text.replace('μ', '\\mu ')
            text = text.replace('≥', '\\geq ')
            text = text.replace('≤', '\\leq ')
            text = text.replace('√', '\\sqrt ')
            # 分数
            text = re.sub(r'(\w+)\s*/\s*(\w+)', r'\\frac{\1}{\2}', text)
            return f'\\({text}\\)'
        return text
    
    # 修复步骤中的公式
    content = re.sub(r'<div class="step">([^\u003c]*(?:<br>[^\u003c]*)*)</div>', 
                     lambda m: m.group(0).replace(m.group(1), 
                     re.sub(r'([A-Za-zωθμ\s\+\-=\(\)/²³√]+)', replace_inline_formula, m.group(1))), content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"🔄 {filepath} - 已修复")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 默认修复ch12和ch13的所有html
        base_dir = os.path.expanduser("~/Desktop/PhysicsHub/units")
        for unit in ['ch12', 'ch13']:
            unit_dir = os.path.join(base_dir, unit)
            if os.path.exists(unit_dir):
                for file in os.listdir(unit_dir):
                    if file.endswith('.html'):
                        fix_formulas_in_file(os.path.join(unit_dir, file))
    else:
        for filepath in sys.argv[1:]:
            fix_formulas_in_file(filepath)
