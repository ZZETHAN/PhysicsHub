#!/usr/bin/env python3
"""
Auto-fix system for HTML edit failures
Usage: python3 autofix.py <file>
"""

import sys
import re
import os

def fix_html_entities(content):
    """Fix HTML entity encoding issues"""
    fixes = [
        ('u003e', '>'),
        ('u003c', '<'),
        ('u0026', '&'),
        ('u0022', '"'),
        ('u0027', "'"),
        ('&gt;', '>'),
        ('&lt;', '<'),
        ('&quot;', '"'),
        ('&#39;', "'"),
    ]
    
    count = 0
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"  ✅ Fixed: {old} → {new}")
    
    return content, count

def fix_broken_tags(content):
    """Fix broken HTML tags from failed edits"""
    # Fix <div class="exam-alert"003e
    content = re.sub(r'(<[^>]+)"(\d+)\003e', r'\1">', content)
    content = re.sub(r'(<[^>]+)"(\d+)\003c', r'\1"<', content)
    
    # Fix <u003e>>
    content = re.sub(r'<u003e>', '', content)
    content = re.sub(r'<u003c>', '', content)
    
    return content

def fix_whitespace(content):
    """Normalize whitespace issues"""
    # Remove trailing whitespace
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 autofix.py <file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    print(f"🔧 Auto-fixing: {filepath}")
    print("-" * 50)
    
    # Apply fixes
    content, entity_count = fix_html_entities(original)
    content = fix_broken_tags(content)
    content = fix_whitespace(content)
    
    # Write back if changed
    if content != original:
        # Backup
        backup_path = filepath + '.autofix.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        
        # Write fixed version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Fixed and saved")
        print(f"   Backup: {backup_path}")
    else:
        print("\n✅ No issues found")

if __name__ == '__main__':
    main()
