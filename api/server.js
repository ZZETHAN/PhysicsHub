const express = require('express');
const cors = require('cors');
const path = require('path');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3001;

// 请求限制
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15分钟
    max: 100, // 每个IP最多100个请求
    message: { success: false, message: '请求过于频繁，请稍后再试' }
});

// 中间件
app.use(cors());
app.use(express.json());
app.use(limiter);

// API 路由
app.use('/api/auth', require('./routes/auth'));
app.use('/api/progress', require('./routes/progress'));

// 健康检查
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 错误处理
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ success: false, message: '服务器内部错误' });
});

app.listen(PORT, () => {
    console.log(`🚀 PhysicsHub API Server running on port ${PORT}`);
    console.log(`📁 Database: ${path.join(__dirname, 'database.db')}`);
    console.log(`🔑 Admin login: username="admin", password="admin123"`);
    console.log(`⚠️  Remember to change the default admin password!`);
});
