#!/usr/bin/env python3
"""
Production startup script for Skin Sattva Backend
Runs database migrations and starts the FastAPI server
"""

import os
import subprocess
import sys
from pathlib import Path

def run_migrations():
    """Run Alembic database migrations"""
    print("Running database migrations...")
    try:
        # Run alembic upgrade head
        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        if result.returncode == 0:
            print("✅ Database migrations completed successfully")
        else:
            print(f"⚠️  Migration output: {result.stdout}")
            print(f"⚠️  Migration errors: {result.stderr}")
            # Don't fail if migrations fail - database might already be up to date

    except Exception as e:
        print(f"⚠️  Migration error: {e}")
        # Continue anyway - database might already be set up

def start_server():
    """Start the FastAPI server"""
    print("Starting FastAPI server...")
    port = os.environ.get("PORT", "8000")
    print(f"Server will run on port {port}")

    # Use uvicorn to run the server
    os.execvp("uvicorn", [
        "uvicorn",
        "server:app",
        "--host", "0.0.0.0",
        "--port", port,
        "--workers", "1",  # Start with 1 worker, can scale later
        "--loop", "uvloop" if os.name != "nt" else "asyncio"  # Use uvloop on Unix, asyncio on Windows
    ])

if __name__ == "__main__":
    run_migrations()
    start_server()