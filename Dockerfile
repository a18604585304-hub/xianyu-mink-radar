FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY scripts ./scripts
COPY config ./config
RUN mkdir -p /data /app/data /app/logs
ENV PYTHONUNBUFFERED=1 TZ=Asia/Shanghai
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
