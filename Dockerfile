# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (libpcap for Scapy)
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run as non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Entry point
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
