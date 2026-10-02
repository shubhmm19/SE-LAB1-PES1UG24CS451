# Work Breakdown Structure (WBS)
## Hyperlocal Courier Dispatch & Tracking Engine — PES1UG24CS451

## Hierarchy

```
0 Hyperlocal Courier Dispatch & Tracking Engine
├── 1 Project Management
│   ├── 1.1 Planning & scheduling
│   ├── 1.2 Risk management
│   └── 1.3 Status tracking & reporting
├── 2 Requirements & Design
│   ├── 2.1 Requirements elicitation (FR, NFR)
│   ├── 2.2 RTM & SRS
│   ├── 2.3 Use-case modelling
│   └── 2.4 Architecture design
├── 3 Development
│   ├── 3.1 Order Service + Nearest Rider Matching data (FR-001)
│   ├── 3.2 Dispatch & Matching Service (FR-001, NFR-002)
│   ├── 3.3 Route Optimization Service (FR-002)
│   ├── 3.4 OTP Service (FR-003)
│   ├── 3.5 Tracking + Notification Services (FR-004, NFR-001)
│   ├── 3.6 Availability Service (FR-005)
│   ├── 3.7 Sender Client App
│   └── 3.8 Delivery Rider App
├── 4 Infrastructure & Non-Functional
│   ├── 4.1 Security (TLS, auth, encryption)
│   ├── 4.2 Scalability & reliability (LB, Kafka, retries)
│   └── 4.3 CI/CD & deployment
├── 5 Testing
│   ├── 5.1 Unit tests
│   ├── 5.2 Integration tests (TC-001 – TC-014)
│   ├── 5.3 Load & failover tests (TC-015, TC-016)
│   └── 5.4 User acceptance testing
└── 6 Deployment & Closure
    ├── 6.1 Production release
    ├── 6.2 Documentation & handover
    └── 6.3 Project review
```

## Work Package Table
| WBS | Task | Deliverable | Linked Req | Effort (days) | Depends on |
|-----|------|-------------|-----------|---------------|-----------|
| 1.1 | Planning & scheduling | Project plan | — | 3 | — |
| 2.1 | Requirements elicitation | FR/NFR document | All | 4 | 1.1 |
| 2.2 | RTM & SRS | RTM, SRS | All | 5 | 2.1 |
| 2.3 | Use-case modelling | Use-case diagram & flow | All | 3 | 2.1 |
| 2.4 | Architecture design | Architecture diagram | All | 5 | 2.2 |
| 3.1 | Order Service | Order APIs, state machine | FR-001, FR-004 | 6 | 2.4 |
| 3.2 | Dispatch & Matching | Matching + retry logic | FR-001, NFR-002 | 8 | 3.1 |
| 3.3 | Route Optimization | Routing service | FR-002 | 7 | 2.4 |
| 3.4 | OTP Service | OTP generate/verify | FR-003 | 4 | 2.4 |
| 3.5 | Tracking + Notification | Live tracking, push/SMS | FR-004, NFR-001 | 8 | 3.1 |
| 3.6 | Availability Service | Toggle API | FR-005 | 3 | 2.4 |
| 3.7 | Sender app | Mobile app | FR-004 | 8 | 3.1 |
| 3.8 | Rider app | Mobile app | FR-002/003/005 | 10 | 3.2–3.6 |
| 4.1 | Security hardening | TLS, auth, encryption | NFR-001 | 4 | 3.5 |
| 4.2 | Scalability & reliability | LB, Kafka, autoscaling | NFR-002 | 5 | 3.2 |
| 4.3 | CI/CD | Pipeline | — | 3 | 2.4 |
| 5.1 | Unit tests | Test suite | All | 6 | 3.x |
| 5.2 | Integration tests | Test report | All | 5 | 5.1 |
| 5.3 | Load & failover | Perf report | NFR-001/002 | 4 | 4.2 |
| 5.4 | UAT | Sign-off | All | 3 | 5.2 |
| 6.1 | Release | Live system | — | 2 | 5.4 |
| 6.2 | Handover docs | User/admin guide | — | 2 | 6.1 |

## Milestones
| Milestone | Completion of |
|-----------|---------------|
| M1 Requirements baselined | 2.1–2.3 |
| M2 Architecture approved | 2.4 |
| M3 Core backend complete | 3.1–3.6 |
| M4 Apps integrated | 3.7–3.8 |
| M5 Tests passed | 5.x |
| M6 Release | 6.1 |
