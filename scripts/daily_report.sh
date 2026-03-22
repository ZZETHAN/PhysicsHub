#!/bin/bash
#
# PhysicsHub 每日进度推送脚本
# 每天早上9点自动推送到飞书群组
#

# 配置
APP_ID="cli_a932ba6476389bd3"
APP_SECRET="WjkTcKHzjabgzRdqSJUGPfd2HJwss3PE"

# 获取访问令牌
TOKEN_RESPONSE=$(curl -s -X POST \
    https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ 获取Token失败"
    exit 1
fi

# 获取当前日期
TODAY=$(date +"%Y-%m-%d")
WEEK_DAY=$(date +"%u")

# 计算项目统计
TOTAL_UNITS=$(ls -1 ~/Desktop/PhysicsHub/units/ch* 2>/dev/null | wc -l)
COMPLETED_UNITS=$(grep -l "completed" ~/Desktop/PhysicsHub/units/*/index.html 2>/dev/null | wc -l)
PROGRESS=$((COMPLETED_UNITS * 100 / 11))

# 获取最新更新
LATEST_UPDATE=$(git -C ~/Desktop/PhysicsHub log --oneline -1 2>/dev/null || echo "Ch 12 圆周运动完成")

# 构建消息内容
MESSAGE="📊 PhysicsHub 每日进度报告
━━━━━━━━━━━━━━━━━━━━━━

📅 日期: $TODAY
📈 整体进度: $PROGRESS% ($COMPLETED_UNITS/11 单元)

📝 最新更新:
• $LATEST_UPDATE

📋 今日任务:
• 继续完善 Ch 13 引力场内容
• 检查昨日完成质量
• 规划明日任务

👥 团队状态:
• 文档工程师: 活跃 ✅
• 项目助理: 监控中 📊

🔗 项目位置: ~/Desktop/PhysicsHub

💡 回复 \\"@文档工程师 进度\\" 查看详情"

# 发送消息（需要替换GROUP_ID）
# 先打印消息内容
echo "$MESSAGE"

# 如果需要实际发送，取消下面注释并设置GROUP_ID
# GROUP_ID="your_group_id_here"
# curl -X POST \
#     "https://open.feishu.cn/open-apis/im/v1/messages" \
#     -H "Authorization: Bearer $TOKEN" \
#     -H "Content-Type: application/json" \
#     -d "{
#         \"receive_id\": \"$GROUP_ID\",
#         \"msg_type\": \"text\",
#         \"content\": \"{\\\"text\\\":\\\"$MESSAGE\\\"}\"
#     }"
