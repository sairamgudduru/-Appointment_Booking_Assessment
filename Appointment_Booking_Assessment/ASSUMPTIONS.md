# Assumptions and Booking Invariant

## Assumptions
1. Appointment times must be timezone-aware Python `datetime` values. Naive datetimes are rejected because their timezone is ambiguous.
2. Aware datetimes with non-UTC offsets are accepted and normalized to UTC.
3. Intervals are half-open (`[start, end)`), so exact adjacency is allowed.
4. Duration must be positive (`end > start`).
5. Appointment IDs are unique for the lifetime of the service. Cancelled IDs are not reused.
6. Provider and appointment IDs must be non-empty strings; leading and trailing whitespace is stripped.
7. Only appointments with `active` status block a provider's time.
8. Missing and already-cancelled cancellation requests return clear failure results without changing stored state.
9. Provider working hours, breaks, and availability calendars are outside this assignment's scope.

## Booking invariant
For any two active appointments belonging to the same provider, their intervals must not overlap. For `[new_start, new_end)` and `[existing_start, existing_end)`, overlap is:

`new_start < existing_end and existing_start < new_end`

The conflict check and insertion occur under the same lock so two threads using this service instance cannot both reserve overlapping time for one provider.
