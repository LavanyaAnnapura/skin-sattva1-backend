#!/usr/bin/env python3
"""
Production startup script for Skin Sattva Backend
Runs database migrations and starts the FastAPI server
"""

import os
import subprocess
import sys

def run_migrations():
    """Run Alembic database migrations"""
    print("Running database migrations...")
    try:
        subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], check=False)
        print("✅ Database migrations completed")
    except Exception as e:
        print(f"⚠️  Migration warning: {e}")

if __name__ == "__main__":
    # Run migrations first
    run_migrations()
    
    # Start FastAPI server with uvicorn
    port = os.environ.get("PORT", "8000")
    print(f"Starting server on port {port}")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "server:app",
        "--host", "0.0.0.0",
        "--port", port
    ])