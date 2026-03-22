#!/usr/bin/env python3
"""
Wrapper for edit tool with auto-retry and auto-fix
This should be called instead of direct edit for critical operations
"""

import sys
import subprocess
import os

def run_edit(file_path, old_text, new_text):
    """Try to edit with multiple fallback strategies"""
    
    # Strategy 1: Try exact match with Python
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Edit successful: {file_path}")
            return True
    except Exception as e:
        print(f"  ⚠️ Strategy 1 failed: {e}")
    
    # Strategy 2: Normalize whitespace
    try:
        import re
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Normalize search text
        old_norm = re.sub(r'\s+', ' ', old_text).strip()
        content_norm = re.sub(r'\s+', ' ', content)
        
        if old_norm in content_norm:
            # Find matching section with flexible whitespace
            pattern = re.escape(old_norm).replace(r'\ ', r'\s+')
            match = re.search(pattern, content_norm)
            if match:
                # Get original text with correct whitespace
                start = match.start()
                end = match.end()
                # Map back to original content
                orig_start = content_norm[:start].count(' ')
                orig_end = content_norm[:end].count(' ')
                # This is approximate - use line-based approach instead
                
                lines = content.split('\n')
                old_lines = old_text.split('\n')
                new_lines = new_text.split('\n')
                
                # Find starting line
                for i, line in enumerate(lines):
                    if old_lines[0].strip() in line:
                        # Replace block
                        lines[i:i+len(old_lines)] = new_lines
                        with open(file_path, 'w') as f:
                            f.write('\n'.join(lines))
                        print(f"✅ Edit successful (whitespace normalized): {file_path}")
                        return True
                        
    except Exception as e:
        print(f"  ⚠️ Strategy 2 failed: {e}")
    
    # Strategy 3: Line-by-line replacement
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        old_first = old_text.strip().split('\n')[0]
        old_last = old_text.strip().split('\n')[-1]
        new_lines = new_text.split('\n')
        
        start_idx = -1
        end_idx = -1
        
        for i, line in enumerate(lines):
            if old_first in line and start_idx == -1:
                start_idx = i
            if old_last in line and start_idx != -1:
                end_idx = i
                break
        
        if start_idx != -1 and end_idx != -1:
            # Ensure newline at end
            if not new_lines[-1].endswith('\n'):
                new_lines[-1] += '\n'
            
            result = lines[:start_idx] + [l + '\n' if not l.endswith('\n') else l for l in new_lines] + lines[end_idx+1:]
            with open(file_path, 'w') as f:
                f.writelines(result)
            print(f"✅ Edit successful (line-based): {file_path}")
            return True
            
    except Exception as e:
        print(f"  ⚠️ Strategy 3 failed: {e}")
    
    # All strategies failed - run autofix and retry
    print(f"  🔄 Running autofix and retrying...")
    try:
        subprocess.run(['python3', os.path.expanduser('~/Desktop/PhysicsHub/scripts/autofix.py'), file_path], check=False)
        # Retry strategy 1 after autofix
        with open(file_path, 'r') as f:
            content = f.read()
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Edit successful (after autofix): {file_path}")
            return True
    except Exception as e:
        print(f"  ⚠️ Autofix retry failed: {e}")
    
    print(f"❌ Edit failed: Could not match text in {file_path}")
    return False

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 edit_wrapper.py <file> <old_text> <new_text>")
        sys.exit(1)
    
    success = run_edit(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)
