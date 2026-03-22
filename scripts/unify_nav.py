#!/usr/bin/env python3
"""
Fix header and unify sidebar navigation across A2 Physics units (ch12-ch22)
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

SIDEBAR_CSS = '''
        .sidebar-nav {
            position: sticky;
            top: 80px;
            height: fit-content;
            background: white;
            border-radius: 12px;
            padding: 16px;
            border: 1px solid #e2e8f0;
        }
        .nav-section-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            margin-bottom: 12px;
        }
        .nav-list { list-style: none; padding: 0; margin: 0 0 20px 0; }
        .nav-item { margin-bottom: 4px; }
        .nav-link {
            display: block;
            padding: 8px 12px;
            color: #475569;
            text-decoration: none;
            border-radius: 6px;
            font-size: 13px;
            transition: all 0.2s;
            cursor: pointer;
        }
        .nav-link:hover { background: #f1f5f9; color: var(--primary-color, #1d4ed8); }
        .nav-link.active { background: var(--light-color, #dbeafe); color: var(--primary-color, #1d4ed8); font-weight: 500; }
'''

UNIT_LINKS_CSS = '''
        .unit-nav-link { display: flex; align-items: center; padding: 10px 12px; border-radius: 8px; text-decoration: none; font-size: 13px; color: #475569; margin-bottom: 2px; transition: background 0.15s; }
        .unit-nav-link:hover { background: #f1f5f9; }
        .unit-nav-link.active { background: {color}22; color: {color}; }
        .unit-nav-link .unit-num {{ font-weight: 600; min-width: 52px; }}
        .unit-nav-link .unit-title {{ color: #64748b; flex: 1; }}
        .unit-nav-link.active .unit-title {{ color: {color}; }}
'''

def get_unit_links(unit_id):
    links = []
    for uid in ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22']:
        info = UNITS[uid]
        is_active = uid == unit_id
        dot = f'<span style="width: 8px; height: 8px; background: {info["color"]}; border-radius: 50%;"></span>' if is_active else ''
        links.append(
            f'<a href="../{uid}/index.html" class="unit-nav-link{" active" if is_active else ""}">'
            f'<span class="unit-num" style="color: {info["color"] if is_active else "#475569"};">Unit {info["num"]}</span>'
            f'<span class="unit-title">{info["title"]}</span>'
            f'{dot}'
            f'</a>'
        )
    return '\n'.join(links)

def get_header_right(unit_id):
    info = UNITS[unit_id]
    color = info['color']
    unit_links = get_unit_links(unit_id)
    return f'''<div style="display: flex; align-items: center; flex: 1; justify-content: flex-end; padding-right: 8px;">
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

def fix_header(content, unit_id):
    info = UNITS[unit_id]
    color = info['color']
    
    new_right = get_header_right(unit_id)
    
    old_pattern = r'<div style="position: relative;">\s*<button onclick="toggleUnitNav\(\)" id="unitNavBtn"[^<]*</button>\s*<div id="unitNavDropdown"[^<]*</div>\s*</div>\s*<div id="authBtn"></div>'
    
    match = re.search(old_pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_right + content[match.end():]
        return content, True
    
    old_pattern2 = r'<div style="position: relative;">\s*<button onclick="toggleUnitNav\(\)" id="unitNavBtn"[^>]*>.*?</div>\s*</div>\s*<div id="authBtn"></div>'
    match = re.search(old_pattern2, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_right + content[match.end():]
        return content, True
    
    return content, False

def get_sidebar_nav(unit_id, sections, homework_link):
    info = UNITS[unit_id]
    color = info['color']
    
    section_links = []
    for sec in sections:
        section_links.append(
            f'<li class="nav-item"><a href="javascript:void(0)" class="nav-link" onclick="scrollToSection(\'{sec["id"]}\')">{sec["title"]}</a></li>'
        )
    
    return f'''<nav class="sidebar-nav">
            <div class="nav-section-title">Unit Contents</div>
            <ul class="nav-list">
                {''.join(section_links)}
                <li class="nav-item"><a href="structured-questions.html" class="nav-link">Practice Questions</a></li>
            </ul>
            
            <div class="nav-section-title" style="margin-top: 20px;">Resources</div>
            <ul class="nav-list">
                <li class="nav-item"><a href="../../homework/{unit_id}/" class="nav-link" style="color: #16a34a;">📚 Homework (Exercises)</a></li>
            </ul>
            
            <div class="nav-section-title" style="margin-top: 20px;">My Progress</div>
            <ul class="nav-list">
                <li class="nav-item">
                    <div style="padding: 8px 0; display: flex; gap: 8px;">
                        <button onclick="updateProgress('{unit_id}', 'not_started')" id="progress-btn-not_started" class="progress-btn" style="flex:1; min-width: 0; padding: 8px 4px; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 11px; white-space: nowrap;">Start</button>
                        <button onclick="updateProgress('{unit_id}', 'in_progress')" id="progress-btn-in_progress" class="progress-btn" style="flex:1; min-width: 0; padding: 8px 4px; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 11px; white-space: nowrap;">Active</button>
                        <button onclick="updateProgress('{unit_id}', 'completed')" id="progress-btn-completed" class="progress-btn" style="flex:1; min-width: 0; padding: 8px 4px; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 11px; white-space: nowrap;">Done</button>
                    </div>
                </li>
            </ul>
        </nav>'''

def process_file(filepath, unit_id, sections):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, header_fixed = fix_header(content, unit_id)
    if header_fixed:
        print(f"  Fixed header for {unit_id}")
    else:
        print(f"  Header not changed for {unit_id}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Fixing header and sidebar for A2 units (ch12-ch22)...")
    
    for unit_id in UNITS.keys():
        filepath = os.path.join(base_path, unit_id, 'index.html')
        if os.path.exists(filepath):
            print(f"Processing {unit_id}...")
            process_file(filepath, unit_id, [])
        else:
            print(f"  File not found: {filepath}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()