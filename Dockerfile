# Use a slim Python base image
ARG PYTHON_VERSION=3.13-slim
FROM python:${PYTHON_VERSION} AS builder

# Set environment variables for security
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Use a dedicated directory and install dependencies securely
COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && pip install --upgrade pip \
    --no-cache-dir \
    --disable-pip-version-check \ 
    --default-timeout=100 \
    -r requirements.txt

COPY ./app ./app

# Stage 2: Build minimal runtime using Distroless
FROM python:${PYTHON_VERSION}

# Set working directory
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Set up a non-root user and group
RUN groupadd -r fastapi && useradd --no-log-init -r -g fastapi fastapi

# Copy application code
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app/ /app/
COPY --from=builder /usr/local/bin /usr/local/bin

# Change ownership to the non-root user and restrict permissions
RUN chown -R fastapi:fastapi /app && chmod -R 755 /app

# Switch to non-root user
USER fastapi

# Expose port 8080
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# Use a health check to ensure the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD curl -f http://localhost:8080/octocat || exit 1