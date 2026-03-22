const express = require('express');
const db = require('../database');
const { authenticateToken } = require('../middleware/auth');

const router = express.Router();

const UNITS = ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22', 'ch23', 'ch24', 'ch25'];

router.get('/', authenticateToken, (req, res) => {
    const userId = req.user.userId;
    
    db.all(
        'SELECT unit_id, status, completed_at FROM user_progress WHERE user_id = ?',
        [userId],
        (err, rows) => {
            if (err) {
                return res.status(500).json({ success: false, message: '获取进度失败' });
            }
            
            const progressMap = {};
            rows.forEach(row => {
                progressMap[row.unit_id] = {
                    status: row.status,
                    completed_at: row.completed_at
                };
            });
            
            const units = UNITS.map(unitId => ({
                unit_id: unitId,
                status: progressMap[unitId]?.status || 'not_started',
                completed_at: progressMap[unitId]?.completed_at || null
            }));
            
            const completedCount = rows.filter(r => r.status === 'completed').length;
            
            res.json({
                success: true,
                units,
                stats: {
                    total: UNITS.length,
                    completed: completedCount,
                    in_progress: rows.filter(r => r.status === 'in_progress').length,
                    not_started: UNITS.length - completedCount - rows.filter(r => r.status === 'in_progress').length
                }
            });
        }
    );
});

router.put('/:unitId', authenticateToken, (req, res) => {
    const userId = req.user.userId;
    const { unitId } = req.params;
    const { status } = req.body;
    
    if (!UNITS.includes(unitId)) {
        return res.status(400).json({ success: false, message: '无效的单元ID' });
    }
    
    if (!['not_started', 'in_progress', 'completed'].includes(status)) {
        return res.status(400).json({ success: false, message: '无效的状态' });
    }
    
    const completedAt = status === 'completed' ? 'CURRENT_TIMESTAMP' : 'NULL';
    
    db.run(
        `INSERT INTO user_progress (user_id, unit_id, status, completed_at) 
         VALUES (?, ?, ?, ${completedAt})
         ON CONFLICT(user_id, unit_id) 
         DO UPDATE SET status = ?, completed_at = ${completedAt}`,
        [userId, unitId, status, status],
        function(err) {
            if (err) {
                return res.status(500).json({ success: false, message: '更新进度失败' });
            }
            res.json({ success: true, message: '进度已更新' });
        }
    );
});

router.get('/stats', authenticateToken, (req, res) => {
    const userId = req.user.userId;
    
    db.get(
        `SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'not_started' THEN 1 ELSE 0 END) as not_started
         FROM user_progress WHERE user_id = ?`,
        [userId],
        (err, row) => {
            if (err) {
                return res.status(500).json({ success: false, message: '获取统计失败' });
            }
            
            const total = UNITS.length;
            const completed = row.completed || 0;
            
            res.json({
                success: true,
                stats: {
                    total,
                    completed,
                    in_progress: row.in_progress || 0,
                    not_started: total - completed,
                    percentage: Math.round((completed / total) * 100)
                }
            });
        }
    );
});

module.exports = router;
