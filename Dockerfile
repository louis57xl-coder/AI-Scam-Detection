# Use Python 3.12 slim image for smaller footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install minimal system dependencies first (better layer caching)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
# This layer is cached separately from code changes
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scamcheck.py .

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Command to run the script
CMD ["python", "-u", "scamcheck.py"]
Key improvements in v2.01:

Better layer caching: Dependencies are installed before copying the main application code

Reduced image size:

Added --no-install-recommends to apt-get

Combined pip commands to reduce layers

Security enhancements:

Added non-root user execution

Set Python environment variables for better security/performance

Performance optimizations:

PYTHONUNBUFFERED=1 ensures unbuffered output (replaces -u flag in CMD)

PYTHONDONTWRITEBYTECODE=1 prevents .pyc files

Optional additions if needed:

If you need CUDA support, replace the first line with:

dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04
If disk space is critical, you could also add cleanup after build-essential:

dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*
This version provides better caching, smaller image size, and improved security while maintaining functionality.