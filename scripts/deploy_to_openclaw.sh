#!/bin/bash
# PhysicsHub 部署脚本 - 腾讯云 OpenClaw 镜像
# 运行前请确保已SSH登录到服务器

set -e

echo "🚀 开始部署 PhysicsHub 到 OpenClaw 服务器..."

# 1. 检查是否以root运行
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

# 2. 创建网站目录
PHYSICS_DIR="/var/www/physicshub"
echo "📁 创建网站目录: $PHYSICS_DIR"
mkdir -p $PHYSICS_DIR

# 3. 提示用户上传文件
echo ""
echo "📤 请先将 PhysicsHub 文件夹上传到服务器:"
echo "   本地运行: scp -r ~/Desktop/PhysicsHub root@你的服务器IP:/tmp/"
echo ""
echo "   上传完成后，按回车继续..."
read

# 4. 移动文件到Web目录
if [ -d "/tmp/PhysicsHub" ]; then
    echo "📂 移动文件到网站目录..."
    cp -r /tmp/PhysicsHub/* $PHYSICS_DIR/
    chown -R www-data:www-data $PHYSICS_DIR
    chmod -R 755 $PHYSICS_DIR
else
    echo "❌ 未找到 /tmp/PhysicsHub 文件夹"
    exit 1
fi

# 5. 检查Nginx配置
if ! command -v nginx &> /dev/null; then
    echo "📦 安装 Nginx..."
    apt-get update
    apt-get install -y nginx
fi

# 6. 创建Nginx配置文件
echo "⚙️  配置 Nginx..."
cat > /etc/nginx/sites-available/physicshub << 'EOF'
server {
    listen 80;
    server_name _;  # 接受所有域名/IP访问
    
    # PhysicsHub 网站根目录
    root /var/www/physicshub;
    index index.html;
    
    # 日志
    access_log /var/log/nginx/physicshub_access.log;
    error_log /var/log/nginx/physicshub_error.log;
    
    # 静态文件缓存
    location ~* \.(html|css|js|png|jpg|jpeg|gif|ico|svg|pdf)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # 首页
    location = / {
        try_files /index.html =404;
    }
    
    # 所有路径
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
EOF

# 7. 启用配置
ln -sf /etc/nginx/sites-available/physicshub /etc/nginx/sites-enabled/

# 8. 检查OpenClaw配置是否冲突（保留OpenClaw）
if [ -f "/etc/nginx/sites-enabled/openclaw" ]; then
    echo "✅ 检测到 OpenClaw 配置，将保留其访问路径"
    echo "   - OpenClaw: http://你的服务器IP:8080 或原有端口"
    echo "   - PhysicsHub: http://你的服务器IP:80"
fi

# 9. 测试并重载Nginx
echo "🔄 测试 Nginx 配置..."
nginx -t

echo "🔄 重载 Nginx..."
systemctl reload nginx

# 10. 防火墙放行（如果有）
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
fi

# 11. 完成
echo ""
echo "✅ PhysicsHub 部署完成！"
echo ""
echo "📍 访问地址:"
echo "   - PhysicsHub: http://$(curl -s ip.sb 2>/dev/null || echo '你的服务器IP')"
echo ""
echo "🔧 管理命令:"
echo "   查看状态: systemctl status nginx"
echo "   重启Nginx: systemctl restart nginx"
echo "   网站目录: $PHYSICS_DIR"
echo ""

# 显示文件列表
echo "📋 已部署文件:"
ls -la $PHYSICS_DIR
