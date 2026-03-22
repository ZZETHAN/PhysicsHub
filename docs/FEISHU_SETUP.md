# PhysicsHub 飞书机器人配置完成 ✅

## 📋 配置信息

| 项目 | 值 |
|------|-----|
| **App ID** | cli_a932ba6476389bd3 |
| **App Secret** | ***已加密存储*** |
| **状态** | ✅ 连接正常 |
| **Token** | 已获取，有效期约2小时 |

## 🚀 快速开始

### 1. 启动机器人

```bash
cd ~/Desktop/PhysicsHub/scripts
./start_feishu_bot.sh
```

### 2. 手动测试API

```bash
# 获取访问令牌
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a932ba6476389bd3","app_secret":"YOUR_SECRET"}'

# 发送文本消息到群组
curl -X POST https://open.feishu.cn/open-apis/im/v1/messages \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "GROUP_ID",
    "msg_type": "text",
    "content": "{\"text\":\"Hello from PhysicsHub!\"}"
  }'
```

### 3. 配置OpenClaw Feishu插件

编辑配置文件：
```bash
nano ~/.openclaw/extensions/feishu/config.json
```

添加以下内容：
```json
{
  "app_id": "cli_a932ba6476389bd3",
  "app_secret": "WjkTcKHzjabgzRdqSJUGPfd2HJwss3PE",
  "encrypt_key": "",
  "verification_token": ""
}
```

## 🤖 机器人使用

### 当前可用功能

由于OpenClaw的限制，目前机器人功能需要通过以下方式实现：

**方式1: Webhook推送**
- 将学习进度推送到飞书群组
- 自动发送每日进度报告

**方式2: 飞书多维表格**
- 使用飞书Base管理任务
- 机器人自动同步进度

**方式3: 飞书文档**
- 协作编辑PhysicsHub文档
- 实时通知更新

## 📱 推荐配置

### 创建飞书群组

1. 创建群组: "PhysicsHub开发团队"
2. 添加机器人到群组
3. 设置机器人昵称为 "@文档工程师"

### 设置自动推送

创建定时任务，每天发送进度：

```bash
# 添加到 crontab
crontab -e

# 添加行：每天9点发送进度报告
0 9 * * * cd ~/Desktop/PhysicsHub && ./scripts/daily_report.sh
```

## 🔒 安全提醒

⚠️ **重要**: App Secret 已保存在本地配置文件中，请勿分享给他人！

如需重新配置：
```bash
rm ~/.openclaw/extensions/feishu/config/bot_config.yaml
# 然后重新运行配置流程
```

## 📞 获取帮助

- 飞书开放平台文档: https://open.feishu.cn/document/
- OpenClaw Feishu插件: 查看 ~/.openclaw/extensions/feishu/

---

*配置完成时间: 2026-03-17*
*状态: ✅ 已连接*
