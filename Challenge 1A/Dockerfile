# Use official Python image for AMD64
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY process_pdf.py .

# Create input/output directories (matching hackathon specs)
RUN mkdir -p /input /output

# Run the processor
CMD ["python", "process_pdf.py"]