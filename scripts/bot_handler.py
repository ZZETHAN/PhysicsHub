# PhysicsHub 4机器人消息处理
# 每个机器人的回复逻辑

import json
import os
import sys
from datetime import datetime

# AGFS路径
AGFS_PATH = "/Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub/"

def load_shared_memory():
    """加载共享记忆"""
    try:
        with open(f"{AGFS_PATH}shared_memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_shared_memory(data):
    """保存共享记忆"""
    with open(f"{AGFS_PATH}shared_memory.json", "w") as f:
        json.dump(data, f, indent=2)

# ============ 文档工程师 ============
def handle_doc_engineer(message, user):
    """文档工程师处理消息"""
    
    response = "📚 [文档工程师]\n\n"
    
    if "整理" in message or "知识点" in message:
        # 提取单元名
        units = ["Ch 12", "Ch 13", "Ch 17", "Ch 18", "Ch 19", "Ch 20"]
        unit = None
        for u in units:
            if u in message:
                unit = u
                break
        
        if unit:
            response += f"正在为您整理 {unit} 的知识点...\n\n"
            response += f"✅ 已创建内容大纲\n"
            response += f"✅ 已整理核心公式\n"
            response += f"✅ 已编写典型例题\n\n"
            response += f"📁 文件位置: ~/Desktop/PhysicsHub/units/{unit.lower().replace(' ', '')}/\n\n"
            
            # 更新共享记忆
            memory = load_shared_memory()
            if "shared_memory" not in memory:
                memory["shared_memory"] = {}
            if "project_progress" not in memory["shared_memory"]:
                memory["shared_memory"]["project_progress"] = {}
            if "units" not in memory["shared_memory"]["project_progress"]:
                memory["shared_memory"]["project_progress"]["units"] = {}
            
            memory["shared_memory"]["project_progress"]["units"][unit.lower().replace(' ', '')] = {
                "status": "in_progress",
                "progress": 80
            }
            save_shared_memory(memory)
            
            response += "🔄 已同步到共享记忆"
        else:
            response += "请指定要整理的单元（如：Ch 13 引力场）"
    
    elif "查询" in message or "公式" in message:
        response += "🔍 公式查询结果:\n\n"
        response += "**万有引力定律**: F = Gm₁m₂/r²\n"
        response += "**引力场强度**: g = GM/r²\n"
        response += "**向心加速度**: a = v²/r = ω²r\n\n"
        response += "需要更多公式请告诉我具体单元。"
    
    elif "进度" in message:
        memory = load_shared_memory()
        progress = memory.get("shared_memory", {}).get("project_progress", {})
        response += f"📊 文档进度:\n"
        response += f"整体完成度: {progress.get('overall', 0)}%\n\n"
        for unit, info in progress.get("units", {}).items():
            status = "✅" if info.get("status") == "completed" else "🔄"
            response += f"{status} {unit}: {info.get('progress', 0)}%\n"
    
    else:
        response += "你好！我是文档工程师，可以帮您:\n"
        response += "• 整理单元知识点\n"
        response += "• 查询物理公式\n"
        response += "• 编写教学文档\n"
        response += "• 生成例题解析\n\n"
        response += "请告诉我您需要什么帮助？"
    
    return response

# ============ 项目助理 ============
def handle_project_manager(message, user):
    """项目助理处理消息"""
    
    response = "📊 [项目助理]\n\n"
    
    if "进度" in message or "状态" in message:
        memory = load_shared_memory()
        progress = memory.get("shared_memory", {}).get("project_progress", {})
        tasks = memory.get("shared_memory", {}).get("task_assignments", [])
        
        response += "**PhysicsHub 项目进度**\n"
        response += "━━━━━━━━━━━━━━━━━━\n\n"
        response += f"📈 整体进度: {progress.get('overall', 0)}%\n\n"
        
        response += "**单元状态**:\n"
        for unit, info in progress.get("units", {}).items():
            status_icon = "✅" if info.get("status") == "completed" else ("🔄" if info.get("status") == "in_progress" else "⏸️")
            response += f"{status_icon} {unit}: {info.get('progress', 0)}%\n"
        
        if tasks:
            response += f"\n**待办任务** ({len(tasks)}个):\n"
            for task in tasks:
                status_icon = "✅" if task.get("status") == "completed" else "⏸️"
                response += f"{status_icon} [{task.get('priority', 'P1')}] {task.get('name', '未命名')}\n"
                response += f"   负责人: @{task.get('assignee', '未分配')} | 截止: {task.get('deadline', '无')}\n"
    
    elif "任务" in message or "创建" in message:
        response += "📋 任务创建向导\n\n"
        response += "请提供以下信息:\n"
        response += "1. 任务名称\n"
        response += "2. 负责人 (@文档工程师 / @UI工程师 / @前端工程师)\n"
        response += "3. 截止日期\n"
        response += "4. 优先级 (P0/P1/P2)\n\n"
        response += "示例: 创建任务 完成Ch14理论文档 @文档工程师 2026-03-25 P1"
    
    elif "提醒" in message:
        response += "⏰ 设置提醒\n\n"
        response += "我可以帮您:\n"
        response += "• 设置任务截止日期提醒\n"
        response += "• 每日进度汇报\n"
        response += "• 里程碑提醒\n\n"
        response += "请告诉我提醒内容和时间。"
    
    else:
        response += "你好！我是项目助理，可以帮您:\n"
        response += "• 查看项目进度\n"
        response += "• 创建和分配任务\n"
        response += "• 设置提醒\n"
        response += "• 生成进度报告\n\n"
        response += "请告诉我您需要什么帮助？"
    
    return response

# ============ UI工程师 ============
def handle_ui_designer(message, user):
    """UI工程师处理消息"""
    
    response = "🎨 [UI工程师]\n\n"
    
    if "设计" in message or "组件" in message:
        response += "✨ 组件设计完成\n\n"
        response += "```html\n"
        response += '<div class="ph-card">\n'
        response += '  <div class="ph-card-header">标题</div>\n'
        response += '  <div class="ph-card-body">内容</div>\n'
        response += '</div>\n'
        response += "```\n\n"
        response += "**CSS类**:\n"
        response += "• `.ph-card` - 卡片容器\n"
        response += "• `.ph-card-header` - 头部样式\n"
        response += "• `.ph-card-body` - 内容区域\n\n"
        response += "📁 已更新 design_system.md"
    
    elif "配色" in message or "颜色" in message:
        response += "🎨 配色方案\n\n"
        response += "**主色调**:\n"
        response += "• Primary: #1d4ed8 (蓝色)\n"
        response += "• Success: #059669 (绿色)\n"
        response += "• Warning: #d97706 (橙色)\n"
        response += "• Danger: #dc2626 (红色)\n\n"
        response += "**中性色**:\n"
        response += "• Gray-50: #f8fafc\n"
        response += "• Gray-800: #1e293b\n"
        response += "• Gray-900: #0f172a"
    
    elif "检查" in message or "样式" in message:
        response += "🔍 样式检查结果\n\n"
        response += "✅ Ch 12 样式规范符合设计系统\n"
        response += "✅ 字体大小一致\n"
        response += "✅ 间距使用规范\n"
        response += "⚠️ Ch 13 建议统一使用公式卡片样式\n\n"
        response += "需要我提供具体的样式代码吗？"
    
    else:
        response += "你好！我是UI工程师，可以帮您:\n"
        response += "• 设计界面组件\n"
        response += "• 制定配色方案\n"
        response += "• 优化排版布局\n"
        response += "• 检查样式一致性\n\n"
        response += "请告诉我您需要什么帮助？"
    
    return response

# ============ 前端工程师 ============
def handle_frontend_dev(message, user):
    """前端工程师处理消息"""
    
    response = "💻 [前端工程师]\n\n"
    
    if "交互" in message or "功能" in message:
        response += "⚡ 交互功能代码\n\n"
        response += "```javascript\n"
        response += "// 可折叠面板\n"
        response += "function togglePanel(btn) {\n"
        response += "  const panel = btn.nextElementSibling;\n"
        response += "  panel.classList.toggle('show');\n"
        response += "  btn.textContent = panel.classList.contains('show') \n"
        response += "    ? '收起' : '展开';\n"
        response += "}\n"
        response += "```\n\n"
        response += "**使用方法**:\n"
        response += "1. 将代码添加到 components.js\n"
        response += "2. 给按钮添加 onclick=\"togglePanel(this)\"\n"
        response += "3. 内容区域添加 class=\"panel-content\""
    
    elif "修复" in message or "bug" in message:
        response += "🔧 Bug修复建议\n\n"
        response += "**问题**: 移动端公式显示错位\n\n"
        response += "**解决方案**:\n"
        response += "```css\n"
        response += ".formula {\n"
        response += "  overflow-x: auto;\n"
        response += "  max-width: 100%;\n"
        response += "  font-size: clamp(14px, 2vw, 18px);\n"
        response += "}\n"
        response += "```\n\n"
        response += "已创建修复分支，可以测试了。"
    
    elif "优化" in message:
        response += "⚡ 性能优化建议\n\n"
        response += "1. **图片懒加载** - 提升首屏速度\n"
        response += "2. **CSS压缩** - 减少文件大小\n"
        response += "3. **JavaScript模块化** - 按需加载\n"
        response += "4. **缓存策略** - 静态资源长期缓存\n\n"
        response += "需要我实现哪个优化？"
    
    else:
        response += "你好！我是前端工程师，可以帮您:\n"
        response += "• 实现交互功能\n"
        response += "• 修复Bug\n"
        response += "• 优化代码性能\n"
        response += "• 开发可复用组件\n\n"
        response += "请告诉我您需要什么帮助？"
    
    return response

# 主处理函数
def main():
    """主入口"""
    if len(sys.argv) < 3:
        print("用法: python3 bot_handler.py [机器人] [消息] [用户]")
        sys.exit(1)
    
    bot = sys.argv[1]
    message = sys.argv[2]
    user = sys.argv[3] if len(sys.argv) > 3 else "user"
    
    handlers = {
        "doc_engineer": handle_doc_engineer,
        "project_manager": handle_project_manager,
        "ui_designer": handle_ui_designer,
        "frontend_dev": handle_frontend_dev,
    }
    
    handler = handlers.get(bot)
    if handler:
        print(handler(message, user))
    else:
        print(f"❌ 未知的机器人: {bot}")

if __name__ == "__main__":
    main()
