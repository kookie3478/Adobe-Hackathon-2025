FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY run_all.py .

ENTRYPOINT ["python", "run_all.py"]