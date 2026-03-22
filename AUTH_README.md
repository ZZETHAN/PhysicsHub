# PhysicsHub 用户认证系统集成指南

## 已完成

### 1. 后端 API (Node.js + Express + SQLite)
- ✅ `api/server.js` - 主服务器
- ✅ `api/database.js` - 数据库初始化 (含管理员账号)
- ✅ `api/routes/auth.js` - 认证路由 (登录/注册/审核)
- ✅ `api/middleware/auth.js` - JWT 验证
- ✅ `api/package.json` - 依赖配置

### 2. 前端认证系统
- ✅ `auth/auth.js` - 认证逻辑 + 登录弹窗
- ✅ `auth/auth.css` - 登录弹窗样式
- ✅ `admin.html` - 管理员审核后台

### 3. 页面集成示例
- ✅ `index.html` - 主页已集成
- ✅ `units/ch17/index.html` - 单元页已集成

## 需要手动完成

### 安装后端依赖
```bash
cd ~/Desktop/PhysicsHub/api
npm install
```

### 启动后端服务器
```bash
node server.js
```

服务器将在 http://localhost:3001 运行

### 集成其他单元页面 (12-16)

每个单元页面需要添加:

1. **在 <head> 中添加 CSS 引用:**
```html
<link rel="stylesheet" href="../../auth/auth.css">
```

2. **在 header 中添加登录按钮区域:**
找到 `A2 LEVEL</div>` 后面，添加:
```html
<div style="display: flex; align-items: center; gap: 12px;">
    <div id="authBtn"></div>
```

3. **在 </body> 前添加 JS 引用:**
```html
<!-- 认证系统 -->
<script src="../../auth/auth.js"></script>
```

## 管理员账号

- **用户名**: admin
- **密码**: admin123
- **登录地址**: http://localhost:3000/admin.html

## 系统特性

1. **用户注册**: 学生填写用户名、邮箱、密码
2. **管理员审核**: 新用户状态为 "pending"，需管理员在后台通过
3. **访问控制**: 
   - 主页可公开访问
   - 教学单元需要登录
   - 未登录用户看到登录弹窗
4. **JWT Token**: 登录后 24 小时有效

## 部署说明

开发完成后需要:
1. 配置生产环境数据库路径
2. 修改 JWT_SECRET 环境变量
3. 修改默认管理员密码
4. 配置 Nginx 反向代理
