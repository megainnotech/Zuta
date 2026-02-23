# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Install system dependencies including Node.js and Chromium for Mermaid CLI
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    chromium \
    fonts-liberation \
    libnss3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI globally
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
RUN npm install -g @mermaid-js/mermaid-cli

# Create working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src /app/src

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command
CMD ["python", "src/main.py", "--topic", "High TPS API Service"]
