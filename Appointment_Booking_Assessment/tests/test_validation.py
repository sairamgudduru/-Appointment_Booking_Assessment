from datetime import datetime, timezone, timedelta

def test_missing_appointment_id(service, at):
    result = service.book_appointment(" ", "P1", at(10), at(11))
    assert result.code == "INVALID_APPOINTMENT_ID" and service.list_appointments() == ()

def test_missing_provider_id(service, at):
    result = service.book_appointment("A1", "", at(10), at(11))
    assert result.code == "INVALID_PROVIDER_ID" and service.list_appointments() == ()

def test_naive_start_rejected(service, at):
    result = service.book_appointment("A1", "P1", datetime(2026, 1, 1, 10), at(11))
    assert result.code == "INVALID_TIMESTAMP"

def test_naive_end_rejected(service, at):
    result = service.book_appointment("A1", "P1", at(10), datetime(2026, 1, 1, 11))
    assert result.code == "INVALID_TIMESTAMP"

def test_string_timestamp_rejected(service):
    result = service.book_appointment("A1", "P1", "2026-01-01T10:00:00Z", "2026-01-01T11:00:00Z")
    assert result.code == "INVALID_TIMESTAMP"

def test_zero_duration_rejected(service, at):
    result = service.book_appointment("A1", "P1", at(10), at(10))
    assert result.code == "INVALID_DURATION" and service.list_appointments() == ()

def test_negative_duration_rejected(service, at):
    assert service.book_appointment("A1", "P1", at(11), at(10)).code == "INVALID_DURATION"

def test_missing_cancel_id_rejected(service):
    assert service.cancel_appointment(" ").code == "INVALID_APPOINTMENT_ID"

def test_invalid_booking_does_not_change_existing_state(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    before = service.list_appointments()
    service.book_appointment("A2", "P1", at(11), at(10))
    assert service.list_appointments() == before

def test_non_utc_aware_datetimes_normalized(service):
    start = datetime(2026, 1, 1, 15, tzinfo=timezone(timedelta(hours=5)))
    end = datetime(2026, 1, 1, 16, tzinfo=timezone(timedelta(hours=5)))
    result = service.book_appointment("A1", "P1", start, end)
    assert result.success and result.appointment.start_utc.hour == 10
    assert result.appointment.start_utc.utcoffset().total_seconds() == 0
