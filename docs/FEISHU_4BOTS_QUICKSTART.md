# PhysicsHub 飞书4机器人 - 快速开始指南

## ✅ 状态: 4个机器人已上线！

| 机器人 | 状态 | App ID |
|--------|------|--------|
| 📚 文档工程师 | ✅ 连接成功 | cli_a9339a75b4fadcb5 |
| 📊 项目助理 | ✅ 连接成功 | cli_a9339b17f3f81cba |
| 🎨 UI工程师 | ✅ 连接成功 | cli_a9339b7a57f81ceb |
| 💻 前端工程师 | ✅ 连接成功 | cli_a9339ba0fcf89cca |

---

## 🚀 使用方法

### 1. 添加到飞书群组

在飞书群组中：
1. 点击 **"设置"** → **"群机器人"**
2. 搜索并添加 **4个机器人**
3. 给它们设置昵称：@文档工程师、@项目助理、@UI工程师、@前端工程师

### 2. 测试对话

在群组中@机器人：
```
@文档工程师 整理 Ch 13 知识点
@项目助理 查看项目进度
@UI工程师 设计公式卡片组件
@前端工程师 实现可折叠面板
```

### 3. 共享记忆

4个机器人共用 `/Volumes/大硬盘/OpenViking-Agent-Memory/PhysicsHub/shared_memory.json`

当一个机器人更新内容时，其他机器人自动看到最新状态。

---

## 💬 命令示例

### 📚 文档工程师
```
@文档工程师 整理 Ch 14 电场
@文档工程师 查询向心力公式
@文档工程师 检查 Ch 12 完整性
```

### 📊 项目助理
```
@项目助理 查看进度
@项目助理 创建任务 完成Ch14 @文档工程师 2026-03-25 P1
@项目助理 设置每日提醒
```

### 🎨 UI工程师
```
@UI工程师 设计按钮组件
@UI工程师 配色方案
@UI工程师 检查 Ch 12 样式
```

### 💻 前端工程师
```
@前端工程师 实现交互功能
@前端工程师 修复移动端显示
@前端工程师 优化代码
```

---

## 🔧 管理工具

```bash
# 测试所有机器人连接
bash ~/Desktop/PhysicsHub/scripts/bot_manager.sh test

# 查看状态
bash ~/Desktop/PhysicsHub/scripts/bot_manager.sh status

# 同步共享记忆
bash ~/Desktop/PhysicsHub/scripts/bot_manager.sh sync
```

---

## 📁 配置文件

```
~/.openclaw/extensions/feishu/physicshub_bots.yaml
~/Desktop/PhysicsHub/scripts/bot_handler.py
~/Desktop/PhysicsHub/scripts/bot_manager.sh
```

---

## 🎯 下一步

1. ✅ 在飞书群组中添加4个机器人
2. ✅ 测试@对话功能
3. ✅ 开始协作开发PhysicsHub

**现在可以去飞书群组中@机器人测试了！**
