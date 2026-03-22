#!/bin/bash
#
# PhysicsHub CrewAI 启动脚本
#

echo "🤖 PhysicsHub CrewAI 多Agent协作系统"
echo "======================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

# 检查crewai
if ! python3 -c "import crewai" 2>/dev/null; then
    echo "📦 安装 CrewAI..."
    pip3 install crewai
fi

# 检查环境变量
if [ -z "$KIMI_API_KEY" ]; then
    echo "⚠️  警告: 未设置 KIMI_API_KEY"
    echo "    请设置环境变量: export KIMI_API_KEY='your-key'"
    echo ""
fi

# 进入项目目录
cd ~/Desktop/PhysicsHub/crew

echo "👥 团队成员:"
echo "  📚 文档工程师 - 知识点整理、文档撰写"
echo "  📊 项目助理   - 进度跟踪、任务管理"
echo "  🎨 UI工程师   - 界面设计、样式规范"
echo "  💻 前端工程师 - 组件开发、交互实现"
echo ""

echo "🚀 启动协作..."
echo ""

# 运行Crew
python3 physics_hub_team.py
