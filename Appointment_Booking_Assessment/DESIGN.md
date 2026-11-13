# Design Specification

## Service boundary
`AppointmentBookingService` owns the in-memory appointment collection and provides:
- `book_appointment(appointment_id, provider_id, start_utc, end_utc)`
- `cancel_appointment(appointment_id)`
- `get_appointment(appointment_id)` and `list_appointments()` for inspection.

The service is limited to booking conflict detection and cancellation. It does not manage provider working hours, customers, reminders, or calendar integrations.

## Data model
Each `Appointment` stores an appointment ID, provider ID, UTC start and end datetimes, and an `active` or `cancelled` status. `BookingResult` contains a success flag, result code, message, and optional appointment.

## Booking invariant
Two distinct active appointments for the same provider must never overlap. Intervals are half-open: `[start, end)`. A conflict exists when:

`new_start < existing_end and existing_start < new_end`

Therefore, an appointment ending at 11:00 and another beginning at 11:00 are adjacent and allowed. Appointments for different providers do not conflict.

## Booking flow
1. Validate appointment and provider identifiers.
2. Require timezone-aware datetime values and normalize them to UTC.
3. Reject `end <= start`.
4. Acquire the service lock.
5. Reject an appointment ID already in the store.
6. Check every active appointment for the same provider.
7. Reject an overlap or store the new appointment as active.

Invalid and conflicting requests do not modify stored appointments.

## Cancellation flow
The service validates the ID and looks up the appointment under the lock. A missing ID returns `APPOINTMENT_NOT_FOUND`; a cancelled record returns `ALREADY_CANCELLED`. Otherwise, the status changes to `cancelled`. Conflict checks ignore cancelled records, so the interval becomes available again. Appointment IDs are not reused after cancellation.

## Concurrency and persistence
A `threading.RLock` protects the conflict check plus insertion, cancellation, and reads. This prevents competing threads sharing one service instance from both booking overlapping times for the same provider.

The lock is process-local; it does not coordinate multiple processes or application instances. A persistent implementation would require a database transaction and a concurrency strategy that enforces the invariant across all writers, such as provider-scoped locking or an appropriate database locking/constraint design.

## Results and tradeoffs
Expected outcomes are returned as structured result codes such as `BOOKED`, `BOOKING_CONFLICT`, `INVALID_TIMESTAMP`, `INVALID_DURATION`, `CANCELLED`, `APPOINTMENT_NOT_FOUND`, and `ALREADY_CANCELLED`.

The in-memory store is easy to run but loses data when the process exits. Conflict detection scans stored appointments, O(n), which is acceptable for this small prototype but may need indexing or database support at scale.
