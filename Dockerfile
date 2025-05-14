FROM acidrain/python-poetry:3.12-alpine-2.1.3

WORKDIR /app

#分阶段构建

COPY DeepRAG/deeprag/pyproject.toml .
COPY DeepRAG/deeprag/poetry.lock .
RUN poetry install

COPY DeepRAG/deeprag/src ./src

#启动应用
CMD ["poetry", "run", "uvicorn", "deeprag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]