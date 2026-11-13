from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class AppointmentStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Appointment:
    appointment_id: str
    provider_id: str
    start_utc: datetime
    end_utc: datetime
    status: AppointmentStatus = AppointmentStatus.ACTIVE

@dataclass(frozen=True)
class BookingResult:
    success: bool
    code: str
    message: str
    appointment: Optional[Appointment] = None
