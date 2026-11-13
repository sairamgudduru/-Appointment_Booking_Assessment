from datetime import datetime, timezone
import pytest
from appointment_booking import AppointmentBookingService

@pytest.fixture
def service():
    return AppointmentBookingService()

@pytest.fixture
def at():
    return lambda hour, minute=0: datetime(2026, 1, 1, hour, minute, tzinfo=timezone.utc)
