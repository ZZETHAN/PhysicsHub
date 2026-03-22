const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// 验证JWT Token
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
        return res.status(401).json({ 
            success: false, 
            message: '请先登录' 
        });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ 
                success: false, 
                message: '登录已过期，请重新登录' 
            });
        }
        req.user = user;
        next();
    });
};

// 验证是否为管理员
const requireAdmin = (req, res, next) => {
    if (req.user.role !== 'admin') {
        return res.status(403).json({ 
            success: false, 
            message: '需要管理员权限' 
        });
    }
    next();
};

// 验证用户是否已通过审核
const requireApproved = (req, res, next) => {
    if (req.user.status !== 'approved') {
        return res.status(403).json({ 
            success: false, 
            message: '账号正在审核中，请等待管理员批准' 
        });
    }
    next();
};

module.exports = {
    JWT_SECRET,
    authenticateToken,
    requireAdmin,
    requireApproved
};
