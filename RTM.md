# Requirements Traceability Matrix (RTM)

**Project:** Hyperlocal Courier Dispatch & Tracking Engine — PES1UG24CS451

Traces each requirement forward to use case, architecture component, SRS section, work package (WBS) and test case.

| Req ID | Requirement | Priority | Use Case(s) | Actor | Architecture Component(s) | SRS Section | WBS Task(s) | Test Case(s) | Status |
|--------|-------------|----------|-------------|-------|---------------------------|-------------|-------------|--------------|--------|
| FR-001 | Nearest Rider Matching | High | UC-02 Match Nearest Rider (included by UC-01 Place Courier Request) | Sender Client, Rider | Dispatch & Matching Service, Redis Geo Cache, Order Service | 3.1 | 3.1, 3.2 | TC-001, TC-002, TC-003 | Planned |
| FR-002 | Multi-Stop Route Optimization | High | UC-06 Optimize Multi-Stop Route (extends UC-05 Receive Dispatch Notification) | Rider | Route Optimization Service, Maps API | 3.2 | 3.3 | TC-004, TC-005 | Planned |
| FR-003 | OTP Generation & Verification | High | UC-09 Verify OTP (included by UC-08 Complete Delivery) | Rider, Sender Client | OTP Service, Notification Service, Order Service | 3.3 | 3.4 | TC-006, TC-007, TC-008 | Planned |
| FR-004 | Real-Time Order Status Notifications | Medium | UC-03 Track Delivery Status, UC-05 Receive Dispatch Notification, UC-04 Cancel Order (extends UC-03) | Sender Client, Rider | Notification Service, Tracking Service, Message Broker | 3.4 | 3.5 | TC-009, TC-010 | Planned |
| FR-005 | Rider Availability Toggle | Medium | UC-07 Toggle Availability | Rider | Availability Service, Redis Geo Cache, Rider App | 3.5 | 3.6 | TC-011, TC-012 | Planned |
| NFR-001 | Telemetry Latency & Security | High | UC-03 Track Delivery Status | Sender Client, Rider | Tracking Service, API Gateway (TLS), Auth Service, Time-series Store | 4.1, 4.2 | 3.5, 4.1 | TC-013, TC-014 | Planned |
| NFR-002 | Dispatch Reliability & Scalability | High | UC-02 Match Nearest Rider | System | Dispatch Service, Message Broker, Load Balancer, PostgreSQL | 4.3, 4.4 | 3.2, 4.2 | TC-015, TC-016 | Planned |

## Use Case Index
| ID | Use Case | Relationship |
|----|----------|--------------|
| UC-01 | Place Courier Request | «include» UC-02 |
| UC-02 | Match Nearest Rider | included by UC-01 |
| UC-03 | Track Delivery Status | extended by UC-04 |
| UC-04 | Cancel Order | «extend» UC-03 |
| UC-05 | Receive Dispatch Notification | extended by UC-06 |
| UC-06 | Optimize Multi-Stop Route | «extend» UC-05 |
| UC-07 | Toggle Availability | — |
| UC-08 | Complete Delivery | «include» UC-09 |
| UC-09 | Verify OTP | included by UC-08 |

## Test Case Index
| ID | Description |
|----|-------------|
| TC-001 | Nearest of several available riders is assigned |
| TC-002 | No available rider → request queued and sender informed |
| TC-003 | Rider declines/times out → next nearest offered |
| TC-004 | Route for 2–10 stops returned within 3 s |
| TC-005 | Optimized route not longer than naive sequence |
| TC-006 | Correct OTP completes delivery |
| TC-007 | Wrong OTP rejected; 3 failures escalate |
| TC-008 | Expired / reused OTP rejected |
| TC-009 | Notification sent on each state change within 5 s |
| TC-010 | Cancel order notifies rider and sender |
| TC-011 | Unavailable rider receives no dispatch |
| TC-012 | Toggle off during active order shows warning |
| TC-013 | 95th-percentile location latency ≤ 3 s |
| TC-014 | Non-owner cannot view rider location; TLS enforced |
| TC-015 | Load test: 10,000 orders / 5,000 riders, no double assignment |
| TC-016 | Service instance failure → dispatch retried, no lost orders |
