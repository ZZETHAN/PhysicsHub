#!/usr/bin/env python3
"""
深度修复HTML中的纯文本公式
"""

import re
import sys

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计数器
    count = 0
    
    # 查找所有 class="formula" 的div
    def replace_formula(match):
        nonlocal count
        count += 1
        
        formula_content = match.group(1)
        # 处理内容
        formula_content = formula_content.replace('<br>', '\\n')
        formula_content = formula_content.replace('<br />', '\\n')
        formula_content = formula_content.replace('<br/>', '\\n')
        formula_content = formula_content.strip()
        
        # 转换特殊字符
        formula_content = formula_content.replace('²', '^2')
        formula_content = formula_content.replace('³', '^3')
        formula_content = formula_content.replace('°', '^\\circ')
        formula_content = formula_content.replace('ω', '\\omega ')
        formula_content = formula_content.replace('θ', '\\theta ')
        formula_content = formula_content.replace('μ', '\\mu ')
        formula_content = formula_content.replace('≥', '\\geq ')
        formula_content = formula_content.replace('≤', '\\leq ')
        formula_content = formula_content.replace('≈', '\\approx ')
        formula_content = formula_content.replace('√', '\\sqrt ')
        
        # 简单替换分数 a/b 为 \\frac{a}{b}
        # 分行处理
        lines = formula_content.split('\\n')
        new_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 分数转换
            line = re.sub(r'(\w+)\s*/\s*(\w+)', r'\\frac{\1}{\2}', line)
            new_lines.append(line)
        
        if len(new_lines) == 1:
            mathjax = f'\\\\[{new_lines[0]}\\\\]'
        else:
            mathjax = '\\\\[' + ' \\\\ '.join(new_lines) + '\\\\]'
        
        return f'<div class="formula-box" style="background: white; border: 2px solid var(--primary); border-radius: var(--radius); padding: var(--space-4); margin: var(--space-4) 0; text-align: center; font-size: 1.2rem;">{mathjax}</div>'
    
    # 使用非贪婪匹配，DOTALL模式
    new_content = re.sub(
        r'<div class="formula">\s*(.*?)\s*</div>',
        replace_formula,
        content,
        flags=re.DOTALL
    )
    
    # 添加MathJax样式
    if 'mjx-container' not in new_content:
        new_content = new_content.replace(
            '</style>',
            '        mjx-container { font-size: 115% !important; }\n    </style>'
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已修复 {count} 个公式: {filepath}")

if __name__ == "__main__":
    for filepath in sys.argv[1:]:
        fix_file(filepath)
