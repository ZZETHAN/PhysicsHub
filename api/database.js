const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, 'database.db');
const db = new sqlite3.Database(dbPath);

// 初始化数据库表
db.serialize(() => {
    // 用户表 - 添加 status 字段用于管理员审核
    db.run(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
            role TEXT DEFAULT 'student' CHECK(role IN ('student', 'admin')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            approved_at DATETIME,
            approved_by INTEGER,
            last_login DATETIME,
            avatar_color TEXT DEFAULT '#0891b2',
            avatar_icon TEXT DEFAULT '😊'
        )
    `);

    // 添加头像字段（如果表中已存在但列不存在）
    db.run(`ALTER TABLE users ADD COLUMN avatar_color TEXT DEFAULT '#0891b2'`, (err) => {
        if (err && !err.message.includes('duplicate column name')) {
            console.log('avatar_color column already exists or error:', err.message);
        }
    });
    db.run(`ALTER TABLE users ADD COLUMN avatar_icon TEXT DEFAULT '😊'`, (err) => {
        if (err && !err.message.includes('duplicate column name')) {
            console.log('avatar_icon column already exists or error:', err.message);
        }
    });

    // 用户学习进度表
    db.run(`
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            status TEXT DEFAULT 'not_started' CHECK(status IN ('not_started', 'in_progress', 'completed')),
            completed_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, unit_id)
        )
    `);

    // 创建默认管理员账号 (密码: admin123)
    // 注意：生产环境应该修改默认密码
    const bcrypt = require('bcryptjs');
    const adminPassword = bcrypt.hashSync('admin123', 10);
    
    db.run(`
        INSERT OR IGNORE INTO users (username, email, password_hash, status, role)
        VALUES ('admin', 'admin@physicshub.com', ?, 'approved', 'admin')
    `, [adminPassword]);

    console.log('✅ Database initialized');
});

module.exports = db;
