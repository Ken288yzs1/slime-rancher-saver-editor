FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
# 内存字典存储, 必须单worker(-w 1), 否则上传/下载可能落到不同进程
CMD ["gunicorn", "-w", "1", "-t", "120", "-b", "0.0.0.0:7860", "app:app"]
