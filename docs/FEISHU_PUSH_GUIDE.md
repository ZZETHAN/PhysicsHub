# PhysicsHub 飞书推送 - 使用指南

## 🚀 快速测试

### 1. 测试连接
```bash
cd ~/Desktop/PhysicsHub/scripts
./feishu_push.sh test
```

### 2. 发送测试消息（需要群组ID）
```bash
# 获取群组ID方法：
# 1. 在飞书群组设置中查看
# 2. 或通过API查询

./feishu_push.sh send "oc_xxxxxxxx" "Hello from PhysicsHub!"
```

## 📅 设置定时推送

### 方法1: 添加到系统crontab

```bash
# 编辑crontab
crontab -e

# 添加以下内容（每天早上9点推送）
0 9 * * * cd ~/Desktop/PhysicsHub && ./scripts/daily_report.sh
```

### 方法2: 使用macOS LaunchAgent

创建定时任务配置文件：
```bash
cat > ~/Library/LaunchAgents/ai.physicshub.daily.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.physicshub.daily</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/ethanzhao/Desktop/PhysicsHub/scripts/daily_report.sh</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/ethanzhao/.openclaw/devops/logs/feishu_daily.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/ethanzhao/.openclaw/devops/logs/feishu_daily_error.log</string>
</dict>
</plist>
EOF

# 加载配置
launchctl load ~/Library/LaunchAgents/ai.physicshub.daily.plist
```

## 📱 获取飞书群组ID

### 方法1: 通过飞书API
```bash
# 获取用户加入的群组列表
curl -X GET \
  'https://open.feishu.cn/open-apis/im/v1/chats' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

### 方法2: 通过Webhook
1. 在飞书群组中添加 "自定义机器人"
2. 复制Webhook URL中的 `chat_id` 参数

## 📝 消息格式

### 文本消息
纯文本，支持换行和基础格式。

### 富文本消息（推荐）
```bash
./feishu_push.sh rich "oc_xxx" "📊 进度报告" "**完成度**: 50%\\n\\n**今日任务**:\\n1. 完成Ch 13"
```

## 🔧 故障排除

### 问题1: Token获取失败
```bash
# 检查App ID和Secret
cat ~/.openclaw/extensions/feishu/config/bot_config.yaml

# 重新测试连接
./feishu_push.sh test
```

### 问题2: 消息发送失败
- 检查群组ID是否正确
- 确认机器人已在群组中
- 检查机器人权限设置

### 问题3: 定时任务不执行
```bash
# 检查日志
tail -f ~/.openclaw/devops/logs/feishu_daily.log

# 手动执行测试
./scripts/daily_report.sh
```

## 🎯 进阶用法

### 自定义推送内容
编辑 `scripts/daily_report.sh`，修改 MESSAGE 变量。

### 添加更多定时任务
复制 `daily_report.sh` 创建新的推送脚本：
- `weekly_report.sh` - 周报
- `urgent_notice.sh` - 紧急通知
- `completion_notice.sh` - 完成通知

### 集成到开发流程
在Git提交后自动推送：
```bash
# 添加到 .git/hooks/post-commit
#!/bin/bash
cd ~/Desktop/PhysicsHub
./scripts/feishu_push.sh send "oc_xxx" "✅ 新内容已提交"
```

---

*配置完成 - 运行 ./feishu_push.sh test 测试连接*
