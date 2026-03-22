#!/usr/bin/env python3
"""
Fix doubled section numbers in ch12-ch18
e.g., "12.12. 1." → "12.1."
Also fix double spaces: "12.1.  " → "12.1. "
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

def fix_doubled_numbers(content, unit_id):
    unit_num = UNIT_NUMBERS[unit_id]
    
    # Fix sidebar links and h2 titles: "12.12. 1." → "12.1."
    for i in range(1, 10):
        bad_pattern = f'{unit_num}.{unit_num}. {i}.'
        good_pattern = f'{unit_num}.{i}. '
        content = content.replace(bad_pattern, good_pattern)
    
    # Fix double spaces: "12.1.  " → "12.1. "
    content = re.sub(r'(\d+\.\d+\.\s) +', r'\1', content)
    
    return content

def process_file(filepath, unit_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_doubled_numbers(content, unit_id)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Fixed doubled numbers for {unit_id}")

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Fixing doubled section numbers for ch12-ch18...")
    
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