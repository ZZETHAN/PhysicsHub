#!/usr/bin/env python3
"""
Update subsection numbering in ch12-ch18 to match unit format
e.g., "1.1 Key Properties" → "18.1.1 Key Properties"
"""

import os
import re

UNIT_NUMBERS = {
    'ch12': '12',
    'ch13': '13',
    'ch14': '14',
    'ch15': '15',
    'ch16': '16',
    'ch17': '17',
    'ch18': '18',
}

def update_h3_h4_numbers(content, unit_id):
    unit_num = UNIT_NUMBERS[unit_id]
    
    # Update h3 headings: "1.1 Title" → "18.1.1 Title"
    # Note: the pattern is "1.1 " (digit, dot, digit, space)
    for major in range(1, 15):
        for minor in range(1, 15):
            # h3 pattern - match "X.Y " (not "X.Y. ")
            pattern = rf'(<h3[^>]*>)({major}\.{minor}\s)([^<]+)(</h3>)'
            replacement = rf'\g<1>{unit_num}.{major}.{minor} \3\g<4>'
            content = re.sub(pattern, replacement, content)
            
            # h4 pattern  
            pattern = rf'(<h4[^>]*>)({major}\.{minor}\s)([^<]+)(</h4>)'
            replacement = rf'\g<1>{unit_num}.{major}.{minor} \3\g<4>'
            content = re.sub(pattern, replacement, content)
    
    return content

def process_file(filepath, unit_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = update_h3_h4_numbers(content, unit_id)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Updated h3/h4 numbers for {unit_id}")

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Updating subsection numbers for ch12-ch18...")
    
    for unit_id in UNIT_NUMBERS.keys():
        filepath = os.path.join(base_path, unit_id, 'index.html')
        if os.path.exists(filepath):
            print(f"Processing {unit_id}...")
            process_file(filepath, unit_id)
        else:
            print(f"  File not found: {filepath}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()