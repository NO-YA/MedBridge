#!/usr/bin/env sh
set -e

echo "Waiting for database to be ready..."
python -m app.wait_for_db

echo "Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
