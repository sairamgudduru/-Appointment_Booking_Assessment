from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from appointment_booking import AppointmentStatus

def test_only_one_simultaneous_overlapping_booking_succeeds(service, at):
    barrier = Barrier(2)
    def attempt(appointment_id):
        barrier.wait()
        return service.book_appointment(appointment_id, "P1", at(10), at(11))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, ["A1", "A2"]))
    assert sum(result.success for result in results) == 1
    active = [a for a in service.list_appointments() if a.status is AppointmentStatus.ACTIVE]
    assert len(active) == 1

def test_simultaneous_different_provider_bookings_both_succeed(service, at):
    barrier = Barrier(2)
    def attempt(appointment_id, provider_id):
        barrier.wait()
        return service.book_appointment(appointment_id, provider_id, at(10), at(11))
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(attempt, "A1", "P1"), pool.submit(attempt, "A2", "P2")]
        assert all(f.result().success for f in futures)
