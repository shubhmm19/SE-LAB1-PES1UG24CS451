# Architecture Description

**Style:** Layered microservice architecture with event-driven dispatch.
Diagram: `architecture_diagram.svg` (editable source: `architecture.puml`).

| Layer | Component | Responsibility | Requirement |
|-------|-----------|----------------|-------------|
| Client | Sender Client App | Place, track, cancel orders | FR-004 |
| Client | Delivery Rider App | Receive dispatch, route, OTP entry, availability, GPS telemetry | FR-002/003/005 |
| Edge | API Gateway / Load Balancer | TLS termination, auth check, rate limiting, routing | NFR-001, NFR-002 |
| Service | Auth Service | Login, tokens, role-based access | NFR-001 |
| Service | Order Service | Order lifecycle and state machine | FR-001, FR-004 |
| Service | Dispatch & Matching | Nearest rider search, offer/timeout/retry | FR-001, NFR-002 |
| Service | Route Optimization | Multi-stop sequencing using maps API | FR-002 |
| Service | OTP Service | Generate, expire, verify OTPs | FR-003 |
| Service | Tracking / Telemetry | Ingest GPS, serve live location | NFR-001 |
| Service | Notification Service | Push/SMS on state changes | FR-004 |
| Service | Availability Service | Rider available/unavailable state | FR-005 |
| Messaging | Kafka | Decouples services; durable retry | NFR-002 |
| Data | PostgreSQL / Redis Geo / Time-series | Persistent data, geo lookups, telemetry | all |
| External | Maps API, SMS/Push gateway | Routing and message delivery | FR-002, FR-003 |

**Key decisions**
- Redis geospatial index gives fast nearest-rider lookups (FR-001).
- Event broker with retries avoids lost or double-assigned orders (NFR-002).
- Dispatch is stateless, so it scales horizontally.
