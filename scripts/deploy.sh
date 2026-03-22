#!/bin/bash
# PhysicsHub 部署脚本

echo "🚀 PhysicsHub 部署脚本"
echo "======================"

SERVER="123.207.75.145"
USER="ubuntu"

echo ""
echo "📋 部署前检查:"
echo "1. 确保本地测试通过"
echo "2. 数据库不会覆盖（本地和线上独立）"
echo ""
read -p "确认部署? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ 已取消"
    exit 1
fi

echo ""
echo "📦 准备部署..."

# 切换到项目目录
cd ~/Desktop/PhysicsHub

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
fi

# 运行环境设置（切换到生产环境）
echo "⚙️  配置生产环境..."
NODE_ENV=production node config/setup-env.js

# 部署到服务器
echo "📤 上传到服务器..."
rsync -avz --exclude='node_modules' --exclude='.git' --exclude='backup' \
    ~/Desktop/PhysicsHub/ ${USER}@${SERVER}:/var/www/physicshub/

# 重启服务器服务
echo "🔄 重启服务..."
ssh ${USER}@${SERVER} "sudo systemctl restart nginx && sudo systemctl restart physicshub"

echo ""
echo "✅ 部署完成!"
echo "🌐 访问: http://${SERVER}/"
