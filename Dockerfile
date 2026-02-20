# Lightweight base image
FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr (better logs)
ENV PYTHONUNBUFFERED=1

# HF Spaces uses PORT (often 7860). We'll respect it.
ENV PORT=7860

WORKDIR /app

# System deps (add more only if you need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the app
COPY . /app

# Expose the port HF will route to
EXPOSE 7860

# IMPORTANT:
# Replace "app:app" with your server entry:
# - FastAPI: "main:app" or "app.main:app"
# - Flask: "app:app"
# Also: ensure it binds 0.0.0.0 and uses $PORT
CMD ["bash", "-lc", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]