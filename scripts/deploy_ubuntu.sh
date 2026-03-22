#!/bin/bash
# PhysicsHub 完整部署脚本 - 腾讯云 Ubuntu
# 在服务器上以 root 或 sudo 用户运行

set -e

SERVER_IP=$(curl -s ip.sb 2>/dev/null || echo "YOUR_SERVER_IP")

echo "=========================================="
echo "  PhysicsHub 部署脚本"
echo "  服务器IP: $SERVER_IP"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 系统更新
echo -e "${YELLOW}[1/8] 更新系统...${NC}"
apt-get update -y
apt-get upgrade -y

# 2. 安装Nginx
echo -e "${YELLOW}[2/8] 安装 Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    apt-get install -y nginx
    systemctl enable nginx
fi

# 3. 创建网站目录
echo -e "${YELLOW}[3/8] 创建网站目录...${NC}"
PHYSICS_DIR="/var/www/physicshub"
mkdir -p $PHYSICS_DIR

# 4. 等待用户上传文件
echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}  请上传 PhysicsHub 文件到服务器${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "在本地电脑运行以下命令上传文件:"
echo ""
echo "  cd ~/Desktop"
echo "  tar -czf physicshub.tar.gz PhysicsHub/"
echo "  scp physicshub.tar.gz root@$SERVER_IP:/tmp/"
echo ""
echo "上传完成后，在服务器运行:"
echo "  cd /tmp && tar -xzf physicshub.tar.gz"
echo ""

read -p "按回车键确认已上传文件并继续..."

# 5. 移动文件
echo -e "${YELLOW}[4/8] 部署网站文件...${NC}"
if [ -d "/tmp/PhysicsHub" ]; then
    rm -rf $PHYSICS_DIR/*
    cp -r /tmp/PhysicsHub/* $PHYSICS_DIR/
    chown -R www-data:www-data $PHYSICS_DIR
    chmod -R 755 $PHYSICS_DIR
    echo "✅ 文件已复制到 $PHYSICS_DIR"
else
    echo "⚠️  未找到 /tmp/PhysicsHub，跳过文件复制"
fi

# 6. 配置Nginx
echo -e "${YELLOW}[5/8] 配置 Nginx...${NC}"
cat > /etc/nginx/sites-available/physicshub << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    server_name _;
    root /var/www/physicshub;
    index index.html;
    
    # 日志
    access_log /var/log/nginx/physicshub.access.log;
    error_log /var/log/nginx/physicshub.error.log;
    
    # Gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # 缓存静态资源
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # 主页
    location = / {
        try_files /index.html =404;
    }
    
    # 所有请求
    location / {
        try_files $uri $uri/ =404;
    }
    
    # 禁止访问敏感文件
    location ~ /\. {
        deny all;
    }
    
    location ~ ^/(scripts|config)/ {
        deny all;
    }
}
EOF

# 启用配置
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/physicshub /etc/nginx/sites-enabled/

# 7. 配置防火墙
echo -e "${YELLOW}[6/8] 配置防火墙...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
    echo "✅ UFW防火墙已配置"
fi

# 8. 测试并重载Nginx
echo -e "${YELLOW}[7/8] 测试 Nginx 配置...${NC}"
nginx -t

echo -e "${YELLOW}[8/8] 启动 Nginx...${NC}"
systemctl restart nginx
systemctl status nginx --no-pager

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}  ✅ PhysicsHub 部署成功！${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "🌐 访问地址:"
echo "   http://$SERVER_IP"
echo ""
echo "📁 网站目录: $PHYSICS_DIR"
echo "📜 访问日志: /var/log/nginx/physicshub.access.log"
echo "❌ 错误日志: /var/log/nginx/physicshub.error.log"
echo ""
echo "🔧 常用命令:"
echo "   重启Nginx:  sudo systemctl restart nginx"
echo "   查看状态:  sudo systemctl status nginx"
echo "   测试配置:  sudo nginx -t"
echo ""
echo -e "${YELLOW}提示: 如果无法访问，请检查腾讯云安全组是否放行80端口${NC}"
