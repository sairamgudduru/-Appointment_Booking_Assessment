# AI Usage Record

## How I used AI

I used AI as an engineering assistant during requirement analysis,
implementation planning, and test design. I used it to break the
assessment into acceptance criteria, discuss the booking-overlap rule,
UTC timestamp handling, cancellation behavior and concurrency risks,
identify test scenarios, and review the implementation approach against
the requirements.

I treated AI responses as suggestions rather than proof that the
solution was correct. I reviewed the proposed logic and test scenarios,
made the implementation decisions, and ran the tests locally using the
project's Python environment.

## Prompts and how the suggestions were used

### 1. Understand the assessment requirements

**Prompt (summary):** Review the appointment-booking assessment and
identify the required behavior, acceptance criteria, scope boundaries,
and deliverables.

**AI assistance:** The response organized the requirements into booking
validation, provider-specific overlap prevention, adjacent appointments,
cancellation, invalid-input handling, concurrency considerations, tests,
and documentation.

**Decision:** Used this breakdown to plan the service methods and test
coverage.

**How I checked it:** Compared the breakdown with the assessment
requirements and mapped the required behaviors to the implementation and
automated tests.

### 2. Review the appointment-overlap rule

**Prompt (summary):** Suggest an interval-overlap check that rejects
appointments that overlap but allows appointments that meet exactly at
an endpoint.

**AI assistance:** The response suggested treating appointments as
half-open intervals `[start, end)`. Under this rule, two intervals
overlap when `new_start < existing_end` and `existing_start < new_end`.

**Decision:** Used this condition in the overlap-checking logic.

**How I checked it:** Reviewed the condition against examples and
included tests for overlapping intervals, contained intervals, and
appointments adjacent at either boundary.

### 3. Review timestamp validation and UTC handling

**Prompt (summary):** Identify timestamp-comparison risks and recommend
a consistent UTC approach for appointment intervals.

**AI assistance:** The response highlighted the risk of comparing naive
and timezone-aware datetimes. It recommended requiring timezone-aware
values and normalizing them to UTC before comparison.

**Decision:** Applied this approach: naive and non-datetime inputs are
rejected, while timezone-aware values are converted to UTC.

**How I checked it:** Added tests for naive start and end values, string
inputs, and timezone-aware values supplied with a non-UTC offset.

### 4. Identify concurrency risks

**Prompt (summary):** Explain what could happen if two requests attempt
to book overlapping time for the same provider at the same time, and
suggest a proportionate safeguard for the in-memory prototype.

**AI assistance:** The response explained that checking for a conflict
and inserting the appointment must be protected as one critical
operation. It also distinguished a process-local lock from database or
distributed locking.

**Decision:** Used an `RLock` to protect the booking operation within a
shared service instance. The limitation for multiple processes or hosts
is documented.

**How I checked it:** Added a concurrency test in which two threads
attempt to book the same provider and time interval, and checked that
only one booking succeeds. A separate test checks that bookings for
different providers can both succeed.

### 5. Generate and review test scenarios against the acceptance criteria

**Prompt (summary):** Identify test cases for successful booking,
conflicts, adjacency, provider separation, cancellation, invalid input,
and whether rejected operations leave stored data unchanged.

**AI assistance:** The response helped turn the acceptance criteria into
specific test scenarios, including positive cases, negative cases,
boundary cases, and concurrency cases.

**Decision:** Used the suggested scenarios as a test-design checklist
and implemented them in the pytest suite. The tests are grouped into
booking, cancellation, concurrency, and validation modules.

**How I checked it:** Ran the test suite locally with
`python -m pytest -v` and reviewed the individual test results. The
local run collected 27 tests and all 27 passed. The detailed output is
recorded in `TEST_RESULTS.txt`.

### 6. Review cancellation and state integrity

**Prompt (summary):** Review expected cancellation behavior and identify
cases where invalid or rejected operations must not change existing
bookings.

**AI assistance:** The response highlighted missing and
already-cancelled appointment IDs, the need for cancelled appointments
to stop blocking their time, and the importance of avoiding state
changes when validation fails.

**Decision:** Implemented cancellation status handling and validation
before storing a new booking.

**How I checked it:** Tests cover cancelling an active appointment,
cancelling a missing or already-cancelled appointment, booking a
previously released time, and confirming that invalid booking input does
not alter existing state.

## Test execution evidence

The project was tested locally on Windows using Python 3.9.13 and pytest
8.4.2.

Command:

``` powershell
python -m pytest -v
```

Result:

``` text
collected 27 items

27 passed
```

The full test output, including individual test names, is available in
`TEST_RESULTS.txt`.

## Reflection

AI was useful for structuring the requirements, discussing
implementation trade-offs, and identifying test cases that might
otherwise be missed. It did not replace checking the assessment criteria
or running the tests. I reviewed the suggestions, used the ones that fit
the scope, and verified the resulting test suite in my local
environment.

The passing tests provide evidence for the scenarios covered by the
suite; they do not prove that every possible production scenario has
been tested. The implementation's in-memory storage and process-local
locking limitations are documented separately.