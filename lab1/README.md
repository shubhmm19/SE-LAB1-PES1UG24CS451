# Lab 1 — Requirements Engineering & UML Use-Case Modelling
### Problem Statement #23: Hyperlocal Courier Dispatch & Tracking Engine
*Smart Cities, Transport & Logistics — PES University, Dept. of CSE*

## Overview
An on-demand package delivery platform that assigns local parcel pickups to the nearest delivery rider, optimizes multi-stop routing, and enforces OTP verification at the destination.

**Actors:** Sender Client, Delivery Rider

## Repository Contents

| File | Contents |
|---|---|
| [`requirements.md`](./requirements.md) | Complete requirements table — 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001–NFR-002), each with ID, Type (NFRs), Description, Priority, Acceptance Criteria, and Rationale. |
| [`usecase_diagram.png`](./usecase_diagram.png) | UML Use-Case Diagram covering all actors and primary use cases, including one `«include»` relationship pair and one `«extend»` relationship pair (two of each are modelled). |
| [`usecase_diagram.puml`](./usecase_diagram.puml) | Editable PlantUML source for the diagram above (render at [plantuml.com](https://www.plantuml.com/plantuml) or with a local PlantUML/Java setup, or the PlantUML VS Code extension). |
| [`usecase_flow.md`](./usecase_flow.md) | 1-page Use-Case Flow Specification for the core use case **"Place Courier Request"** — Preconditions, Postconditions, Main Success Scenario, and an Alternate Flow. |

## Use-Case Diagram Summary

```
Sender Client ──── Place Courier Request ──«include»──▶ Match Nearest Rider
Sender Client ──── Track Delivery Status  ◀─«extend»─── Cancel Order
Delivery Rider ─── Receive Dispatch Notification ◀─«extend»─── Optimize Multi-Stop Route
Delivery Rider ─── Toggle Availability
Delivery Rider ─── Complete Delivery ──«include»──▶ Verify OTP
```

## Requirement → Use Case Traceability

| Requirement | Realized By |
|---|---|
| FR-001 Nearest Rider Matching | Match Nearest Rider |
| FR-002 Multi-Stop Route Optimization | Optimize Multi-Stop Route |
| FR-003 OTP Generation & Verification | Verify OTP |
| FR-004 Real-Time Order Status Notifications | Track Delivery Status, Receive Dispatch Notification |
| FR-005 Rider Availability Toggle | Toggle Availability |
| NFR-001 Telemetry Latency & Security | Track Delivery Status (non-functional constraint) |
| NFR-002 Dispatch Reliability & Scalability | Match Nearest Rider (non-functional constraint) |

## Deliverables Checklist
- [x] Exactly 5 Functional Requirements (FR-001 to FR-005)
- [x] 2 Non-Functional Requirements (NFR-001 & NFR-002)
- [x] UML Use-Case Diagram with all actors and primary use cases
- [x] At least one `«include»` relationship
- [x] At least one `«extend»` relationship
- [x] 1-page Use-Case Flow Specification (Preconditions, Postconditions, Main Success Scenario, Alternate Flow)
