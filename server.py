from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import httpx
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Booking

load_dotenv(Path(__file__).parent / '.env')

app = FastAPI(title="Skin Sattva API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SHEETS_WEBHOOK_URL = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL", "")


class BookingRequest(BaseModel):
    patient_name: str
    phone: str
    service: str
    preferred_date: str
    preferred_time: str
    message: Optional[str] = ""


class BookingResponse(BaseModel):
    id: str
    patient_name: str
    phone: str
    service: str
    preferred_date: str
    preferred_time: str
    message: str
    status: str
    created_at: str
    sheet_sync_status: str


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Skin Sattva API"}


@app.post("/api/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingRequest, db: AsyncSession = Depends(get_db)):
    new_booking = Booking(
        patient_name=booking.patient_name,
        phone=booking.phone,
        service=booking.service,
        preferred_date=booking.preferred_date,
        preferred_time=booking.preferred_time,
        message=booking.message or "",
        status="Pending",
        created_at=datetime.now(timezone.utc),
        sheet_sync_status="not_configured",
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    # Sync to Google Sheets
    if GOOGLE_SHEETS_WEBHOOK_URL:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                payload = {
                    "patient_name": new_booking.patient_name,
                    "phone": new_booking.phone,
                    "service": new_booking.service,
                    "preferred_date": new_booking.preferred_date,
                    "preferred_time": new_booking.preferred_time,
                    "message": new_booking.message,
                }
                response = await client.post(GOOGLE_SHEETS_WEBHOOK_URL, json=payload, follow_redirects=True)
                if response.status_code == 200:
                    new_booking.sheet_sync_status = "synced"
                else:
                    new_booking.sheet_sync_status = "sync_failed"
        except Exception:
            new_booking.sheet_sync_status = "sync_failed"

        await db.commit()
        await db.refresh(new_booking)

    return BookingResponse(
        id=new_booking.id,
        patient_name=new_booking.patient_name,
        phone=new_booking.phone,
        service=new_booking.service,
        preferred_date=new_booking.preferred_date,
        preferred_time=new_booking.preferred_time,
        message=new_booking.message or "",
        status=new_booking.status,
        created_at=new_booking.created_at.isoformat() if new_booking.created_at else "",
        sheet_sync_status=new_booking.sheet_sync_status,
    )


@app.get("/api/bookings")
async def get_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking).order_by(Booking.created_at.desc()))
    bookings = result.scalars().all()
    return [
        BookingResponse(
            id=b.id,
            patient_name=b.patient_name,
            phone=b.phone,
            service=b.service,
            preferred_date=b.preferred_date,
            preferred_time=b.preferred_time,
            message=b.message or "",
            status=b.status,
            created_at=b.created_at.isoformat() if b.created_at else "",
            sheet_sync_status=b.sheet_sync_status,
        )
        for b in bookings
    ]
