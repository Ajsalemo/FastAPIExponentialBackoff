#!/bin/sh

set -e 

echo "Starting SSH ..."
service ssh start

# Start FastAPI with uvicorn
exec uvicorn app:app --host 0.0.0.0 --port 8000