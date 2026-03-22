# PhysicsHub CrewAI 多Agent团队配置
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 使用 Kimi API (通过OpenAI兼容接口)
llm = ChatOpenAI(
    model="kimi-coding/k2p5",
    api_key=os.getenv("KIMI_API_KEY", "your-api-key"),
    base_url="https://api.moonshot.cn/v1"
)

# ============ 4个机器人员工 ============

# 1. 文档工程师
doc_engineer = Agent(
    role='文档工程师',
    goal='整理A-Level物理知识点，撰写高质量教学文档',
    backstory='''你是一位资深的A-Level物理教育专家，擅长：
    - 将复杂物理概念转化为易懂的教学内容
    - 整理系统化的知识点框架
    - 编写清晰的公式推导和例题解析
    - 使用中英双语撰写文档
    
    你工作严谨，注重细节，确保每个知识点都准确无误。''',
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# 2. 项目助理
project_manager = Agent(
    role='项目助理',
    goal='高效管理PhysicsHub项目进度，确保按时交付',
    backstory='''你是一位经验丰富的项目助理，擅长：
    - 制定项目计划和里程碑
    - 跟踪任务进度并及时提醒
    - 协调团队成员工作
    - 生成进度报告和统计数据
    
    你做事有条理，善于发现问题并推动解决。''',
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# 3. UI工程师
ui_designer = Agent(
    role='UI工程师',
    goal='打造美观、易用的PhysicsHub界面设计',
    backstory='''你是一位有教育产品经验的UI设计师，擅长：
    - 设计简洁专业的学习界面
    - 制定统一的视觉规范（配色、字体、间距）
    - 编写高质量的CSS代码
    - 优化用户体验和可读性
    
    你注重细节，追求完美的视觉效果。''',
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# 4. 前端工程师
frontend_dev = Agent(
    role='前端工程师',
    goal='开发高质量、交互流畅的PhysicsHub前端页面',
    backstory='''你是一位精通现代前端技术的工程师，擅长：
    - 编写语义化的HTML结构
    - 实现复杂的JavaScript交互
    - 开发可复用的组件
    - 优化代码性能和可维护性
    
    你代码风格清晰，注重最佳实践。''',
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# ============ 示例任务 ============

# 任务1: 创建Ch 13引力场内容
task_ch13_content = Task(
    description='''
    创建Ch 13 引力场(Gravitational Field)的完整教学内容：
    
    1. 在 ~/Desktop/PhysicsHub/units/ch13/ 目录下创建以下文件：
       - theory.html: 理论讲解（牛顿万有引力定律、引力场强度、引力势等）
       - formulas.html: 公式汇总（F=Gm₁m₂/r², g=GM/r², φ=-GM/r等）
       - examples.html: 3道典型例题（卫星轨道、逃逸速度、引力势能计算）
    
    2. 参考Ch 12的格式和样式
    3. 使用PhysicsHub设计规范（main.css）
    4. 内容要详细，适合A-Level学生学习
    
    完成后报告：创建的文件列表、内容概要
    ''',
    agent=doc_engineer,
    expected_output='完整的Ch 13教学文件（theory.html, formulas.html, examples.html）'
)

# 任务2: 项目进度规划
task_project_plan = Task(
    description='''
    为PhysicsHub项目制定详细的项目计划：
    
    1. 分析当前状态：
       - Ch 12 已完成
       - Ch 13 待完成
       - Ch 17-25 (A2单元) 待开发
    
    2. 创建任务清单（写入 ~/Desktop/PhysicsHub/config/tasks.json）：
       - 每个单元的子任务（理论、公式、例题、测试）
       - 优先级（P0/P1/P2）
       - 预估工时
       - 依赖关系
    
    3. 制定里程碑：
       - Phase 1: AS单元 (Ch12-13) - 3月20日
       - Phase 2: 核心A2 (Ch17-20) - 3月27日
       - Phase 3: 全部完成 - 4月10日
    
    4. 生成甘特图数据
    
    完成后报告：任务清单摘要、关键路径分析
    ''',
    agent=project_manager,
    expected_output='项目计划文档和tasks.json配置文件'
)

# 任务3: 设计系统优化
task_design_system = Task(
    description='''
    优化PhysicsHub的设计系统：
    
    1. 检查现有设计（~/Desktop/PhysicsHub/assets/css/main.css）：
       - 颜色系统是否完整
       - 字体大小是否合适
       - 间距是否一致
    
    2. 创建设计规范文档（~/Desktop/PhysicsHub/docs/DESIGN_SYSTEM.md）：
       - 色彩体系（主色、辅助色、状态色）
       - 字体规范（标题、正文、代码字体）
       - 间距系统（8px基准）
       - 组件规范（按钮、卡片、表格）
    
    3. 提供组件代码示例：
       - 信息框组件
       - 公式展示组件
       - 步骤导航组件
    
    完成后报告：设计改进建议、新增组件列表
    ''',
    agent=ui_designer,
    expected_output='设计规范文档和组件代码'
)

# 任务4: 交互组件开发
task_interactive_components = Task(
    description='''
    为PhysicsHub开发交互组件：
    
    1. 在 ~/Desktop/PhysicsHub/assets/js/ 目录下创建 components.js：
       
       a) 可折叠面板（Accordion）
          - 用于FAQ、步骤展示
          - 平滑动画效果
       
       b) 公式复制按钮
          - 点击复制公式到剪贴板
          - 显示复制成功提示
       
       c) 进度追踪器
          - 显示学习进度
          - 本地存储进度数据
       
       d) 暗夜模式切换
          - 切换浅色/深色主题
          - 记住用户偏好
    
    2. 创建演示页面（~/Desktop/PhysicsHub/demo/components.html）
    
    3. 编写使用文档
    
    完成后报告：组件功能列表、使用示例
    ''',
    agent=frontend_dev,
    expected_output='components.js文件和演示页面'
)

# ============ Crew配置 ============

# 创建Crew（顺序执行）
physics_hub_crew = Crew(
    agents=[doc_engineer, project_manager, ui_designer, frontend_dev],
    tasks=[task_ch13_content, task_project_plan, task_design_system, task_interactive_components],
    process=Process.sequential,  # 顺序执行，也可改为Process.parallel并行
    verbose=True
)

# 启动函数
def run_crew():
    """启动PhysicsHub团队协作"""
    print("🚀 启动PhysicsHub多Agent协作团队")
    print("=" * 50)
    result = physics_hub_crew.kickoff()
    print("\n" + "=" * 50)
    print("✅ 所有任务执行完成！")
    print(f"\n结果:\n{result}")
    return result

if __name__ == "__main__":
    run_crew()
