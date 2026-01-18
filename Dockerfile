FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies and supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libavdevice-dev \
    libavfilter-dev \
    libavcodec-dev \
    libavformat-dev \
    libswresample-dev \
    libswscale-dev \
    pkg-config \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Setup supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Use supervisord to start both processes
CMD ["/usr/bin/supervisord"]
