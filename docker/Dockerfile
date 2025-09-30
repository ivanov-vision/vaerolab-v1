###################
# BUILDER STAGE
###################
FROM public.ecr.aws/docker/library/python:3.13.6-alpine3.22 AS builder

WORKDIR /app

# Install build deps (only for building wheels)
RUN apk add --no-cache build-base

# Install Python deps into a local folder
COPY app/requirements.txt .
RUN pip install --upgrade pip --no-cache-dir \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt

###################
# RUNTIME STAGE
###################
FROM public.ecr.aws/docker/library/python:3.13.6-alpine3.22 AS runtime

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appgroup app/app.py .

# Switch to non-root user
USER appuser

# Expose port for Prometheus scraping
EXPOSE 8000

# Healthcheck (scrapes /metrics)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -qO- http://localhost:8000/metrics || exit 1

# Run the service
CMD ["python", "app.py"]
