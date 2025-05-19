#!/bin/bash

set -e

echo "==> Initializing Prisma schema..."

cd /app/src/deeprag
echo "==> Changed to directory: $(pwd)"

# 确保应用程序的幂等性
# 标志文件的路径
INIT_FLAG_FILE=".prisma_initialized"

# 第一次初始化时才执行以下操作
if [ ! -f "$INIT_FLAG_FILE" ]; then
    echo "==> First time setup: pushing schema to database"
    poetry run prisma db push --schema ./db/prisma/schema.prisma
    echo "==> Prisma schema pushed successfully"

    sleep 2

    echo "==> Running SQL to create auto-increment"
    poetry run prisma db execute --file ./db/prisma/create_auto_increment.sql --schema ./db/prisma/schema.prisma
    echo "==> Auto-increment SQL executed successfully"

    sleep 2

    echo "==> Pulling schema from database"
    poetry run prisma db pull --schema ./db/prisma/schema.prisma
    echo "==> Prisma schema pulled successfully"

    # 创建标志文件，防止重复初始化
    touch "$INIT_FLAG_FILE"
    echo "==> Initialization complete, flag file created"
    poetry run prisma generate --schema ./db/prisma/schema.prisma
else
    echo "==> Prisma schema already initialized. Skipping setup."
    
fi

echo "==> Prisma generate executed" 
echo "==> Starting application with uvicorn..."
exec poetry run uvicorn deeprag.api.main:app --host 0.0.0.0 --port 8000
