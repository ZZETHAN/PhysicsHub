# PhysicsHub Backend Dockerfile
FROM node:18-alpine

WORKDIR /app

# 复制 package.json
COPY package.json ./

# 安装依赖
RUN npm install --production

# 复制代码
COPY . .

# 暴露端口
EXPOSE 3001

# 启动命令
CMD ["node", "server.js"]
