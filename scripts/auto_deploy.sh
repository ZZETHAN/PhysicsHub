#!/bin/bash
# PhysicsHub 一键自动部署脚本
# 使用方法: 上传此脚本到服务器，运行: sudo bash auto_deploy.sh

set -e

echo "=========================================="
echo "  PhysicsHub 自动部署"
echo "=========================================="

# 获取服务器IP
SERVER_IP=$(curl -s ip.sb 2>/dev/null || hostname -I | awk '{print $1}')
echo "服务器IP: $SERVER_IP"
echo ""

# 检查root权限
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 sudo 运行: sudo bash auto_deploy.sh"
    exit 1
fi

# 1. 安装必要软件
echo "[1/6] 安装 Nginx..."
apt-get update -qq
apt-get install -y -qq nginx curl

# 2. 创建网站目录
echo "[2/6] 创建网站目录..."
mkdir -p /var/www/physicshub

# 3. 下载网站文件
echo "[3/6] 准备下载网站文件..."
echo ""
echo "⚠️  请确保已将 physicshub.tar.gz 上传到 /tmp/ 目录"
echo ""

if [ -f "/tmp/physicshub.tar.gz" ]; then
    echo "✅ 找到网站文件，正在解压..."
    cd /tmp
    tar -xzf physicshub.tar.gz
    cp -r PhysicsHub/* /var/www/physicshub/
    echo "✅ 文件已部署"
elif [ -d "/tmp/PhysicsHub" ]; then
    echo "✅ 找到网站文件夹，正在复制..."
    cp -r /tmp/PhysicsHub/* /var/www/physicshub/
    echo "✅ 文件已部署"
else
    echo "❌ 未找到网站文件！"
    echo ""
    echo "请先上传文件到服务器:"
    echo "  scp ~/Desktop/physicshub.tar.gz root@$SERVER_IP:/tmp/"
    echo ""
    exit 1
fi

# 4. 设置权限
echo "[4/6] 设置文件权限..."
chown -R www-data:www-data /var/www/physicshub
chmod -R 755 /var/www/physicshub

# 5. 配置Nginx
echo "[5/6] 配置 Nginx..."
cat > /etc/nginx/sites-available/physicshub << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    root /var/www/physicshub;
    index index.html;
    
    access_log /var/log/nginx/physicshub.access.log;
    error_log /var/log/nginx/physicshub.error.log;
    
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf)$ {
        expires 30d;
        add_header Cache-Control "public";
    }
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location ~ /\. {
        deny all;
    }
}
EOF

# 启用配置
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/physicshub /etc/nginx/sites-enabled/

# 6. 启动服务
echo "[6/6] 启动 Nginx..."
systemctl restart nginx
systemctl enable nginx

# 配置防火墙
ufw allow 80/tcp 2>/dev/null || true
ufw allow 443/tcp 2>/dev/null || true

echo ""
echo "=========================================="
echo "  ✅ 部署完成！"
echo "=========================================="
echo ""
echo "🌐 网站地址: http://$SERVER_IP"
echo ""
echo "📁 网站目录: /var/www/physicshub"
echo ""
echo "⚠️  重要提示:"
echo "   请在腾讯云控制台 > 安全组/防火墙"
echo "   添加规则: TCP 80 端口允许所有IP访问"
echo ""
