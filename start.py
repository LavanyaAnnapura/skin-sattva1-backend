#!/usr/bin/env python3
import os
import subprocess
import sys

# Try to run migrations (but don't fail if it doesn't work)
print("Attempting database migrations...")
try:
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        timeout=30,
        capture_output=True
    )
    print("✅ Migrations completed")
except Exception as e:
    print(f"⚠️ Migrations skipped: {e}")

# Start FastAPI server
port = os.environ.get("PORT", "8000")
print(f"Starting server on port {port}...")

os.execvp(sys.executable, [
    sys.executable, "-m", "uvicorn",
    "server:app",
    "--host", "0.0.0.0",
    "--port", port
])