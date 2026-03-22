# PhysicsHub 开发注意事项

## ⚠️ 重要：部署时禁止覆盖的文件

**`database.db`** - 用户数据存储，禁止覆盖！

部署必须使用 `scripts/deploy_physicshub.sh` 脚本，该脚本已排除 `database.db`。

## 服务器信息

- **IP**: 123.207.75.145
- **网站根目录**: `/var/www/physicshub`
- **API 目录**: `/opt/physicshub/api`
- **API 运行端口**: 3001

## 部署命令

```bash
cd ~/Desktop/PhysicsHub && ./scripts/deploy_physicshub.sh
```

## API 端点

### 认证相关
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录
- `GET /api/auth/me` - 获取当前用户
- `PUT /api/auth/profile` - 更新个人资料
- `PUT /api/auth/password` - 修改密码

### 进度相关
- `GET /api/progress/stats` - 获取进度统计
- `PUT /api/progress/:unitId` - 更新单元进度

## 数据库表

- `users` - 用户表
- `user_progress` - 学习进度表

## 常用操作

### 重启 API 服务
```bash
ssh ubuntu@123.207.75.145
sudo pkill -f 'node server.js'
cd /opt/physicshub/api && node server.js
```

### 检查 API 健康状态
```bash
curl http://localhost:3001/api/health
```

### 查看服务器日志
```bash
ssh ubuntu@123.207.75.145 "tail -f /tmp/server.log"
```
