FROM --platform=linux/amd64 python:3.10-slim

# Avoid writing .pyc files and keep logs clean
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY app/ ./app/
COPY run_all.py .

# If using offline models
# COPY models/ ./models/
# ENV TRANSFORMERS_OFFLINE=1
# ENV HF_DATASETS_OFFLINE=1

ENTRYPOINT ["python", "run_all.py"]
