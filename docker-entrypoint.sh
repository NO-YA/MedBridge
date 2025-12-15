#!/usr/bin/env bash
set -euo pipefail

# Simple entrypoint for the MedBridge container.
# - Waits for the database host/port to accept TCP connections
# - Runs create_tables.py to ensure tables exist (useful in dev)
# - Execs the CMD

echo "Starting docker-entrypoint.sh"

DB_URL=${DATABASE_URL:-}
if [ -z "$DB_URL" ]; then
  echo "WARNING: DATABASE_URL is not set. The app may fail to start." >&2
else
  # Extract host and port using python (robust parsing)
  read host port <<< $(python - <<PY
import os
from urllib.parse import urlparse
u = os.getenv('DATABASE_URL')
if not u:
    print('','')
else:
    p = urlparse(u)
    host = p.hostname or ''
    port = p.port or ''
    print(host, port)
PY
)

  if [ -n "$host" ] && [ -n "$port" ]; then
    echo "Waiting for DB $host:$port..."
    until python - <<PY
import socket,sys
sock=socket.socket()
try:
    sock.settimeout(1)
    sock.connect(("$host", int("$port")))
    print('ok')
except Exception as e:
    sys.exit(1)
finally:
    sock.close()
PY
    do
      sleep 1
    done
    echo "DB reachable"
  else
    echo "Could not parse host/port from DATABASE_URL (value: '$DB_URL')" >&2
  fi
fi

# Create tables (idempotent) - useful for dev. In production you may want alembic migrations.
if [ -f ./create_tables.py ]; then
  echo "Creating DB tables (if necessary)"
  python create_tables.py || true
fi

echo "Entrypoint finished, executing: $@"
exec "$@"
