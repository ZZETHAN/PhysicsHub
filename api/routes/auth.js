const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../database');
const { JWT_SECRET, authenticateToken, requireAdmin, requireApproved } = require('../middleware/auth');

const router = express.Router();

// ========== 公开接口 ==========

// 注册 - 需要管理员审核
router.post('/register', (req, res) => {
    const { username, email, password } = req.body;

    // 验证输入
    if (!username || !email || !password) {
        return res.status(400).json({ 
            success: false, 
            message: '请填写所有必填字段' 
        });
    }

    // 验证邮箱格式
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return res.status(400).json({ 
            success: false, 
            message: '请输入有效的邮箱地址' 
        });
    }

    // 验证密码强度
    if (password.length < 6) {
        return res.status(400).json({ 
            success: false, 
            message: '密码至少需要6位字符' 
        });
    }

    // 验证用户名
    if (username.length < 3 || username.length > 20) {
        return res.status(400).json({ 
            success: false, 
            message: '用户名长度需要在3-20个字符之间' 
        });
    }

    const passwordHash = bcrypt.hashSync(password, 10);

    db.run(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        [username, email, passwordHash],
        function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed')) {
                    if (err.message.includes('username')) {
                        return res.status(400).json({ 
                            success: false, 
                            message: '用户名已被使用' 
                        });
                    }
                    if (err.message.includes('email')) {
                        return res.status(400).json({ 
                            success: false, 
                            message: '邮箱已被注册' 
                        });
                    }
                }
                return res.status(500).json({ 
                    success: false, 
                    message: '注册失败，请稍后重试' 
                });
            }

            res.json({ 
                success: true, 
                message: '注册申请已提交，请等待管理员审核通过后即可登录' 
            });
        }
    );
});

// 登录
router.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ 
            success: false, 
            message: '请填写用户名和密码' 
        });
    }

    db.get(
        'SELECT * FROM users WHERE username = ? OR email = ?',
        [username, username],
        (err, user) => {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '登录失败，请稍后重试' 
                });
            }

            if (!user) {
                return res.status(401).json({ 
                    success: false, 
                    message: '用户名或密码错误' 
                });
            }

            // 检查账号状态
            if (user.status === 'pending') {
                return res.status(403).json({ 
                    success: false, 
                    message: '账号正在审核中，请等待管理员批准' 
                });
            }

            if (user.status === 'rejected') {
                return res.status(403).json({ 
                    success: false, 
                    message: '注册申请未通过审核，请联系管理员' 
                });
            }

            // 验证密码
            if (!bcrypt.compareSync(password, user.password_hash)) {
                return res.status(401).json({ 
                    success: false, 
                    message: '用户名或密码错误' 
                });
            }

            // 更新最后登录时间
            db.run('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', [user.id]);

            // 生成 JWT Token
            const token = jwt.sign(
                { 
                    userId: user.id, 
                    username: user.username, 
                    role: user.role,
                    status: user.status 
                },
                JWT_SECRET,
                { expiresIn: '24h' }
            );

            res.json({
                success: true,
                message: '登录成功',
                token,
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    role: user.role,
                    avatar_color: user.avatar_color,
                    avatar_icon: user.avatar_icon
                }
            });
        }
    );
});

// 获取当前用户信息
router.get('/me', authenticateToken, (req, res) => {
    db.get(
        'SELECT id, username, email, role, status, created_at, avatar_color, avatar_icon FROM users WHERE id = ?',
        [req.user.userId],
        (err, user) => {
            if (err || !user) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ success: true, user });
        }
    );
});

// 更新个人资料
router.put('/profile', authenticateToken, (req, res) => {
    const userId = req.user.userId;
    const { username, email, avatar_color, avatar_icon } = req.body;

    if (!username && !email && avatar_color === undefined && avatar_icon === undefined) {
        return res.status(400).json({
            success: false,
            message: '没有要更新的字段'
        });
    }

    const updates = [];
    const params = [];

    if (username) {
        if (username.length < 3 || username.length > 20) {
            return res.status(400).json({
                success: false,
                message: '用户名长度需要在3-20个字符之间'
            });
        }
        updates.push('username = ?');
        params.push(username);
    }

    if (email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({
                success: false,
                message: '请输入有效的邮箱地址'
            });
        }
        updates.push('email = ?');
        params.push(email);
    }

    if (avatar_color !== undefined) {
        updates.push('avatar_color = ?');
        params.push(avatar_color);
    }

    if (avatar_icon !== undefined) {
        updates.push('avatar_icon = ?');
        params.push(avatar_icon);
    }

    params.push(userId);

    db.run(
        `UPDATE users SET ${updates.join(', ')} WHERE id = ?`,
        params,
        function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed')) {
                    return res.status(400).json({
                        success: false,
                        message: '用户名或邮箱已被使用'
                    });
                }
                return res.status(500).json({
                    success: false,
                    message: '更新失败'
                });
            }
            res.json({
                success: true,
                message: '个人资料已更新'
            });
        }
    );
});

// 修改密码
router.put('/password', authenticateToken, (req, res) => {
    const userId = req.user.userId;
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
        return res.status(400).json({
            success: false,
            message: '请填写所有字段'
        });
    }

    if (newPassword.length < 6) {
        return res.status(400).json({
            success: false,
            message: '新密码至少需要6位字符'
        });
    }

    db.get('SELECT password_hash FROM users WHERE id = ?', [userId], (err, user) => {
        if (err || !user) {
            return res.status(404).json({
                success: false,
                message: '用户不存在'
            });
        }

        if (!bcrypt.compareSync(currentPassword, user.password_hash)) {
            return res.status(401).json({
                success: false,
                message: '当前密码错误'
            });
        }

        const passwordHash = bcrypt.hashSync(newPassword, 10);
        db.run('UPDATE users SET password_hash = ? WHERE id = ?', [passwordHash, userId], function(err) {
            if (err) {
                return res.status(500).json({
                    success: false,
                    message: '密码修改失败'
                });
            }
            res.json({
                success: true,
                message: '密码已修改'
            });
        });
    });
});

// ========== 管理员接口 ==========

// 获取所有用户列表 (支持分页和筛选)
router.get('/admin/users', authenticateToken, requireAdmin, (req, res) => {
    const { status, role, search, page = 1, limit = 10 } = req.query;
    
    let whereClause = 'WHERE 1=1';
    const params = [];
    
    if (status) {
        whereClause += ' AND status = ?';
        params.push(status);
    }
    
    if (role) {
        whereClause += ' AND role = ?';
        params.push(role);
    }
    
    if (search) {
        whereClause += ' AND (username LIKE ? OR email LIKE ?)';
        params.push(`%${search}%`, `%${search}%`);
    }
    
    // 获取总数
    db.get(`SELECT COUNT(*) as total FROM users ${whereClause}`, params, (err, countRow) => {
        if (err) {
            return res.status(500).json({ 
                success: false, 
                message: '获取失败' 
            });
        }
        
        // 获取分页数据
        const offset = (parseInt(page) - 1) * parseInt(limit);
        const queryParams = [...params, parseInt(limit), offset];
        
        db.all(
            `SELECT id, username, email, status, role, created_at, approved_at, last_login, avatar_color, avatar_icon 
             FROM users ${whereClause} 
             ORDER BY created_at DESC 
             LIMIT ? OFFSET ?`,
            queryParams,
            (err, users) => {
                if (err) {
                    return res.status(500).json({ 
                        success: false, 
                        message: '获取失败' 
                    });
                }
                res.json({ 
                    success: true, 
                    users,
                    pagination: {
                        total: countRow.total,
                        page: parseInt(page),
                        limit: parseInt(limit),
                        totalPages: Math.ceil(countRow.total / parseInt(limit))
                    }
                });
            }
        );
    });
});

// 获取用户统计数据
router.get('/admin/stats', authenticateToken, requireAdmin, (req, res) => {
    db.get(
        `SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
            SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected
         FROM users`,
        (err, stats) => {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '获取统计数据失败' 
                });
            }
            
            // 获取今日新增
            db.get(
                `SELECT COUNT(*) as today FROM users 
                 WHERE DATE(created_at) = DATE('now')`,
                (err, todayRow) => {
                    if (err) {
                        return res.status(500).json({ 
                            success: false, 
                            message: '获取统计数据失败' 
                        });
                    }
                    
                    res.json({ 
                        success: true, 
                        stats: {
                            ...stats,
                            today: todayRow.today
                        }
                    });
                }
            );
        }
    );
});

// 获取单个用户详情
router.get('/admin/users/:id', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    
    db.get(
        `SELECT u.*, a.username as approved_by_name 
         FROM users u 
         LEFT JOIN users a ON u.approved_by = a.id 
         WHERE u.id = ?`,
        [userId],
        (err, user) => {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '获取失败' 
                });
            }
            if (!user) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ success: true, user });
        }
    );
});

// 更新用户信息
router.put('/admin/users/:id', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    const { username, email, role, status } = req.body;
    
    const updates = [];
    const params = [];
    
    if (username) {
        updates.push('username = ?');
        params.push(username);
    }
    if (email) {
        updates.push('email = ?');
        params.push(email);
    }
    if (role) {
        updates.push('role = ?');
        params.push(role);
    }
    if (status) {
        updates.push('status = ?');
        params.push(status);
        if (status === 'approved') {
            updates.push('approved_at = CURRENT_TIMESTAMP');
            updates.push('approved_by = ?');
            params.push(req.user.userId);
        }
    }
    
    if (updates.length === 0) {
        return res.status(400).json({ 
            success: false, 
            message: '没有要更新的字段' 
        });
    }
    
    params.push(userId);
    
    db.run(
        `UPDATE users SET ${updates.join(', ')} WHERE id = ?`,
        params,
        function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed')) {
                    return res.status(400).json({ 
                        success: false, 
                        message: '用户名或邮箱已被使用' 
                    });
                }
                return res.status(500).json({ 
                    success: false, 
                    message: '更新失败' 
                });
            }
            if (this.changes === 0) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ 
                success: true, 
                message: '用户信息已更新' 
            });
        }
    );
});

// 审核通过用户
router.post('/admin/approve/:id', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    
    db.run(
        'UPDATE users SET status = ?, approved_at = CURRENT_TIMESTAMP, approved_by = ? WHERE id = ?',
        ['approved', req.user.userId, userId],
        function(err) {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '审核失败' 
                });
            }
            if (this.changes === 0) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ 
                success: true, 
                message: '审核通过' 
            });
        }
    );
});

// 拒绝用户注册
router.post('/admin/reject/:id', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    
    db.run(
        'UPDATE users SET status = ?, approved_by = ? WHERE id = ?',
        ['rejected', req.user.userId, userId],
        function(err) {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '操作失败' 
                });
            }
            if (this.changes === 0) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ 
                success: true, 
                message: '已拒绝该用户的注册申请' 
            });
        }
    );
});

// 批量操作用户
router.post('/admin/batch', authenticateToken, requireAdmin, (req, res) => {
    const { ids, action } = req.body;
    
    if (!Array.isArray(ids) || ids.length === 0) {
        return res.status(400).json({ 
            success: false, 
            message: '请选择要操作的用户' 
        });
    }
    
    if (!['approve', 'reject', 'delete'].includes(action)) {
        return res.status(400).json({ 
            success: false, 
            message: '无效的操作类型' 
        });
    }
    
    const placeholders = ids.map(() => '?').join(',');
    let sql;
    let params;
    
    switch (action) {
        case 'approve':
            sql = `UPDATE users SET status = 'approved', approved_at = CURRENT_TIMESTAMP, approved_by = ? 
                   WHERE id IN (${placeholders})`;
            params = [req.user.userId, ...ids];
            break;
        case 'reject':
            sql = `UPDATE users SET status = 'rejected', approved_by = ? 
                   WHERE id IN (${placeholders})`;
            params = [req.user.userId, ...ids];
            break;
        case 'delete':
            // 不能删除自己
            if (ids.includes(req.user.userId.toString())) {
                return res.status(400).json({ 
                    success: false, 
                    message: '不能删除当前登录的账号' 
                });
            }
            sql = `DELETE FROM users WHERE id IN (${placeholders})`;
            params = ids;
            break;
    }
    
    db.run(sql, params, function(err) {
        if (err) {
            return res.status(500).json({ 
                success: false, 
                message: '批量操作失败' 
            });
        }
        
        const actionText = {
            approve: '批准',
            reject: '拒绝',
            delete: '删除'
        };
        
        res.json({ 
            success: true, 
            message: `已成功${actionText[action]} ${this.changes} 个用户`,
            affected: this.changes
        });
    });
});

// 删除用户
router.delete('/admin/users/:id', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    
    // 不能删除自己
    if (parseInt(userId) === req.user.userId) {
        return res.status(400).json({ 
            success: false, 
            message: '不能删除当前登录的账号' 
        });
    }
    
    db.run('DELETE FROM users WHERE id = ?', [userId], function(err) {
        if (err) {
            return res.status(500).json({ 
                success: false, 
                message: '删除失败' 
            });
        }
        if (this.changes === 0) {
            return res.status(404).json({ 
                success: false, 
                message: '用户不存在' 
            });
        }
        res.json({ 
            success: true, 
            message: '用户已删除' 
        });
    });
});

// 重置用户密码
router.post('/admin/users/:id/reset-password', authenticateToken, requireAdmin, (req, res) => {
    const userId = req.params.id;
    const { newPassword } = req.body;
    
    if (!newPassword || newPassword.length < 6) {
        return res.status(400).json({ 
            success: false, 
            message: '新密码至少需要6位字符' 
        });
    }
    
    const passwordHash = bcrypt.hashSync(newPassword, 10);
    
    db.run(
        'UPDATE users SET password_hash = ? WHERE id = ?',
        [passwordHash, userId],
        function(err) {
            if (err) {
                return res.status(500).json({ 
                    success: false, 
                    message: '密码重置失败' 
                });
            }
            if (this.changes === 0) {
                return res.status(404).json({ 
                    success: false, 
                    message: '用户不存在' 
                });
            }
            res.json({ 
                success: true, 
                message: '密码已重置' 
            });
        }
    );
});

module.exports = router;
