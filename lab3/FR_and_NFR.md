# Requirements Specification — Functional & Non-Functional Requirements

**Project:** Hyperlocal Courier Dispatch & Tracking Engine (Problem Statement #23)
**Course:** Software Engineering, PES University, Dept. of CSE — Lab 1
**Student:** PES1UG24CS451
**Actors:** Sender Client, Delivery Rider

---

## 1. Functional Requirements (FR)

| ID | Title | Description | Priority | Acceptance Criteria | Rationale |
|----|-------|-------------|----------|---------------------|-----------|
| FR-001 | Nearest Rider Matching | The system shall assign each new courier request to the nearest available Delivery Rider, based on the rider's live GPS location and the pickup location. | High | Given a request and ≥1 available rider, the rider with the smallest distance to pickup is assigned within 5 s; if the rider declines or times out (30 s), the next nearest rider is offered the job. | Core value of the platform: fast pickups reduce delivery time and rider idle time. |
| FR-002 | Multi-Stop Route Optimization | The system shall compute an optimized stop sequence for a rider holding multiple pickups/drop-offs, minimizing total travel distance/time. | High | For a rider with 2–10 stops, a route is returned within 3 s and its total distance is no worse than the order-received (naive) sequence. | Batching parcels lowers cost per delivery and improves rider productivity. |
| FR-003 | OTP Generation & Verification | The system shall generate a one-time password per order, send it to the receiver, and require the rider to enter it at the destination before an order can be marked delivered. | High | OTP is 4–6 digits, valid for a limited period, single use; wrong OTP is rejected; delivery is completed only on a correct OTP; max 3 failed attempts then escalation. | Prevents wrong or fraudulent handovers and provides proof of delivery. |
| FR-004 | Real-Time Order Status Notifications | The system shall notify the Sender Client (and Rider where relevant) of every order state change (Placed, Assigned, Picked Up, In Transit, Delivered, Cancelled) in real time. | Medium | A notification is delivered within 5 s of each state change; the sender can view the current status and live rider location on a tracking screen. | Transparency builds trust and reduces support queries. |
| FR-005 | Rider Availability Toggle | The system shall let a Delivery Rider switch between Available and Unavailable; only Available riders are considered for dispatch. | Medium | Toggle takes effect within 2 s; an Unavailable rider receives no new dispatches; riders cannot go Unavailable while carrying an active order without an explicit warning. | Gives riders control over working hours and keeps the dispatch pool accurate. |

---

## 2. Non-Functional Requirements (NFR)

| ID | Type | Title | Description | Priority | Acceptance Criteria | Rationale |
|----|------|-------|-------------|----------|---------------------|-----------|
| NFR-001 | Performance & Security | Telemetry Latency & Security | Rider location telemetry shall reach the tracking service with low latency and be transmitted/stored securely. | High | 95% of location updates are visible to the sender in ≤ 3 s end-to-end; all traffic over TLS 1.2+; location data encrypted at rest; only the sender of an active order can view that rider's location. | Live tracking is useless if stale; location data is personal and sensitive. |
| NFR-002 | Reliability & Scalability | Dispatch Reliability & Scalability | The dispatch engine shall remain available and scale during peak demand without losing or double-assigning orders. | High | ≥ 99.5% monthly availability; supports 10,000 concurrent active orders and 5,000 concurrent riders with horizontal scaling; no order is assigned to two riders; failed dispatches are retried automatically. | Peak hours (rain, festivals) are when users need the service most. |

---

## 3. Assumptions & Constraints

- Riders use a smartphone with GPS and mobile data.
- A third-party maps/routing API and an SMS/push gateway are available.
- Payment handling is out of scope for this lab.
- Numeric targets above (latencies, capacity) are design targets to be validated during testing.
