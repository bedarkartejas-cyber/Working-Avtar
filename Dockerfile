# Use the full Python image instead of slim to ensure all build tools are available
FROM python:3.11

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for compiling heavy libraries like 'av' and 'numpy'
# Added libav and ffmpeg development headers specifically for LiveKit agent audio/video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libavdevice-dev \
    libavfilter-dev \
    libavcodec-dev \
    libavformat-dev \
    libswresample-dev \
    libswscale-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary code
COPY app ./app

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Default command for the agent
CMD ["python", "-m", "app.main"]
