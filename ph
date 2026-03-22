#!/bin/bash
#
# PhysicsHub 协调器 - 快捷入口
# 一键调用4个机器人同时工作
#

cd ~/Desktop/PhysicsHub

if [ $# -eq 0 ]; then
    echo "🎯 PhysicsHub 助手"
    echo "===================="
    echo ""
    echo "用法: ph [指令]"
    echo ""
    echo "示例:"
    echo '  ph "完成Ch 13所有内容"          # 4个机器人同时工作'
    echo '  ph "查看项目进度"              # 项目助理汇报'
    echo '  ph "设计新组件"                # UI工程师设计'
    echo '  ph "整理Ch 14知识点"          # 文档工程师整理'
    echo '  ph "开发交互功能"              # 前端工程师开发'
    echo ""
    echo "智能分配:"
    echo "  • 整理/文档/公式 → 📚 文档工程师"
    echo "  • 进度/任务/计划 → 📊 项目助理"
    echo "  • 设计/样式/配色 → 🎨 UI工程师"
    echo "  • 开发/代码/交互 → 💻 前端工程师"
    echo "  • 完成/创建/制作 → 🎯 全部4个"
    exit 0
fi

# 合并所有参数为一句话
message="$*"

echo "🎯 PhysicsHub 助手: $message"
echo ""

python3 coordinator.py "$message"
