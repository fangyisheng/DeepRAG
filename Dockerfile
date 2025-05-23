FROM python:3.12


WORKDIR /app
RUN pip install poetry
#分阶段构建

COPY ./deeprag/pyproject.toml .
COPY ./deeprag/poetry.lock .
# # 安装编译依赖
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential gcc libffi-dev libssl-dev \
#     curl git pkg-config libgl1 libglib2.0-0 \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY ./deeprag/src ./src
# 使用poetry 安装依赖
RUN poetry install
RUN cd /app/src/deeprag && poetry run prisma generate --schema ./db/prisma/schema.prisma
COPY entrypoint.sh /app/src/deeprag/entrypoint.sh
RUN chmod +x /app/src/deeprag/entrypoint.sh
# RUN cd /app/src/deeprag && bash /app/src/deeprag/entrypoint.sh
#启动应用
# CMD ["poetry", "run", "uvicorn", "deeprag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]