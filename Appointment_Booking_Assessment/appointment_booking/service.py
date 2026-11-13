from datetime import datetime, timezone
from threading import RLock
from .models import Appointment, AppointmentStatus, BookingResult

class AppointmentBookingService:
    """In-memory booking service. All state operations are protected by one process-local lock."""

    def __init__(self):
        self._appointments = {}
        self._lock = RLock()

    @staticmethod
    def _valid_id(value):
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def _utc(value):
        if not isinstance(value, datetime) or value.tzinfo is None:
            return None
        try:
            if value.utcoffset() is None:
                return None
            return value.astimezone(timezone.utc)
        except (OverflowError, ValueError):
            return None

    @staticmethod
    def _overlaps(start, end, other_start, other_end):
        # Half-open intervals [start, end): exact adjacency is allowed.
        return start < other_end and other_start < end

    def book_appointment(self, appointment_id, provider_id, start_utc, end_utc):
        if not self._valid_id(appointment_id):
            return BookingResult(False, "INVALID_APPOINTMENT_ID", "Appointment ID is required.")
        if not self._valid_id(provider_id):
            return BookingResult(False, "INVALID_PROVIDER_ID", "Provider ID is required.")
        start, end = self._utc(start_utc), self._utc(end_utc)
        if start is None or end is None:
            return BookingResult(False, "INVALID_TIMESTAMP", "Start and end must be timezone-aware datetimes.")
        if end <= start:
            return BookingResult(False, "INVALID_DURATION", "Appointment end must be later than its start.")

        appointment_id, provider_id = appointment_id.strip(), provider_id.strip()
        with self._lock:
            if appointment_id in self._appointments:
                return BookingResult(False, "DUPLICATE_APPOINTMENT_ID", "Appointment ID already exists.")
            for current in self._appointments.values():
                if (current.status is AppointmentStatus.ACTIVE
                    and current.provider_id == provider_id
                    and self._overlaps(start, end, current.start_utc, current.end_utc)):
                    return BookingResult(False, "BOOKING_CONFLICT", "Provider already has an overlapping active appointment.")
            appointment = Appointment(appointment_id, provider_id, start, end)
            self._appointments[appointment_id] = appointment
            return BookingResult(True, "BOOKED", "Appointment booked successfully.", appointment)

    def cancel_appointment(self, appointment_id):
        if not self._valid_id(appointment_id):
            return BookingResult(False, "INVALID_APPOINTMENT_ID", "Appointment ID is required.")
        key = appointment_id.strip()
        with self._lock:
            current = self._appointments.get(key)
            if current is None:
                return BookingResult(False, "APPOINTMENT_NOT_FOUND", "Appointment was not found.")
            if current.status is AppointmentStatus.CANCELLED:
                return BookingResult(False, "ALREADY_CANCELLED", "Appointment is already cancelled.")
            cancelled = Appointment(current.appointment_id, current.provider_id,
                                    current.start_utc, current.end_utc,
                                    AppointmentStatus.CANCELLED)
            self._appointments[key] = cancelled
            return BookingResult(True, "CANCELLED", "Appointment cancelled successfully.", cancelled)

    def get_appointment(self, appointment_id):
        if not self._valid_id(appointment_id):
            return None
        with self._lock:
            return self._appointments.get(appointment_id.strip())

    def list_appointments(self):
        with self._lock:
            return tuple(self._appointments.values())
