# PhysicsHub 本地开发环境配置

## 🚀 快速启动

### 1. 启动后端服务器
```bash
cd ~/Desktop/PhysicsHub/api
npm install  # 首次运行
node server.js
```
后端运行在: http://localhost:3001

### 2. 启动前端服务器（新开终端）
```bash
cd ~/Desktop/PhysicsHub
npx http-server -p 8080
```
前端运行在: http://localhost:8080

### 3. 或使用一键启动脚本
```bash
cd ~/Desktop/PhysicsHub
./start-dev.sh
```

## 📁 项目结构

```
~/Desktop/PhysicsHub/
├── index.html              # 首页
├── admin.html              # 管理后台
├── auth/                   # 认证模块
│   ├── auth.js
│   └── auth.css
├── units/                  # 教学单元
│   ├── ch12/
│   ├── ch13/
│   └── ...
└── api/                    # 后端API
    ├── server.js
    ├── database.js
    └── routes/
```

## ⚙️ 本地开发配置

### 后端配置 (api/server.js)
- 端口: 3001
- 数据库: SQLite (api/database.db)
- 管理员账号: admin / admin123

### 前端配置
本地开发时，API_BASE_URL 自动检测：
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:3001/api' 
    : 'http://123.207.75.145:3001/api';
```

## 🧪 测试场景

### 1. 用户注册流程
1. 访问 http://localhost:8080
2. 点击"Log in" → 切换到 Register
3. 填写用户名、邮箱、密码
4. 提交注册
5. 打开 http://localhost:8080/admin.html
6. 查看待审核用户

### 2. 管理员审核
1. 登录 admin 账号
2. 看到 Pending 用户列表
3. 点击 Approve / Reject
4. 用户收到通知（可登录）

## 📱 手机/外网测试（可选）

使用 ngrok 让外网访问本地服务器：
```bash
# 安装 ngrok
brew install ngrok

# 启动后端隧道
grok http 3001
# 获得 https://xxx.ngrok.io → 替换 API_BASE_URL

# 启动前端隧道
grok http 8080
```

## 🔄 开发流程

### 开发新功能
1. **本地开发**
   - 修改代码
   - 本地测试（http://localhost:8080）
   - 调试完成

2. **本地验证**
   - 用户注册 ✓
   - 管理员审核 ✓
   - 功能正常 ✓

3. **部署上线**
   ```bash
   # 同步到服务器
   rsync -avz ~/Desktop/PhysicsHub/ ubuntu@123.207.75.145:/var/www/physicshub/
   
   # 或告诉我"部署"
   ```

### 数据库管理
本地和线上数据库是独立的：
- 本地: `~/Desktop/PhysicsHub/api/database.db`
- 线上: `/var/www/physicshub/api/database.db`

## 📋 待开发功能清单

- [ ] 学生论坛
- [ ] 作业上传系统
- [ ] 聊天室
- [ ] 学习进度追踪
- [ ] 在线测验

## 🛠️ 常用命令

```bash
# 启动后端
cd api && node server.js

# 查看后端日志
tail -f /tmp/server.log

# 重启后端
pkill -f "node server.js" && cd api && node server.js

# 本地访问
open http://localhost:8080
open http://localhost:8080/admin.html
```

## ❓ 常见问题

**Q: 后端启动失败？**
A: 检查端口 3001 是否被占用：`lsof -i :3001`

**Q: 前端无法连接后端？**
A: 确保后端已启动，且 API_BASE_URL 配置正确

**Q: 数据库文件在哪里？**
A: 本地: `~/Desktop/PhysicsHub/api/database.db`

## 📞 需要帮助？

开发完成后告诉我：
1. "功能已完成，本地测试通过"
2. "部署到服务器"
3. 我会帮你同步到线上
