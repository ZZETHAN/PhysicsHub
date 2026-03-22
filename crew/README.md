# PhysicsHub CrewAI 环境配置

## 环境变量设置

### 1. Kimi API Key (必需)
```bash
export KIMI_API_KEY="your-kimi-api-key"
```

获取方式:
- 访问 https://platform.moonshot.cn/
- 创建API Key
- 复制到环境变量

### 2. 添加到 ~/.zshrc (永久生效)
```bash
echo 'export KIMI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

## 安装依赖

```bash
pip3 install crewai langchain-openai
```

## 运行方式

### 方式1: 直接运行
```bash
cd ~/Desktop/PhysicsHub/crew
python3 physics_hub_team.py
```

### 方式2: 使用启动脚本
```bash
~/Desktop/PhysicsHub/scripts/run_crew.sh
```

## 团队成员

| 角色 | 职责 | 输出 |
|------|------|------|
| 文档工程师 | 整理知识点、撰写文档 | HTML文件 |
| 项目助理 | 进度管理、任务规划 | tasks.json |
| UI工程师 | 设计规范、样式优化 | DESIGN_SYSTEM.md |
| 前端工程师 | 组件开发、交互实现 | components.js |

## 任务流程

1. 文档工程师创建Ch 13内容
2. 项目助理制定项目计划
3. UI工程师优化设计系统
4. 前端工程师开发交互组件

（可配置为顺序或并行执行）

## 自定义任务

编辑 `physics_hub_team.py` 修改 `Task` 部分：
- 修改 `description` 更改任务内容
- 修改 `agent` 更换执行者
- 修改 `tasks` 列表调整任务顺序
