from appointment_booking import AppointmentStatus

def test_cancel_active_booking(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    result = service.cancel_appointment("A1")
    assert result.success and result.appointment.status is AppointmentStatus.CANCELLED

def test_cancelled_time_can_be_booked_again(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    service.cancel_appointment("A1")
    assert service.book_appointment("A2", "P1", at(10), at(11)).success

def test_missing_booking_cancellation(service):
    result = service.cancel_appointment("missing")
    assert not result.success and result.code == "APPOINTMENT_NOT_FOUND"

def test_repeated_cancellation(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    service.cancel_appointment("A1")
    assert service.cancel_appointment("A1").code == "ALREADY_CANCELLED"

def test_cancelling_one_does_not_change_another(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    service.book_appointment("A2", "P2", at(10), at(11))
    service.cancel_appointment("A1")
    assert service.get_appointment("A2").status is AppointmentStatus.ACTIVE

def test_cancelled_id_is_not_reused(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    service.cancel_appointment("A1")
    assert service.book_appointment("A1", "P1", at(12), at(13)).code == "DUPLICATE_APPOINTMENT_ID"
