#!/bin/bash
set -e
echo "==> Initializing Prisma schema..."
prisma db push --schema ./db/prisma/schema.prisma
prisma db execute --file ./db/prisma/create_auto_increment.sql --schema ./db/prisma/schema.prisma
prisma db pull --schema ./db/prisma/schema.prisma