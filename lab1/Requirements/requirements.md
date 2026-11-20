# Requirements Table
### Problem Statement #23 — Hyperlocal Courier Dispatch & Tracking Engine
**Stakeholders / Actors:** Sender Client, Delivery Rider

---

## Functional Requirements

### FR-001 — Nearest Rider Matching
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | The system shall match an outgoing courier request with the nearest active Delivery Rider within a 3 km radius of the pickup location. |
| **Acceptance Criteria** | **Pass:** Rider receives a dispatch notification with the pickup location, and the matched rider was online and within 3 km. **Fail:** Order is assigned to an offline rider or a rider outside the 3 km radius. |
| **Rationale** | Minimizing rider-to-pickup distance directly reduces pickup wait time, which is the core value proposition of a "hyperlocal" dispatch platform. |

### FR-002 — Multi-Stop Route Optimization
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | When a Delivery Rider holds more than one active pickup/drop-off in overlapping areas, the system shall compute and present an optimized stop sequence that minimizes total travel distance. |
| **Acceptance Criteria** | **Pass:** For a rider with 2+ concurrent orders, the suggested stop sequence has a total distance less than or equal to the naive (assignment-order) route. **Fail:** Stops are presented in raw assignment order with no distance optimization. |
| **Rationale** | Efficient multi-stop routing increases rider throughput (deliveries/hour) and lowers per-order operating cost, supporting platform scalability. |

### FR-003 — OTP Generation & Delivery Verification
| Field | Detail |
|---|---|
| **Priority** | High |
| **Description** | The system shall generate a unique one-time password (OTP) for each order at the time of dispatch and require the Delivery Rider to enter the OTP, confirmed by the recipient, before the order can be marked "Delivered." |
| **Acceptance Criteria** | **Pass:** Order status transitions to "Delivered" only after correct OTP entry. **Fail:** Order can be marked "Delivered" with no OTP entry or an incorrect OTP. |
| **Rationale** | OTP verification prevents fraudulent delivery confirmations and protects both sender and rider in disputes over non-delivery. |

### FR-004 — Real-Time Order Status Notifications
| Field | Detail |
|---|---|
| **Priority** | Medium |
| **Description** | The system shall push real-time notifications to the Sender Client whenever the order status changes (Assigned, Picked Up, In Transit, Delivered). |
| **Acceptance Criteria** | **Pass:** Sender Client receives a notification within 5 seconds of each status transition. **Fail:** The client-side status does not reflect the current backend order state. |
| **Rationale** | Timely status visibility builds sender trust in the platform and reduces support inquiries about order whereabouts. |

### FR-005 — Delivery Rider Availability Toggle
| Field | Detail |
|---|---|
| **Priority** | Medium |
| **Description** | The system shall allow a Delivery Rider to set their status to "Online" or "Offline," and shall exclude "Offline" riders from all nearest-rider matching computations. |
| **Acceptance Criteria** | **Pass:** An "Offline" rider is never returned by the matching query, even if physically nearest. **Fail:** An "Offline" rider receives a dispatch notification. |
| **Rationale** | Giving riders explicit control over availability respects working-hours autonomy and prevents dispatch to riders unable to fulfil deliveries. |

---

## Non-Functional Requirements

### NFR-001 — Live Telemetry Latency & Security
| Field | Detail |
|---|---|
| **Type** | Performance & Security |
| **Priority** | High |
| **Description** | Delivery status and live GPS telemetry updates from riders shall transmit to the Sender Client with under 2-second latency, over an encrypted channel. |
| **Acceptance Criteria** | **Pass:** Benchmarking tests confirm target latency and encryption standards under simulated peak load. **Fail:** Telemetry updates exceed 2 seconds or travel unencrypted. |
| **Rationale** | Low-latency, secure tracking is essential for sender confidence in real-time visibility and for protecting rider/recipient location privacy. |

### NFR-002 — Dispatch Reliability & Scalability
| Field | Detail |
|---|---|
| **Type** | Reliability & Scalability |
| **Priority** | High |
| **Description** | The dispatch-matching service shall maintain at least 99.9% uptime and continue matching riders without noticeable performance degradation under a simulated load of 10,000 concurrent active riders. |
| **Acceptance Criteria** | **Pass:** Load testing at 10,000 concurrent riders shows matching response time within the defined SLA and no service outage. **Fail:** Downtime exceeds the allowed threshold or matching latency degrades beyond SLA under peak load. |
| **Rationale** | As a logistics platform, dispatch reliability directly drives delivery SLAs; downtime or slow matching during peak hours cascades into delays across the entire courier network. |
