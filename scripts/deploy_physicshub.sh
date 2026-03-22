#!/bin/bash
# PhysicsHub 部署脚本
# 用途：将本地代码同步到服务器，排除敏感文件

set -e

# 配置
SERVER="ubuntu@123.207.75.145"
SERVER_PATH_WEB="/var/www/physicshub"
SERVER_PATH_API="/opt/physicshub/api"
LOCAL_PATH="/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub"

# 需要排除的文件/目录
EXCLUDES="--exclude 'node_modules' --exclude '.DS_Store' --exclude '*.zip' --exclude 'backup' --exclude '*.backup*' --exclude 'database.db' --exclude '*.log'"

echo "🚀 PhysicsHub 部署"
echo "=================="

# 1. 同步网站文件
echo "📁 同步网站文件..."
rsync -avz $EXCLUDES -e "sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_PATH/" "$SERVER:~/tmp/physicshub_sync/"

# 2. 复制到服务器网站目录
echo "📦 复制到网站目录..."
sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no "$SERVER" \
    "mkdir -p $SERVER_PATH_WEB && sudo cp -r ~/tmp/physicshub_sync/* $SERVER_PATH_WEB/"

# 3. 复制 API 文件（但排除 database.db）
echo "📦 复制 API 文件..."
sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no "$SERVER" \
    "sudo cp ~/tmp/physicshub_sync/api/server.js $SERVER_PATH_API/ && \
     sudo cp ~/tmp/physicshub_sync/api/database.js $SERVER_PATH_API/ && \
     sudo cp ~/tmp/physicshub_sync/api/routes/*.js $SERVER_PATH_API/routes/ && \
     sudo cp -r ~/tmp/physicshub_sync/api/middleware $SERVER_PATH_API/"

# 4. 修复权限（关键：必须 chown 为 www-data，否则 auth/ 和 units/ 会 404）
echo "🔧 修复权限..."
sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no "$SERVER" \
    "sudo chown -R www-data:www-data $SERVER_PATH_WEB/ && \
     sudo find $SERVER_PATH_WEB -type f -exec chmod 644 {} \; && \
     sudo find $SERVER_PATH_WEB -type d -exec chmod 755 {} \;"

# 5. 重启服务
echo "🔄 重启服务..."
sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no "$SERVER" \
    "sudo pkill -f 'node server.js' 2>/dev/null; \
     sleep 1; \
     cd $SERVER_PATH_API && \
     sudo -u ubuntu node server.js > /tmp/server.log 2>&1 &"

# 6. 验证
sleep 2
HEALTH=$(sshpass -p '@0430zYH' ssh -o StrictHostKeyChecking=no "$SERVER" "curl -s http://localhost:3001/api/health")
if echo "$HEALTH" | grep -q "ok"; then
    echo "✅ 部署成功！服务器运行正常"
else
    echo "❌ 部署完成但服务器可能需要检查"
fi

echo ""
echo "📝 注意事项："
echo "   - database.db 未被覆盖，用户数据已保留"
echo "   - 如需完整同步（包括 database.db），手动处理"
