FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 设置 Python 环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# # 安装 Nginx
# RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# # 复制 Nginx 配置文件
# COPY nginx.conf /etc/nginx/sites-available/default

# 暴露Nginx端口
# EXPOSE 80
# 暴露端口
EXPOSE 8000

# 启动 Gunicorn 和 Nginx
# CMD ["sh", "-c", "gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"]  
# 普通启动 
# CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000"]