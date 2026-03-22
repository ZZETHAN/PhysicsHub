#!/bin/bash
# 本地开发环境启动脚本

echo "🚀 PhysicsHub 本地开发环境"
echo "============================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "请安装 Node.js: https://nodejs.org/ (建议 v18 LTS)"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"

# 进入后端目录
cd ~/Desktop/PhysicsHub/api

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装后端依赖..."
    npm install
fi

# 启动后端服务器（后台）
echo "🚀 启动后端服务器..."
nohup node server.js > /tmp/server.log 2>&1 &
SERVER_PID=$!
echo "   后端 PID: $SERVER_PID"
sleep 2

# 检查后端是否启动
if curl -s http://localhost:3001/api/health | grep -q "ok"; then
    echo "   ✅ 后端运行正常: http://localhost:3001"
else
    echo "   ⚠️ 后端可能未启动，检查日志: tail -f /tmp/server.log"
fi

# 启动前端开发服务器（简单 HTTP 服务器）
echo ""
echo "🚀 启动前端服务器..."
cd ~/Desktop/PhysicsHub

# 检查是否有 http-server
if ! command -v npx &> /dev/null; then
    echo "📦 安装 http-server..."
    npm install -g http-server
fi

echo "   前端地址: http://localhost:8080"
echo ""
npx http-server -p 8080 -o

# 清理函数
cleanup() {
    echo ""
    echo "🛑 停止服务器..."
    kill $SERVER_PID 2>/dev/null
    echo "✅ 已清理"
}
trap cleanup EXIT
