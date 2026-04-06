#!/usr/bin/env python3
import os
import subprocess
import sys

# Attempt database migrations (non-blocking)
print("Running database migrations...")
try:
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        timeout=30
    )
except Exception as e:
    print(f"Migration skipped: {e}")

# Start server
port = os.environ.get("PORT", "8000")
print(f"Starting FastAPI server on port {port}")

subprocess.call([
    sys.executable, "-m", "uvicorn",
    "server:app",
    "--host", "0.0.0.0",
    "--port", port,
    "--workers", "1"
])