const fs = require('fs');
const path = require('path');

// 自动配置 API 地址
const API_URLS = {
    local: 'http://localhost:3001/api',
    production: 'http://123.207.75.145:3001/api'
};

function detectEnvironment() {
    // 检查是否在本地开发
    const isLocal = process.env.NODE_ENV !== 'production' && 
                    fs.existsSync(path.join(__dirname, 'api', 'database.db'));
    
    return isLocal ? 'local' : 'production';
}

function updateApiUrl() {
    const env = detectEnvironment();
    const apiUrl = API_URLS[env];
    
    console.log(`🔧 环境检测: ${env}`);
    console.log(`🔧 API地址: ${apiUrl}`);
    
    // 更新 auth.js
    const authJsPath = path.join(__dirname, 'auth', 'auth.js');
    if (fs.existsSync(authJsPath)) {
        let content = fs.readFileSync(authJsPath, 'utf8');
        content = content.replace(
            /const API_BASE_URL = ['"].*?['"];/,
            `const API_BASE_URL = '${apiUrl}';`
        );
        fs.writeFileSync(authJsPath, content);
        console.log('✅ auth.js 已更新');
    }
    
    // 更新 admin.html
    const adminHtmlPath = path.join(__dirname, 'admin.html');
    if (fs.existsSync(adminHtmlPath)) {
        let content = fs.readFileSync(adminHtmlPath, 'utf8');
        content = content.replace(
            /window\.API_BASE_URL = ['"].*?['"];/,
            `window.API_BASE_URL = '${apiUrl}';`
        );
        fs.writeFileSync(adminHtmlPath, content);
        console.log('✅ admin.html 已更新');
    }
}

// 如果直接运行此脚本
if (require.main === module) {
    updateApiUrl();
}

module.exports = { detectEnvironment, updateApiUrl };
