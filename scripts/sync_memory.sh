#!/bin/bash
#
# PhysicsHub 共享记忆同步脚本
# 用于多机器人之间的记忆同步

PHYSICSHUB_DIR="/Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub"
SHARED_MEMORY="$PHYSICSHUB_DIR/shared_memory.json"
LOG_FILE="$PHYSICSHUB_DIR/sync.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查AGFS
if [ ! -d "$PHYSICSHUB_DIR" ]; then
    log "❌ 错误: AGFS路径不存在"
    exit 1
fi

# 读取共享记忆
read_shared() {
    if [ -f "$SHARED_MEMORY" ]; then
        cat "$SHARED_MEMORY"
    else
        echo '{}'
    fi
}

# 更新共享记忆
update_shared() {
    local key="$1"
    local value="$2"
    
    python3 <<EOF
import json
import sys

try:
    with open('$SHARED_MEMORY', 'r') as f:
        data = json.load(f)
    
    keys = '$key'.split('.')
    target = data
    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]
    
    target[keys[-1]] = json.loads('$value')
    data['last_sync'] = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")'
    
    with open('$SHARED_MEMORY', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ 更新成功")
except Exception as e:
    print(f"❌ 错误: {e}")
    sys.exit(1)
EOF
}

# 获取项目进度
get_progress() {
    log "📊 获取项目进度..."
    
    python3 <<EOF
import json

with open('$SHARED_MEMORY', 'r') as f:
    data = json.load(f)

progress = data.get('shared_memory', {}).get('project_progress', {})
print(f"整体进度: {progress.get('overall', 0)}%")

units = progress.get('units', {})
for unit, info in units.items():
    status = info.get('status', 'unknown')
    p = info.get('progress', 0)
    icon = '✅' if status == 'completed' else ('🔄' if status == 'in_progress' else '⏸️')
    print(f"{icon} {unit}: {p}%")
EOF
}

# 更新单元状态
update_unit() {
    local unit="$1"
    local status="$2"
    local progress="$3"
    
    log "📝 更新单元状态: $unit -> $status ($progress%)"
    
    python3 <<EOF
import json

with open('$SHARED_MEMORY', 'r') as f:
    data = json.load(f)

if 'shared_memory' not in data:
    data['shared_memory'] = {}
if 'project_progress' not in data['shared_memory']:
    data['shared_memory']['project_progress'] = {}
if 'units' not in data['shared_memory']['project_progress']:
    data['shared_memory']['project_progress']['units'] = {}

data['shared_memory']['project_progress']['units']['$unit'] = {
    'status': '$status',
    'progress': $progress
}

# 重新计算整体进度
units = data['shared_memory']['project_progress']['units']
if units:
    total = sum(u.get('progress', 0) for u in units.values())
    data['shared_memory']['project_progress']['overall'] = int(total / len(units))

data['last_sync'] = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")'

with open('$SHARED_MEMORY', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ 单元状态已更新")
EOF
}

# 创建任务
create_task() {
    local name="$1"
    local assignee="$2"
    local deadline="$3"
    local priority="${4:-P1}"
    
    log "📋 创建任务: $name -> $assignee"
    
    python3 <<EOF
import json

with open('$SHARED_MEMORY', 'r') as f:
    data = json.load(f)

if 'shared_memory' not in data:
    data['shared_memory'] = {}
if 'task_assignments' not in data['shared_memory']:
    data['shared_memory']['task_assignments'] = []

tasks = data['shared_memory']['task_assignments']
task_id = f"TASK-{len(tasks)+1:03d}"

new_task = {
    'id': task_id,
    'name': '$name',
    'assignee': '$assignee',
    'deadline': '$deadline',
    'priority': '$priority',
    'status': 'pending'
}

tasks.append(new_task)
data['last_sync'] = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")'

with open('$SHARED_MEMORY', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ 任务已创建: {task_id}")
EOF
}

# 列出任务
list_tasks() {
    log "📋 任务列表:"
    
    python3 <<EOF
import json

with open('$SHARED_MEMORY', 'r') as f:
    data = json.load(f)

tasks = data.get('shared_memory', {}).get('task_assignments', [])

if not tasks:
    print("暂无任务")
else:
    for task in tasks:
        status_icon = '✅' if task['status'] == 'completed' else ('🔄' if task['status'] == 'in_progress' else '⏸️')
        print(f"{status_icon} [{task['priority']}] {task['id']}: {task['name']}")
        print(f"   负责人: {task['assignee']} | 截止: {task['deadline']}")
EOF
}

# 主命令
case "$1" in
    "progress"|"p")
        get_progress
        ;;
    "update-unit"|"uu")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "用法: $0 update-unit [单元名] [状态] [进度]"
            echo "示例: $0 update-unit ch13 in_progress 50"
            exit 1
        fi
        update_unit "$2" "$3" "$4"
        ;;
    "create-task"|"ct")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "用法: $0 create-task [任务名] [负责人] [截止日期] [优先级]"
            echo "示例: $0 create-task '完成Ch13' doc_engineer 2026-03-20 P0"
            exit 1
        fi
        create_task "$2" "$3" "$4" "${5:-P1}"
        ;;
    "list-tasks"|"lt")
        list_tasks
        ;;
    "read")
        read_shared | python3 -m json.tool
        ;;
    "notify")
        # 通知所有Agent同步
        log "🔔 发送同步通知..."
        echo "所有Agent请注意：共享记忆已更新，请重新加载。"
        ;;
    *)
        echo "PhysicsHub 共享记忆同步工具"
        echo ""
        echo "用法:"
        echo "  $0 progress                    - 查看项目进度"
        echo "  $0 update-unit [单元] [状态] [进度]  - 更新单元状态"
        echo "  $0 create-task [名] [人] [日期] [优先级] - 创建任务"
        echo "  $0 list-tasks                  - 列出所有任务"
        echo "  $0 read                        - 读取完整共享记忆"
        echo "  $0 notify                      - 通知所有Agent同步"
        echo ""
        echo "示例:"
        echo "  $0 update-unit ch13 completed 100"
        echo "  $0 create-task '优化样式' ui_designer 2026-03-22 P1"
        ;;
esac
