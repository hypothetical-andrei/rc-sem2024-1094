# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install development tools (optional)
RUN pip install --no-cache-dir watchdog ipython

# Expose any necessary ports (e.g., Flask or FastAPI)
EXPOSE 8000
