#!/bin/bash
# PhysicsHub 服务器权限修复脚本
# 用途：修复部署后 www-data 权限问题，确保 auth 和 units 可访问
# 
# 根本原因：deploy_physicshub.sh 使用 cp -r 复制但没有 chown www-data
# 症状：auth/ 和 units/ 目录变成 drwx------ (700)，导致 404 和登录失效
#
# 使用方法：
#   ./fix_permissions.sh              # 修复权限
#   ./fix_permissions.sh --verify     # 修复并验证
#
# 建议：在 deploy_physicshub.sh 末尾添加对此脚本的调用

set -e

SERVER="ubuntu@123.207.75.145"
SERVER_PATH="/var/www/physicshub"
SSH_OPTS="-o StrictHostKeyChecking=no"

echo "🔧 PhysicsHub 权限修复"
echo "======================"

# 修复 auth 目录权限
echo "📁 修复 auth 目录..."
sshpass -p '@0430zYH' ssh $SSH_OPTS $SERVER << 'ENDSSH'
sudo chmod 755 /var/www/physicshub/auth/
sudo chmod 644 /var/www/physicshub/auth/auth.js
sudo chmod 644 /var/www/physicshub/auth/auth.css
sudo chown -R www-data:www-data /var/www/physicshub/auth/
ENDSSH
echo "   ✅ auth 目录已修复"

# 修复 units 目录权限
echo "📁 修复 units 目录..."
sshpass -p '@0430zYH' ssh $SSH_OPTS $SERVER << 'ENDSSH'
sudo chmod 755 /var/www/physicshub/
sudo chmod 755 /var/www/physicshub/units/
sudo chown -R www-data:www-data /var/www/physicshub/units/
sudo find /var/www/physicshub/units/ -type d -exec chmod 755 {} \;
sudo find /var/www/physicshub/units/ -type f -exec chmod 644 {} \;
ENDSSH
echo "   ✅ units 目录已修复"

# 修复所有 HTML 和 JS/CSS 文件
echo "📁 修复全局权限..."
sshpass -p '@0430zYH' ssh $SSH_OPTS $SERVER << 'ENDSSH'
sudo chown -R www-data:www-data /var/www/physicshub/
sudo find /var/www/physicshub/ -type f -name '*.html' -exec chmod 644 {} \;
sudo find /var/www/physicshub/ -type f -name '*.js' ! -path '*/node_modules/*' -exec chmod 644 {} \;
sudo find /var/www/physicshub/ -type f -name '*.css' -exec chmod 644 {} \;
sudo find /var/www/physicshub/ -type d -exec chmod 755 {} \;
ENDSSH
echo "   ✅ 全局权限已修复"

if [ "$1" = "--verify" ] || [ "$1" = "-v" ]; then
    echo ""
    echo "🔍 验证修复..."
    sshpass -p '@0430zYH' ssh $SSH_OPTS $SERVER << 'ENDSSH'
echo "auth 目录:"
ls -la /var/www/physicshub/auth/
echo ""
echo "units 目录 (前5个):"
ls /var/www/physicshub/units/ | head -5
echo ""
echo "index.html 权限:"
ls -la /var/www/physicshub/index.html
ENDSSH
    echo "   ✅ 验证完成"
fi

echo ""
echo "✅ 权限修复完成！"
