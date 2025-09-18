# Base image pinned to Debian Bookworm (stable)
FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install only what’s needed for parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libmagic1 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies (CPU-only)
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the project (not venv, not data dumps)
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]

