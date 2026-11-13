def test_valid_booking(service, at):
    result = service.book_appointment("A1", "P1", at(10), at(11))
    assert result.success and result.code == "BOOKED"

def test_same_provider_overlap_rejected(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A2", "P1", at(10, 30), at(11, 30)).code == "BOOKING_CONFLICT"

def test_adjacent_start_allowed(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A2", "P1", at(11), at(12)).success

def test_adjacent_end_allowed(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A2", "P1", at(9), at(10)).success

def test_different_providers_do_not_conflict(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A2", "P2", at(10), at(11)).success

def test_contained_interval_conflicts(service, at):
    service.book_appointment("A1", "P1", at(9), at(12))
    assert service.book_appointment("A2", "P1", at(10), at(11)).code == "BOOKING_CONFLICT"

def test_interval_containing_existing_conflicts(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A2", "P1", at(9), at(12)).code == "BOOKING_CONFLICT"

def test_duplicate_appointment_id_rejected(service, at):
    service.book_appointment("A1", "P1", at(10), at(11))
    assert service.book_appointment("A1", "P2", at(12), at(13)).code == "DUPLICATE_APPOINTMENT_ID"

def test_ids_are_trimmed(service, at):
    result = service.book_appointment(" A1 ", " P1 ", at(10), at(11))
    assert result.appointment.appointment_id == "A1"
    assert result.appointment.provider_id == "P1"
