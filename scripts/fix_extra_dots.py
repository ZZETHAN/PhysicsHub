#!/usr/bin/env python3
"""
Fix extra dots in subsection numbers
e.g., "18.1.1. " → "18.1.1 "
"""

import os
import re

UNIT_NUMBERS = {
    'ch12': '12', 'ch13': '13', 'ch14': '14', 'ch15': '15',
    'ch16': '16', 'ch17': '17', 'ch18': '18',
}

def fix_extra_dots(content, unit_id):
    unit_num = UNIT_NUMBERS[unit_id]
    
    # Fix patterns like "18.1.1. " → "18.1.1 "
    # Match "UNIT.MAJOR.MINOR. " and replace with "UNIT.MAJOR.MINOR "
    for major in range(1, 15):
        for minor in range(1, 15):
            # Fix h3
            pattern = rf'(<h3[^>]*>)({unit_num}\.{major}\.{minor}\.\s)([^<]+)(</h3>)'
            replacement = rf'\g<1>{unit_num}.{major}.{minor} \3\g<4>'
            content = re.sub(pattern, replacement, content)
            
            # Fix h4
            pattern = rf'(<h4[^>]*>)({unit_num}\.{major}\.{minor}\.\s)([^<]+)(</h4>)'
            replacement = rf'\g<1>{unit_num}.{major}.{minor} \3\g<4>'
            content = re.sub(pattern, replacement, content)
    
    return content

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Fixing extra dots in subsection numbers...")
    
    for unit_id in UNIT_NUMBERS.keys():
        filepath = os.path.join(base_path, unit_id, 'index.html')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = fix_extra_dots(content, unit_id)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed {unit_id}")

if __name__ == '__main__':
    main()