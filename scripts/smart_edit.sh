#!/bin/bash
# Smart edit wrapper with auto-fix
# Usage: bash smart_edit.sh <file> <search> <replace>

FILE="$1"
SEARCH="$2"
REPLACE="$3"

if [ -z "$FILE" ] || [ -z "$SEARCH" ]; then
    echo "Usage: bash smart_edit.sh <file> <search> <replace>"
    exit 1
fi

# Create backup
cp "$FILE" "$FILE.bak.$(date +%s)"

# Try 3 approaches

# Approach 1: Exact match with sed (Mac compatible)
if grep -q "$SEARCH" "$FILE" 2>/dev/null; then
    # Use Python for reliable replacement
    python3 << PYEOF
import sys
with open('$FILE', 'r') as f:
    content = f.read()
if '$SEARCH' in content:
    content = content.replace('$SEARCH', '$REPLACE', 1)
    with open('$FILE', 'w') as f:
        f.write(content)
    print("✅ Edit successful (exact match)")
    sys.exit(0)
PYEOF
    if [ $? -eq 0 ]; then
        exit 0
    fi
fi

# Approach 2: Normalize whitespace
python3 << PYEOF
import re
with open('$FILE', 'r') as f:
    content = f.read()

# Normalize whitespace in search pattern
search_norm = re.sub(r'\s+', ' ', '''$SEARCH''').strip()
content_norm = re.sub(r'\s+', ' ', content)

if search_norm in content_norm:
    # Find the actual text with original whitespace
    lines = content.split('\n')
    for i, line in enumerate(lines):
        line_norm = re.sub(r'\s+', ' ', line).strip()
        if search_norm == line_norm or search_norm in line_norm:
            lines[i] = line.replace(line.strip(), '''$REPLACE''', 1)
            break
    with open('$FILE', 'w') as f:
        f.write('\n'.join(lines))
    print("✅ Edit successful (whitespace normalized)")
    exit(0)
PYEOF

if [ $? -eq 0 ]; then
    exit 0
fi

# Approach 3: Line-by-line partial match
python3 << PYEOF
with open('$FILE', 'r') as f:
    lines = f.readlines()

search_first = '''$SEARCH'''.strip().split('\n')[0]
search_last = '''$SEARCH'''.strip().split('\n')[-1]

# Find range
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if search_first in line and start_idx == -1:
        start_idx = i
    if search_last in line and start_idx != -1:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    # Replace the range
    new_lines = lines[:start_idx] + ['''$REPLACE''' + '\n'] + lines[end_idx+1:]
    with open('$FILE', 'w') as f:
        f.writelines(new_lines)
    print("✅ Edit successful (line range match)")
    exit(0)

print("❌ Edit failed: Could not find matching text")
exit(1)
PYEOF
