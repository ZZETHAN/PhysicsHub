#!/bin/bash
#
# PhysicsHub 飞书推送工具
#

APP_ID="cli_a932ba6476389bd3"
APP_SECRET="WjkTcKHzjabgzRdqSJUGPfd2HJwss3PE"

# 获取访问令牌
get_token() {
    curl -s -X POST \
        https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))"
}

# 发送文本消息
send_message() {
    local group_id="$1"
    local message="$2"
    local token=$(get_token)
    
    if [ -z "$token" ]; then
        echo "❌ 获取Token失败"
        return 1
    fi
    
    # 转义消息中的特殊字符
    escaped_message=$(echo "$message" | sed 's/\\/\\\\/g; s/"/\\"/g')
    
    curl -s -X POST \
        "https://open.feishu.cn/open-apis/im/v1/messages" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "{
            \"receive_id\": \"$group_id\",
            \"msg_type\": \"text\",
            \"content\": \"{\\\"text\\\":\\\"$escaped_message\\\"}\"
        }"
}

# 发送富文本消息（带格式）
send_rich_message() {
    local group_id="$1"
    local title="$2"
    local content="$3"
    local token=$(get_token)
    
    if [ -z "$token" ]; then
        echo "❌ 获取Token失败"
        return 1
    fi
    
    # 构建富文本内容
    json_content=$(cat <<EOF
{
    "config": {"wide_screen_mode": true},
    "header": {
        "title": {"tag": "plain_text", "content": "$title"},
        "template": "blue"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "$content"}}
    ]
}
EOF
)
    
    curl -s -X POST \
        "https://open.feishu.cn/open-apis/im/v1/messages" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "{
            \"receive_id\": \"$group_id\",
            \"msg_type\": \"interactive\",
            \"content\": $(echo "$json_content" | python3 -c 'import sys,json; print(json.dumps(json.load(sys.stdin)))')
        }"
}

# 主命令
case "$1" in
    "test")
        echo "🔄 测试飞书连接..."
        token=$(get_token)
        if [ -n "$token" ]; then
            echo "✅ 连接成功！"
            echo "Token: ${token:0:20}..."
        else
            echo "❌ 连接失败"
            exit 1
        fi
        ;;
    "send")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "用法: $0 send [群组ID] [消息内容]"
            exit 1
        fi
        echo "📤 发送消息..."
        result=$(send_message "$2" "$3")
        echo "$result"
        ;;
    "rich")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "用法: $0 rich [群组ID] [标题] [内容]"
            exit 1
        fi
        echo "📤 发送富文本消息..."
        result=$(send_rich_message "$2" "$3" "$4")
        echo "$result"
        ;;
    "daily")
        # 执行每日报告
        ~/Desktop/PhysicsHub/scripts/daily_report.sh
        ;;
    *)
        echo "PhysicsHub 飞书推送工具"
        echo ""
        echo "用法:"
        echo "  $0 test                  - 测试连接"
        echo "  $0 send [群组ID] [消息]   - 发送文本消息"
        echo "  $0 rich [群组ID] [标题] [内容] - 发送富文本消息"
        echo "  $0 daily                 - 执行每日报告"
        echo ""
        echo "示例:"
        echo "  $0 test"
        echo "  $0 send 'oc_xxx' 'Hello from PhysicsHub!'"
        ;;
esac
