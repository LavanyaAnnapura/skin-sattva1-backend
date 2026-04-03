import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text
from database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    service = Column(String(255), nullable=False)
    preferred_date = Column(String(50), nullable=False)
    preferred_time = Column(String(50), nullable=False)
    message = Column(Text, default="")
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    sheet_sync_status = Column(String(20), default="not_configured")
