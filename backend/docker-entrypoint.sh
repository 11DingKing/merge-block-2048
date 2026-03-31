#!/bin/bash
set -e

# 等待 MySQL 就绪
echo "Waiting for MySQL..."
while ! python -c "import MySQLdb; MySQLdb.connect(host='db', user='game2048', passwd='game2048pass', db='game2048')" 2>/dev/null; do
    sleep 1
done
echo "MySQL is ready!"

# 运行数据库迁移
python manage.py migrate --noinput

# 启动服务器
exec python manage.py runserver 0.0.0.0:8000
