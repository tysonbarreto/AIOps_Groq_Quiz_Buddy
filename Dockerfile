ARG PYTHON_BASE=3.12-slim
FROM python:$PYTHON_BASE AS compiler

WORKDIR /app

COPY pyproject.toml uv.lock README.md /app/

RUN python -m pip install --break-system-packages -U uv && \
    uv venv --python 3.12

ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync

FROM python:$PYTHON_BASE AS runner

WORKDIR /app

COPY --from=compiler /app/.venv/ /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src
COPY app.py /app/

EXPOSE 8501

CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0","--server.headless=true"]

