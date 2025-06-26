# Stage 1: Builder - Install dependencies and build wheels
FROM python:3.11-slim as builder

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VENV_IN_PROJECT=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  POETRY_HOME="/opt/poetry" \
  POETRY_VERSION=1.7.1

# Install system dependencies needed for building
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Set work directory
WORKDIR /app

# Copy poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies and create wheels
RUN poetry config virtualenvs.create false \
  && poetry install --only=main --no-root \
  && rm -rf $POETRY_CACHE_DIR

# Stage 2: Production - Create final lightweight image
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive

# Install only runtime dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  libpq5 \
  postgresql-client \
  gettext \
  curl \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get purge -y --auto-remove

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Set work directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy project files
COPY . /app/

# Copy and setup entrypoint script
COPY ./scripts/entry.sh /app/entry.sh
RUN chmod +x /app/entry.sh && \
  sed -i 's/\r$//' /app/entry.sh

# Create necessary directories and set permissions
RUN mkdir -p /app/staticfiles /app/media /app/logs \
  && chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
