# PhysicsHub 团队 - 机器人员工配置

## 🤖 团队成员列表（已上线）

### 1. 📚 文档工程师
**Session Key**: `agent:main:subagent:78102189-d56e-4086-a33c-8aa247b3f2cd`
**职责**: 知识点整理、文档撰写、公式汇总

**对话方式**:
```
sessions_send
sessionKey: agent:main:subagent:78102189-d56e-4086-a33c-8aa247b3f2cd
message: 整理 Ch 13 引力场知识点
```

### 2. 📊 项目助理  
**Session Key**: `agent:main:subagent:a26fb000-b33d-4630-b680-87534e77e681`
**职责**: 进度跟踪、任务管理、统计报告

**对话方式**:
```
sessions_send
sessionKey: agent:main:subagent:a26fb000-b33d-4630-b680-87534e77e681  
message: 查看当前项目进度
```

### 3. 🎨 UI工程师
**Session Key**: `agent:main:subagent:51f82b13-d4f6-4e7e-b34d-ecae1b6be74f`
**职责**: 界面设计、CSS样式、配色方案

**对话方式**:
```
sessions_send
sessionKey: agent:main:subagent:51f82b13-d4f6-4e7e-b34d-ecae1b6be74f
message: 设计公式卡片组件
```

### 4. 💻 前端工程师
**Session Key**: `agent:main:subagent:4518b346-3a16-4f46-85e8-4827fae9ce7b`
**职责**: HTML开发、JavaScript交互、组件实现

**对话方式**:
```
sessions_send
sessionKey: agent:main:subagent:4518b346-3a16-4f46-85e8-4827fae9ce7b
message: 创建可折叠面板交互
```

### 5. 🎯 产品经理（你）
**角色**: 需求决策、资源协调、最终审核
**操作**: 直接在当前会话对话

---

## 💬 快速对话指南

### 方式1: 通过主会话（我帮你转发）
直接告诉我：
```
告诉文档工程师整理Ch13
让项目助理查进度
叫UI工程师设计个按钮
```

### 方式2: 直接对话（使用session keys）
如果需要直接和某个机器人对话，使用上述session keys

### 方式3: 创建独立聊天（推荐）
为每个机器人创建独立的飞书/Discord频道，完全分离对话

---

## 📋 任务分配示例

**你**: 告诉文档工程师整理 Ch 13 知识点

**我（转发给文档工程师）** → 文档工程师回复 → 我转发给你

**你**: 让项目助理设置本周任务

**我（转发给项目助理）** → 项目助理回复 → 我转发给你

---

## 🔧 管理命令

```bash
# 查看所有团队成员状态
subagents list

# 给指定成员发消息
sessions_send sessionKey:xxx message:xxx

# 查看成员历史消息
sessions_history sessionKey:xxx
```

---

*配置时间: 2026-03-17*
*状态: ✅ 所有成员已上线*
