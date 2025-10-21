# Runtime: Python 3.11 slim for small image size
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies only if needed (kept minimal; wheels should cover most)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (better caching)
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source
COPY backend/ /app/

# Expose default port (Railway sets PORT env)
EXPOSE 8000

# Start the app
CMD ["bash", "-lc", "exec gunicorn -w 1 -b 0.0.0.0:${PORT:-8000} app:app"]
