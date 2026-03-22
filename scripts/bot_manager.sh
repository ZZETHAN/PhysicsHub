#!/bin/bash
#
# PhysicsHub 4机器人管理脚本
#

CONFIG_FILE="$HOME/.openclaw/extensions/feishu/physicshub_bots.yaml"
PHYSICSHUB_DIR="$HOME/Desktop/PhysicsHub"

echo "🤖 PhysicsHub 飞书机器人管理"
echo "=============================="
echo ""

# 获取访问令牌
get_token() {
    local app_id="$1"
    local app_secret="$2"
    
    curl -s -X POST \
        https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$app_id\",\"app_secret\":\"$app_secret\"}" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))"
}

# 测试单个机器人
test_bot() {
    local name="$1"
    local app_id="$2"
    local app_secret="$3"
    local emoji="$4"
    
    echo -n "$emoji 测试 $name... "
    
    TOKEN=$(get_token "$app_id" "$app_secret")
    
    if [ -n "$TOKEN" ] && [ "$TOKEN" != "" ]; then
        echo "✅ 连接成功"
        echo "   Token: ${TOKEN:0:20}..."
        return 0
    else
        echo "❌ 连接失败"
        return 1
    fi
}

# 发送消息
send_message() {
    local bot_name="$1"
    local group_id="$2"
    local message="$3"
    
    # 从配置读取App ID和Secret
    local app_id=$(grep -A5 "^  $bot_name:" "$CONFIG_FILE" | grep "app_id:" | awk '{print $2}')
    local app_secret=$(grep -A5 "^  $bot_name:" "$CONFIG_FILE" | grep "app_secret:" | awk '{print $2}')
    
    TOKEN=$(get_token "$app_id" "$app_secret")
    
    if [ -z "$TOKEN" ]; then
        echo "❌ 获取Token失败"
        return 1
    fi
    
    # 转义消息
    escaped_message=$(echo "$message" | sed 's/\\/\\\\/g; s/"/\\"/g')
    
    curl -s -X POST \
        "https://open.feishu.cn/open-apis/im/v1/messages" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"receive_id\": \"$group_id\",
            \"msg_type\": \"text\",
            \"content\": \"{\\\"text\\\":\\\"$escaped_message\\\"}\"
        }"
}

# 同步共享记忆
sync_memory() {
    echo "🔄 同步共享记忆到所有机器人..."
    
    local memory_file="/Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub/shared_memory.json"
    
    if [ ! -f "$memory_file" ]; then
        echo "❌ 共享记忆文件不存在"
        return 1
    fi
    
    # 读取进度
    local progress=$(python3 -c "
import json
with open('$memory_file', 'r') as f:
    data = json.load(f)
print(data.get('shared_memory', {}).get('project_progress', {}).get('overall', 0))
")
    
    echo "📊 当前进度: $progress%"
    echo "✅ 共享记忆已同步"
}

# 主命令
case "$1" in
    "test"|"t")
        echo "🧪 测试所有机器人连接..."
        echo ""
        
        test_bot "doc_engineer" "cli_a9339a75b4fadcb5" "bq66ylTi9SVnQ9FzX4sQzd8sU2JLsiTg" "📚"
        test_bot "project_manager" "cli_a9339b17f3f81cba" "EMCmB2QwIt6fMgJCoug8Pc638PLz8Wo0" "📊"
        test_bot "ui_designer" "cli_a9339b7a57f81ceb" "59ZgMXDTgGVUk4Drp5KIpe644zvqqbhE" "🎨"
        test_bot "frontend_dev" "cli_a9339ba0fcf89cca" "QzslJLJrpOgIccXuBgoIAeW7azoG406k" "💻"
        ;;
        
    "send"|"s")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "用法: $0 send [机器人] [群组ID] [消息]"
            echo "示例: $0 send doc_engineer 'oc_xxx' 'Hello'"
            exit 1
        fi
        send_message "$2" "$3" "$4"
        ;;
        
    "sync"|"sy")
        sync_memory
        ;;
        
    "status"|"st")
        echo "📊 机器人状态"
        echo "============="
        echo ""
        echo "📚 文档工程师: cli_a9339a75b4fadcb5"
        echo "📊 项目助理:   cli_a9339b17f3f81cba"
        echo "🎨 UI工程师:   cli_a9339b7a57f81ceb"
        echo "💻 前端工程师: cli_a9339ba0fcf89cca"
        echo ""
        echo "共享记忆: /Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub/"
        ;;
        
    "help"|"h"|*)
        echo "PhysicsHub 飞书机器人管理"
        echo ""
        echo "用法:"
        echo "  $0 test                - 测试所有机器人连接"
        echo "  $0 send [机器人] [群组] [消息] - 发送消息"
        echo "  $0 sync                - 同步共享记忆"
        echo "  $0 status              - 查看状态"
        echo ""
        echo "示例:"
        echo "  $0 test"
        echo "  $0 send doc_engineer 'oc_xxx' '任务完成'"
        ;;
esac
