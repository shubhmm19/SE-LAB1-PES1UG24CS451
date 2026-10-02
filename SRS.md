# Software Requirements Specification (SRS)
## Hyperlocal Courier Dispatch & Tracking Engine
Student: PES1UG24CS451 — PES University, Dept. of CSE — Version 1.0

---
## 1. Introduction
### 1.1 Purpose
Defines the functional and non-functional requirements of the Hyperlocal Courier Dispatch & Tracking Engine for developers, testers and evaluators.
### 1.2 Scope
An on-demand package delivery platform that assigns local pickups to the nearest rider, optimizes multi-stop routes, tracks deliveries live, and enforces OTP verification at the destination. Payments are out of scope.
### 1.3 Definitions
| Term | Meaning |
|------|---------|
| Sender Client | User who requests a courier pickup |
| Delivery Rider | Person who picks up and delivers parcels |
| OTP | One-time password for handover verification |
| RTM | Requirements Traceability Matrix |
### 1.4 References
Problem Statement #23; `1-RE/FR_and_NFR.md`; `1-RE/RTM.md`; `2-Architecture/`.

## 2. Overall Description
### 2.1 Product Perspective
Client–server system: two mobile apps (sender, rider), a backend of microservices, and external maps and messaging services.
### 2.2 User Classes
| Actor | Description |
|-------|-------------|
| Sender Client | Places, tracks and cancels orders |
| Delivery Rider | Accepts jobs, follows routes, verifies OTP, toggles availability |
### 2.3 Operating Environment
Android/iOS apps; cloud-hosted backend; internet connectivity and GPS required.
### 2.4 Constraints
Dependence on third-party maps/SMS; mobile network quality; location privacy regulations.
### 2.5 Assumptions
Riders carry GPS-enabled smartphones; receivers have a phone number for OTP.

## 3. Functional Requirements
### 3.1 FR-001 Nearest Rider Matching
Assign each request to the nearest available rider using live location; offer expires after 30 s and passes to the next rider. Use case: UC-02 (included by UC-01).
### 3.2 FR-002 Multi-Stop Route Optimization
Compute an optimized sequence for 2–10 stops within 3 s. Use case: UC-06.
### 3.3 FR-003 OTP Generation & Verification
Generate a single-use time-limited OTP per order; delivery completes only on correct entry; 3 failures escalate. Use cases: UC-08, UC-09.
### 3.4 FR-004 Real-Time Order Status Notifications
Notify on Placed, Assigned, Picked Up, In Transit, Delivered, Cancelled within 5 s. Use cases: UC-03, UC-04, UC-05.
### 3.5 FR-005 Rider Availability Toggle
Rider switches Available/Unavailable; takes effect within 2 s; only available riders are dispatched. Use case: UC-07.

## 4. Non-Functional Requirements
### 4.1 Performance (NFR-001)
95% of location updates reach the sender in ≤ 3 s.
### 4.2 Security (NFR-001)
TLS 1.2+; encryption at rest; role-based access so only the order's sender sees rider location; OTPs stored hashed.
### 4.3 Reliability (NFR-002)
≥ 99.5% monthly availability; automatic retry; no double assignment.
### 4.4 Scalability (NFR-002)
10,000 concurrent orders and 5,000 concurrent riders via horizontal scaling.
### 4.5 Usability
Core flows (place order, accept job) completable in ≤ 3 taps/screens after login.

## 5. External Interface Requirements
| Interface | Description |
|-----------|-------------|
| User interface | Sender app: order form, tracking map. Rider app: job card, route map, OTP entry, availability switch |
| Software interface | Maps/Routing API; SMS/Push gateway |
| Communication | HTTPS REST + WebSocket/push for real-time updates |
| Hardware | Smartphone GPS |

## 6. System Models
Use-case diagram (Lab 1 repo) and architecture (`2-Architecture/architecture_diagram.svg`).

### Order State Flow
Placed → Assigned → Picked Up → In Transit → Delivered (Cancelled possible before Picked Up).

## 7. Traceability
See `1-RE/RTM.md`.

## 8. Acceptance Summary
Each requirement is accepted when its criteria in `1-RE/FR_and_NFR.md` and mapped test cases TC-001–TC-016 pass.
