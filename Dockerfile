# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies and Node.js (needed for Reflex frontend build)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Initialize Reflex (this installs frontend dependencies)
RUN reflex init

# Export the frontend as static files
RUN reflex export --frontend-only --no-zip

# Expose the ports (8000 for backend API)
EXPOSE 8000

# Start the Reflex backend server
# We use --env prod to optimize for production
CMD ["reflex", "run", "--env", "prod", "--backend-only"]
