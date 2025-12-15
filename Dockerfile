FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser

# Install build deps needed by some cryptography/bcrypt wheels if a prebuilt wheel
# is not available on the base image. We remove build deps after pip install to
# keep image size small.
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libssl-dev python3-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod +x ./docker-entrypoint.sh

EXPOSE 8000

USER appuser

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
