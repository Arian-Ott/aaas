# ────────🔧 Base Builder Stage ────────
FROM python:3.12-slim AS builder

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for mysqlclient and builds
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create working dir
WORKDIR /usr/src/app

# Install Poetry (optional) or pip
COPY requirements.prod.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ────────📦 Final Runtime Stage ────────
FROM python:3.12-slim AS final

# Add runtime-only packages
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory


# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project code
COPY ./api .
COPY .env .

# Expose port
EXPOSE 5000

# Entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]