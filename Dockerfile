FROM python:3.12.1-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ backend/
COPY scripts/ scripts/
COPY dataset/ dataset/

# Create data directory for ChromaDB
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_DIR=/app/data

# Build the search index during image build
RUN python scripts/build_index.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 