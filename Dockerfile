# ============================================================
# New-mir — Neural Code Engine
# Multi-stage Dockerfile
# Works on any Linux x86_64 / arm64 machine, even weak hardware.
# ============================================================

# ---- Stage 1: dependency builder ----
FROM python:3.11-slim AS builder

WORKDIR /app

# System libs required for lz4, zstd, Pillow, qrcode
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        gcc g++ libffi-dev libssl-dev zlib1g-dev liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip --quiet \
 && pip install --prefix=/install --quiet -r requirements.txt

# ---- Stage 2: runtime image ----
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="New-mir Neural Code Engine" \
      org.opencontainers.image.description="Honeycomb-memory transformer for code generation. Runs offline on any Linux PC." \
      org.opencontainers.image.version="1.1.0"

# Minimal runtime libs
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy source
COPY core/     core/
COPY api/      api/
COPY web/      web/
COPY main.py   main.py

# Non-root user for safety
RUN useradd -m -u 1000 newmir && chown -R newmir /app
USER newmir

# Expose web port
EXPOSE 8000

# Health check — verifies the API is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" \
  || exit 1

# Throttle workers: max 4, uses min(cpu_count, 4)
ENV NEW_MIR_HOST=0.0.0.0
ENV NEW_MIR_PORT=8000
ENV NEW_MIR_LOG_LEVEL=info

ENTRYPOINT ["python", "main.py"]
