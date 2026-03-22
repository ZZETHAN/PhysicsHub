#!/bin/bash
#
# PhysicsHub Feishu Bot 启动脚本
#

echo "🤖 PhysicsHub 飞书机器人启动器"
echo "================================"
echo ""

# 检查配置
if [ ! -f "bot_config.yaml" ]; then
    echo "❌ 错误: 配置文件不存在"
    exit 1
fi

# 加载配置
APP_ID=$(grep "app_id:" bot_config.yaml | awk '{print $2}')
APP_SECRET=$(grep "app_secret:" bot_config.yaml | awk '{print $2}')

echo "✅ 配置加载成功"
echo "App ID: ${APP_ID:0:8}..."
echo ""

# 测试连接
echo "🔄 正在测试飞书连接..."
RESPONSE=$(curl -s -X POST \
    https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" 2>/dev/null)

if echo "$RESPONSE" | grep -q "tenant_access_token"; then
    echo "✅ 飞书连接成功！"
    echo ""
    
    # 提取token
    TOKEN=$(echo "$RESPONSE" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)
    
    # 获取机器人信息
    BOT_INFO=$(curl -s -X GET \
        https://open.feishu.cn/open-apis/bot/v3/info \
        -H "Authorization: Bearer $TOKEN" 2>/dev/null)
    
    echo "📝 机器人信息:"
    echo "$BOT_INFO" | grep -o '"bot_name":"[^"]*"' | head -1
    echo ""
    
    echo "🚀 启动选项:"
    echo "1. 启动文档工程师 (推荐)"
    echo "2. 启动项目助理"
    echo "3. 启动全部机器人"
    echo "4. 仅测试连接"
    echo "5. 退出"
    echo ""
    
    read -p "请选择 [1-5]: " choice
    
    case $choice in
        1)
            echo "📚 启动文档工程师..."
            echo "功能: 知识库管理、文档撰写、知识点查询"
            # 这里可以启动具体的bot服务
            ;;
        2)
            echo "📊 启动项目助理..."
            echo "功能: 任务管理、进度跟踪、提醒"
            ;;
        3)
            echo "🤖 启动全部机器人..."
            ;;
        4)
            echo "✅ 连接测试通过"
            ;;
        5)
            echo "👋 再见"
            exit 0
            ;;
        *)
            echo "❌ 无效选择"
            ;;
    esac
else
    echo "❌ 连接失败，请检查 App ID 和 App Secret"
    echo "错误信息:"
    echo "$RESPONSE"
    exit 1
fi
