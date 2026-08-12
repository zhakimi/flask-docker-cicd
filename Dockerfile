# Production-style image: slim base, cached dependency layer, non-root user.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so this layer is cached until requirements change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Never run a service as root inside the container.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Container-level liveness probe hitting the app's own /health endpoint.
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
