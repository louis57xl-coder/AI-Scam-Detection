# Use a lightweight Python image with built-in CUDA support if possible
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for some torch/transformers components)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scamcheck.py script into the container
COPY scamcheck.py .

# Command to run the script
# Use -u to ensure logs/print statements are unbuffered for real-time viewing
CMD ["python", "-u", "scamcheck.py"]