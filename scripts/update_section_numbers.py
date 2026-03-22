#!/usr/bin/env python3
"""
Update section numbering in ch12-ch18 to match ch19-ch22 format
e.g., "1. Angular Motion" → "12.1 Angular Motion"
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

def update_section_numbers(content, unit_id):
    unit_num = UNIT_NUMBERS[unit_id]
    
    # Update sidebar links: "1. Title" → "12.1 Title"
    # Only match standalone single digits followed by dot-space (not part of larger number)
    for i in range(1, 10):
        # For sidebar: look for "Number. " at start of link text
        # Pattern: <a ...>Number. Title</a>
        # Use negative lookbehind to ensure we don't match "12.1"
        pattern = rf'(<a[^>]*>)(?<!\d){i}\.\s([^<]+)(</a>)'
        replacement = rf'\g<1>{unit_num}.{i}. \2\g<3>'
        content = re.sub(pattern, replacement, content)
    
    # Update h2 titles: <h2>1. Title</h2> → <h2>12.1 Title</h2>
    for i in range(1, 10):
        # H2 pattern with negative lookbehind
        pattern = rf'(<h2[^>]*>)(?<!\d){i}\.\s([^<]+)(</h2>)'
        replacement = rf'\g<1>{unit_num}.{i}. \2\g<3>'
        content = re.sub(pattern, replacement, content)
    
    return content

def process_file(filepath, unit_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = update_section_numbers(content, unit_id)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Updated section numbers for {unit_id}")

def main():
    base_path = '/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub/units'
    
    print("Updating section numbers for ch12-ch18...")
    
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