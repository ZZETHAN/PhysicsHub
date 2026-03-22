#!/usr/bin/env python3
"""
Unify left sidebar navigation format across A2 Physics units (ch12-ch22)
"""

import os
import re

UNIT_SECTIONS = {
    'ch12': ['intro', 'angular', 'acceleration', 'force', 'vertical', 'checklist'],
    'ch13': ['intro', 'newtons-law', 'field-strength', 'potential', 'orbits', 'escape', 'checklist'],
    'ch14': ['intro', 'zeroth-law', 'temperature-scales', 'thermometric', 'heat-capacity', 'latent-heat', 'checklist'],
    'ch15': ['intro', 'gas-laws', 'equation-of-state', 'kinetic-theory', 'molecular-kinetic', 'rms-speed', 'assumptions', 'checklist'],
    'ch16': ['intro', 'internal-energy', 'work-gas', 'first-law', 'pv-graph', 'checklist'],
    'ch17': ['intro', 'observing', 'describing', 'equations', 'energy', 'damped', 'resonance', 'checklist'],
    'ch18': ['intro', 'coulomb', 'field-strength', 'field-patterns', 'potential', 'uniform-field', 'checklist'],
    'ch19': ['intro', 'capacitors', 'combination', 'discharging', 'checklist'],
    'ch20': ['intro', 'field-basics', 'lorentz', 'emi', 'checklist'],
    'ch21': ['intro', 'ac-basics', 'cro', 'rms', 'rectification', 'smoothing', 'checklist'],
    'ch22': ['intro', 'photon', 'photoelectric', 'duality', 'energy-levels', 'checklist'],
}

UNIT_TITLES = {
    'ch12': ['Introduction', '1. Angular Motion', '2. Centripetal Acceleration', '3. Centripetal Force', '4. Vertical Circle'],
    'ch13': ["Introduction", "1. Newton's Law", '2. Field Strength', '3. Potential', '4. Orbital Motion', '5. Escape Velocity'],
    'ch14': ['Introduction', '1. Zeroth Law', '2. Temperature Scales', '3. Thermometric Properties', '4. Specific Heat Capacity', '5. Specific Latent Heat'],
    'ch15': ['Introduction', '1. Gas Laws', '2. Equation of State', '3. Kinetic Theory', '4. Molecular Kinetic Energy', '5. RMS Speed', '6. Assumptions'],
    'ch16': ['Introduction', '1. Internal Energy', '2. Doing Work - Gas', '3. First Law of Thermodynamics', '4. P-V Graph Analysis'],
    'ch17': ['Introduction', '1. Observing Oscillations', '2. Describing SHM', '3. SHM Equations', '4. Energy in SHM', '5. Damped Oscillations', '6. Resonance'],
    'ch18': ["Introduction", "1. Coulomb's Law", '2. Electric Field Strength', '3. Electric Field Patterns', '4. Electric Potential', '5. Uniform Electric Field'],
    'ch19': ['Introduction', '19.1 Capacitors', '19.2 Combination', '19.3 Discharging'],
    'ch20': ['Introduction', '20.1 Field Basics', '20.2 Lorentz Force', '20.3 EMI ⭐⭐⭐'],
    'ch21': ['Introduction', '21.1 AC Characteristics', 'CRO & Oscilloscope', '21.2 RMS Values', '21.3 Rectification', 'Smoothing'],
    'ch22': ['Introduction', '22.1 Photons', '22.2 Photoelectric Effect', '22.3 Wave-Particle Duality', '22.4 Energy Levels'],
}

def get_standard_nav_links(unit_id):
    """Generate standard nav links for a unit"""
    sections = UNIT_SECTIONS[unit_id]
    titles = UNIT_TITLES[unit_id]
    
    links = []
    # First section is intro (active)
    links.append(f'<li class="nav-item"><a href="javascript:void(0)" class="nav-link active" onclick="scrollToSection(\'{sections[0]}\')">{titles[0]}</a></li>')
    
    # Remaining sections (skip checklist at end)
    for i in range(1, len(sections) - 1):
        links.append(f'<li class="nav-item"><a href="javascript:void(0)" class="nav-link" onclick="scrollToSection(\'{sections[i]}\')">{titles[i]}</a></li>')
    
    # Checklist (last)
    links.append(f'<li class="nav-item"><a href="javascript:void(0)" class="nav-link" onclick="scrollToSection(\'{sections[-1]}\')">P4 Checklist</a></li>')
    
    return '\n'.join(links)

def fix_sidebar(content, unit_id):
    """Fix sidebar to use standardized format"""
    if unit_id not in UNIT_SECTIONS:
        return content, False
    
    nav_links = get_standard_nav_links(unit_id)
    
    new_sidebar = f'''<nav class="sidebar-nav">
            <div class="nav-section-title">Unit Contents</div>
            <ul class="nav-list">
                {nav_links}
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
    
    pattern = r'<nav class="sidebar-nav">.*?</nav>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_sidebar + content[match.end():]
        return content, True
    
    return content, False

def process_file(filepath, unit_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content, fixed = fix_sidebar(content, unit_id)
    
    if fixed:
        print(f"  Fixed sidebar for {unit_id}")
    else:
        print(f"  Sidebar not found for {unit_id}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixed

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Unifying left sidebar format for A2 units (ch12-ch22)...")
    
    for unit_id in UNIT_SECTIONS.keys():
        filepath = os.path.join(base_path, unit_id, 'index.html')
        if os.path.exists(filepath):
            print(f"Processing {unit_id}...")
            process_file(filepath, unit_id)
        else:
            print(f"  File not found: {filepath}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()