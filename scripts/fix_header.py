#!/usr/bin/env python3
"""
Fix header Units bar position to original location
Restore Units button to be right-aligned using flex: 1 wrapper
"""

import os
import re

UNITS = {
    'ch12': {'num': '12', 'title': 'Motion in a Circle', 'color': '#1d4ed8'},
    'ch13': {'num': '13', 'title': 'Gravitational Field', 'color': '#7c3aed'},
    'ch14': {'num': '14', 'title': 'Temperature', 'color': '#ea580c'},
    'ch15': {'num': '15', 'title': 'Ideal Gases', 'color': '#16a34a'},
    'ch16': {'num': '16', 'title': 'Thermodynamics', 'color': '#dc2626'},
    'ch17': {'num': '17', 'title': 'Oscillations', 'color': '#0891b2'},
    'ch18': {'num': '18', 'title': 'Electric Fields', 'color': '#1e40af'},
    'ch19': {'num': '19', 'title': 'Capacitance', 'color': '#7c3aed'},
    'ch20': {'num': '20', 'title': 'Magnetic Fields', 'color': '#0891b2'},
    'ch21': {'num': '21', 'title': 'Alternating Currents', 'color': '#0f766e'},
    'ch22': {'num': '22', 'title': 'Quantum Physics', 'color': '#be185d'},
}

def get_unit_links(unit_id):
    links = []
    for uid in ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22']:
        info = UNITS[uid]
        is_active = uid == unit_id
        dot = f'<span style="width: 8px; height: 8px; background: {info["color"]}; border-radius: 50%;"></span>' if is_active else ''
        hover_bg = f"#{info['color']}22" if not is_active else 'transparent'
        links.append(
            f'<a href="../{uid}/index.html" style="display: flex; align-items: center; padding: 10px 12px; border-radius: 8px; text-decoration: none; font-size: 13px; color: #475569; margin-bottom: 2px;" onmouseover="this.style.background=\'{hover_bg}\'" onmouseout="this.style.background=\'transparent\'">'
            f'<span style="font-weight: 600; min-width: 52px; color: {info["color"] if is_active else "#475569"};">Unit {info["num"]}</span>'
            f'<span style="color: #64748b; flex: 1;">{info["title"]}</span>'
            f'{dot}'
            f'</a>'
        )
    return '\n'.join(links)

def fix_units_header(content, unit_id):
    """Fix Units header to be right-aligned with flex: 1 wrapper"""
    info = UNITS[unit_id]
    color = info['color']
    unit_links = get_unit_links(unit_id)
    
    # The correct structure: Units button in flex:1 wrapper, then authBtn outside
    correct_right = f'''<div style="display: flex; align-items: center; flex: 1; justify-content: flex-end; padding-right: 8px;">
                <div style="position: relative;">
                    <button onclick="toggleUnitNav()" id="unitNavBtn" style="background: linear-gradient(135deg, {color}22 0%, white 100%); border: 1px solid {color}; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 500; color: {color}; display: flex; align-items: center; gap: 6px;">
                        <span>Units</span>
                        <span style="font-size: 10px;">▼</span>
                    </button>
                    <div id="unitNavDropdown" style="display: none; position: absolute; top: calc(100% + 8px); right: 50%; transform: translateX(50%); background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px; min-width: 220px; max-width: 90vw; box-shadow: 0 10px 40px rgba(0,0,0,0.15); z-index: 1001;">
                        <div style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; padding: 8px 12px; border-bottom: 1px solid #f1f5f9; margin-bottom: 4px;">A2 Physics Units</div>
                        {unit_links}
                    </div>
                </div>
            </div>
            <div id="authBtn"></div>'''
    
    # Pattern 1: Units without flex wrapper (my broken version)
    # Units button directly in a position:relative div, authBtn after
    pattern1 = r'<div style="position: relative;">\s*<button onclick="toggleUnitNav\(\)" id="unitNavBtn"[^>]*>.*?</div>\s*</div>\s*<div id="authBtn"></div>'
    
    # Pattern 2: Units with flex wrapper but wrong structure
    pattern2 = r'<div style="[^"]*flex:\s*1[^"]*justify-content:\s*flex-end[^"]*">\s*<div style="position: relative;">\s*<button[^>]*>.*?</div>\s*</div>\s*</div>\s*<div id="authBtn"></div>'
    
    for pattern in [pattern1, pattern2]:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + correct_right + content[match.end():]
            return content, True
    
    return content, False

def process_file(filepath, unit_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, fixed = fix_units_header(content, unit_id)
    
    if fixed:
        print(f"  Fixed header for {unit_id}")
    else:
        print(f"  Pattern not found for {unit_id}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixed

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Fixing Units header position for A2 units (ch12-ch22)...")
    
    for unit_id in UNITS.keys():
        filepath = os.path.join(base_path, unit_id, 'index.html')
        if os.path.exists(filepath):
            print(f"Processing {unit_id}...")
            process_file(filepath, unit_id)
        else:
            print(f"  File not found: {filepath}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()