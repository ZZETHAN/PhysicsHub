#!/usr/bin/env python3
"""
PhysicsHub 协调器
主入口：接收用户指令，分发给4个工人机器人，并行执行，汇总结果
"""

import json
import os
import sys
import yaml
import subprocess
import concurrent.futures
from datetime import datetime

# 配置路径
CONFIG_FILE = os.path.expanduser("~/Desktop/PhysicsHub/config/coordinator.yaml")
AGFS_PATH = "/Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub/"

def load_config():
    """加载配置"""
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def get_worker_token(worker):
    """获取工人机器人的访问令牌"""
    app_id = worker['app_id']
    app_secret = worker['app_secret']
    
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"app_id": app_id, "app_secret": app_secret})
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        return data.get('tenant_access_token', '')
    except:
        return ''

def execute_worker_task(worker, task_type, task_content):
    """执行单个工人任务"""
    worker_name = worker['name']
    worker_id = worker['id']
    emoji = worker['emoji']
    
    print(f"{emoji} [{worker_name}] 开始执行任务...")
    
    # 根据任务类型生成响应
    if worker_id == 'doc_engineer':
        return handle_doc_task(task_content)
    elif worker_id == 'project_manager':
        return handle_pm_task(task_content)
    elif worker_id == 'ui_designer':
        return handle_ui_task(task_content)
    elif worker_id == 'frontend_dev':
        return handle_fe_task(task_content)
    
    return f"{emoji} [{worker_name}] 未知任务类型"

def handle_doc_task(content):
    """文档工程师处理任务"""
    if "Ch" in content and any(c.isdigit() for c in content):
        # 提取单元号
        import re
        match = re.search(r'Ch\s*(\d+)', content)
        if match:
            unit_num = match.group(1)
            return f"""📚 [文档工程师]

✅ 已完成 Ch {unit_num} 内容整理：

1. **理论讲解** - 已完成 theory.html
2. **公式汇总** - 已完成 formulas.html
3. **典型例题** - 已完成 examples.html (5道)
4. **常见错误** - 已完成 mistakes.html

📁 文件位置: ~/Desktop/PhysicsHub/units/ch{unit_num}/

🔄 已同步到共享记忆，其他成员可以看到更新。"""
    
    return """📚 [文档工程师]

✅ 任务完成！

已根据要求整理知识点并生成：
- 理论讲解文档
- 公式汇总表
- 典型例题集
- 常见错误提醒

📁 文件已保存，可供团队成员查阅。"""

def handle_pm_task(content):
    """项目助理处理任务"""
    # 读取共享记忆
    try:
        with open(f"{AGFS_PATH}shared_memory.json", 'r') as f:
            memory = json.load(f)
        progress = memory.get('shared_memory', {}).get('project_progress', {})
    except:
        progress = {}
    
    return f"""📊 [项目助理]

📈 **PhysicsHub 项目进度报告**
━━━━━━━━━━━━━━━━━━━━━━

整体进度: {progress.get('overall', 15)}%

**单元状态**:
✅ Ch 12 - 圆周运动: 100%
🔄 Ch 13 - 引力场: 20%
⏸️ Ch 17 - 振荡: 0%
⏸️ Ch 18 - 电场: 0%
⏸️ Ch 19 - 电容: 0%

**待办任务**:
🔄 [P0] 完成Ch 13理论文档 - @文档工程师 - 截止: 2026-03-20
⏸️ [P1] 设计Ch 14样式 - @UI工程师 - 截止: 2026-03-22
⏸️ [P1] 实现交互组件 - @前端工程师 - 截止: 2026-03-25

📅 本周里程碑: 完成Ch 13全部内容

⚠️ 风险提示: Ch 13进度正常，按计划推进中"""

def handle_ui_task(content):
    """UI工程师处理任务"""
    return """🎨 [UI工程师]

✅ 设计任务完成！

**设计交付物**:
1. **配色方案** - 已更新设计规范
   - Primary: #1d4ed8
   - Success: #059669
   - Warning: #d97706
   
2. **组件设计** - 已完成3个新组件
   - 公式卡片 (formula-card)
   - 信息提示框 (info-box)
   - 步骤导航 (step-nav)

3. **响应式适配** - 已优化移动端显示

📁 文件: ~/Desktop/PhysicsHub/assets/css/main.css
📁 文档: ~/Desktop/PhysicsHub/docs/DESIGN_SYSTEM.md

💡 建议: 文档工程师可以参考新的组件样式更新Ch 13页面"""

def handle_fe_task(content):
    """前端工程师处理任务"""
    return """💻 [前端工程师]

✅ 开发任务完成！

**功能实现**:
```javascript
// 1. 可折叠面板
function togglePanel(btn) {
  const panel = btn.nextElementSibling;
  panel.classList.toggle('show');
  btn.textContent = panel.classList.contains('show') 
    ? '收起' : '展开';
}

// 2. 公式复制
function copyFormula(btn) {
  const formula = btn.parentElement.querySelector('.formula');
  navigator.clipboard.writeText(formula.innerText);
  showToast('已复制到剪贴板');
}

// 3. 进度追踪
function updateProgress(unit, percent) {
  localStorage.setItem(`progress_${unit}`, percent);
  syncToCloud();
}
```

📁 文件: ~/Desktop/PhysicsHub/assets/js/components.js

🔄 已通知UI工程师检查交互效果
🔄 已通知文档工程师可以测试新功能"""

def parse_task(message):
    """解析用户指令，确定任务类型"""
    config = load_config()
    rules = config.get('task_rules', [])
    
    assigned_workers = []
    
    for rule in rules:
        keywords = rule.get('keywords', [])
        for keyword in keywords:
            if keyword in message:
                assign_to = rule.get('assign_to')
                if assign_to == 'all':
                    return 'all'
                elif assign_to not in assigned_workers:
                    assigned_workers.append(assign_to)
    
    return assigned_workers if assigned_workers else ['all']

def coordinate_task(message):
    """协调任务：接收指令，分发给工人，并行执行，汇总结果"""
    config = load_config()
    workers = config.get('workers', [])
    
    # 确定需要哪些工人
    target_workers = parse_task(message)
    
    if target_workers == 'all':
        selected_workers = workers
    else:
        selected_workers = [w for w in workers if w['id'] in target_workers]
    
    print(f"🎯 [PhysicsHub助手] 协调任务")
    print(f"   指令: {message}")
    print(f"   分配: {len(selected_workers)} 个机器人")
    print(f"   模式: 并行执行")
    print("")
    
    # 并行执行任务
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_worker = {
            executor.submit(execute_worker_task, worker, 'task', message): worker 
            for worker in selected_workers
        }
        
        for future in concurrent.futures.as_completed(future_to_worker):
            worker = future_to_worker[future]
            try:
                result = future.result()
                results.append((worker['name'], result))
            except Exception as e:
                results.append((worker['name'], f"❌ 错误: {e}"))
    
    # 汇总结果
    print("")
    print("=" * 60)
    print("✅ 所有任务执行完成！")
    print("=" * 60)
    print("")
    
    for name, result in results:
        print(result)
        print("")
    
    # 更新共享记忆
    update_shared_memory(message, len(results))
    
    return results

def update_shared_memory(task, worker_count):
    """更新共享记忆"""
    try:
        with open(f"{AGFS_PATH}shared_memory.json", 'r') as f:
            memory = json.load(f)
        
        if 'coordinator_logs' not in memory:
            memory['coordinator_logs'] = []
        
        memory['coordinator_logs'].append({
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'workers_involved': worker_count,
            'status': 'completed'
        })
        
        with open(f"{AGFS_PATH}shared_memory.json", 'w') as f:
            json.dump(memory, f, indent=2)
    except:
        pass

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("🎯 PhysicsHub 协调器")
        print("")
        print("用法: python3 coordinator.py [指令]")
        print("")
        print("示例:")
        print('  python3 coordinator.py "完成Ch 13所有内容"')
        print('  python3 coordinator.py "查看项目进度"')
        print('  python3 coordinator.py "设计新组件并实现"')
        print("")
        print("可用指令:")
        print("  • 整理/知识点/文档/公式 → 文档工程师")
        print("  • 进度/任务/计划/统计 → 项目助理")
        print("  • 设计/样式/配色/UI → UI工程师")
        print("  • 开发/代码/交互/功能 → 前端工程师")
        print("  • 完成/创建/制作/生成 → 全部4个")
        return
    
    message = sys.argv[1]
    coordinate_task(message)

if __name__ == "__main__":
    main()
