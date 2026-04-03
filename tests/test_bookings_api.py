"""Booking API critical flow tests: create, persistence, and sheet sync status behavior."""

import os
import uuid

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL").rstrip("/")


@pytest.fixture(scope="module")
def api_client():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


@pytest.fixture(scope="module")
def booking_payload():
    suffix = uuid.uuid4().hex[:8]
    return {
        "patient_name": f"TEST_BOOKING_{suffix}",
        "phone": "9876543210",
        "service": "Acne Control Treatment",
        "preferred_date": "2026-03-25",
        "preferred_time": "10:30",
        "message": "TEST booking flow validation",
    }


@pytest.fixture(scope="module")
def created_booking(api_client, booking_payload):
    response = api_client.post(f"{BASE_URL}/api/bookings", json=booking_payload, timeout=20)
    assert response.status_code == 200, f"Create booking failed: {response.status_code} {response.text}"
    return response.json()


def test_create_booking_returns_expected_structure(created_booking, booking_payload):
    assert isinstance(created_booking.get("id"), str)
    assert created_booking["patient_name"] == booking_payload["patient_name"]
    assert created_booking["phone"] == booking_payload["phone"]
    assert created_booking["service"] == booking_payload["service"]
    assert created_booking["preferred_date"] == booking_payload["preferred_date"]
    assert created_booking["preferred_time"] == booking_payload["preferred_time"]
    assert created_booking["message"] == booking_payload["message"]


def test_booking_status_defaults_to_pending(created_booking):
    assert created_booking["status"] == "Pending"


def test_sheet_sync_status_graceful_when_webhook_missing(created_booking):
    assert created_booking["sheet_sync_status"] == "not_configured"


def test_created_booking_persisted_and_retrievable(api_client, created_booking):
    response = api_client.get(f"{BASE_URL}/api/bookings", timeout=20)
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)

    matched = next((item for item in bookings if item.get("id") == created_booking["id"]), None)
    assert matched is not None
    assert matched["patient_name"] == created_booking["patient_name"]
    assert matched["status"] == "Pending"


def test_invalid_phone_rejected(api_client):
    bad_payload = {
        "patient_name": "TEST_BOOKING_BAD_PHONE",
        "phone": "12345",
        "service": "Acne Control Treatment",
        "preferred_date": "2026-03-25",
        "preferred_time": "10:30",
        "message": "invalid phone case",
    }
    response = api_client.post(f"{BASE_URL}/api/bookings", json=bad_payload, timeout=20)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Phone number looks invalid"
