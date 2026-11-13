# Appointment Booking Service

A small Python service implementing the appointment-conflict and cancellation feature from the AI-Assisted Engineering Assessment.

## Features
- Prevents overlapping active appointments for the same provider.
- Allows overlapping appointments for different providers.
- Allows adjacent intervals where one appointment ends exactly when another begins.
- Cancels an appointment so its time can be booked again.
- Rejects invalid timestamps, missing identifiers, non-positive durations, and duplicate appointment IDs.
- Uses a process-local lock to protect booking and cancellation operations.

## Requirements
- Python 3.9.13
- pytest 8.x

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run individual test modules

Run booking tests:
```bash
python -m pytest tests/test_booking.py -v
```

Run cancellation tests:
```bash
python -m pytest tests/test_cancellation.py -v
```

Run concurrency tests:
```bash
python -m pytest tests/test_concurrency.py -v
```

Run validation tests:
```bash
python -m pytest tests/test_validation.py -v
```

Run all tests:
```bash
python -m pytest -v
```


Optional coverage:

```bash
python -m pip install pytest-cov
python -m pytest --cov=appointment_booking --cov-report=term-missing
```

## Example

```python
from datetime import datetime, timezone
from appointment_booking import AppointmentBookingService

service = AppointmentBookingService()
start = datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc)
end = datetime(2026, 1, 1, 11, 0, tzinfo=timezone.utc)

result = service.book_appointment("APT-100", "PROV-10", start, end)
print(result.code, result.message)

cancelled = service.cancel_appointment("APT-100")
print(cancelled.code, cancelled.message)
```

The service accepts timezone-aware `datetime` objects and normalizes them to UTC. Naive datetimes are rejected.

## Layout
- `appointment_booking/models.py` — appointment and result models.
- `appointment_booking/service.py` — booking, conflict checking, cancellation, and in-memory state.
- `tests/` — automated tests, including a thread concurrency test.
- `DESIGN.md` — service design and booking invariant.
- `ASSUMPTIONS.md` — explicit behavior assumptions.
- `AI_USAGE.md` — AI prompts, decisions, and verification record.
- `LIMITATIONS.md` — known limitations and follow-up risks.
- `TEST_RESULTS.txt` — recorded test run.

This is a bounded service prototype, not a complete scheduling product. No frontend, authentication, notifications, database, calendar integration, or deployment configuration is included.
