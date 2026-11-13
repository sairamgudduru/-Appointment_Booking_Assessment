# Limitations and Follow-up Risks

- **In-memory storage:** Appointments are lost when the process stops. A production service needs persistent storage.
- **Process-local lock:** `RLock` protects threads sharing one service instance only. It does not coordinate multiple processes, containers, or hosts.
- **Linear conflict scan:** Each booking scans stored appointments, O(n). A larger system may need indexing or database-supported conflict checks.
- **No provider availability rules:** Working hours, leave, breaks, and provider-specific availability are not checked.
- **No authentication or authorization:** The prototype assumes trusted callers.
- **No API or UI:** This is a Python service slice, as allowed by the assessment.
- **No recurring appointments or calendar integration:** These are outside the requested scope.
- **Appointment ID lifecycle:** IDs remain reserved after cancellation for the lifetime of the in-memory store.
- **Datetime input format:** The service accepts timezone-aware Python `datetime` objects, not timestamp strings.
