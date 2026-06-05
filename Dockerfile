FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    nodejs npm curl git ca-certificates --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g opencode-ai && npm cache clean --force

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
WORKDIR /app

RUN mkdir -p /root/.local/share/opencode && echo '{}' > /root/.local/share/opencode/auth.json

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
