# 使用官方 Node.js 镜像
FROM node:18-slim

# 设置工作目录
WORKDIR /app

# 将 package.json 和 package-lock.json 复制到容器中
COPY package*.json ./

# 安装依赖项
RUN npm install

# 复制 React 应用的代码到容器中
COPY . .

# 构建 React 应用
RUN npm run build

# 使用 Nginx 作为生产环境的 Web 服务器
FROM nginx:stable-alpine
COPY --from=0 /app/build /usr/share/nginx/html

# 暴露 Nginx 默认的 Web 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]