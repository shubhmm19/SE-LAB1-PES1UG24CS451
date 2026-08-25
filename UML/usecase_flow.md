# Use-Case Flow Specification

## Use Case: Place Courier Request

| Field | Detail |
|---|---|
| **Use Case ID** | UC-01 |
| **Primary Actor** | Sender Client |
| **Secondary Actor** | Delivery Rider |
| **Related Requirements** | FR-001 (Nearest Rider Matching), FR-004 (Real-Time Order Status Notifications) |
| **Included Use Case** | Match Nearest Rider (`«include»`) |

### Description
Allows a Sender Client to submit a new courier request by specifying a pickup location, drop-off location, and package details. The system automatically finds and dispatches the nearest available Delivery Rider.

### Preconditions
- PC-1: The Sender Client is authenticated and logged into the platform.
- PC-2: The pickup and drop-off addresses fall within the platform's active service coverage area.

### Postconditions (Success Guarantee)
- PS-1: A new courier order record exists with status `Assigned`.
- PS-2: A unique OTP has been generated and stored against the order for later delivery verification.
- PS-3: The assigned Delivery Rider has received a dispatch notification.
- PS-4: The Sender Client has been notified of the assigned rider and an estimated pickup time.

### Main Success Scenario
1. The Sender Client opens the app and enters the pickup location, drop-off location, and package details.
2. The system validates the entered addresses and package details.
3. The system searches for active Delivery Riders within a 3 km radius of the pickup location *(«include» Match Nearest Rider)*.
4. The system identifies the nearest available rider based on GPS proximity and current workload.
5. The system assigns the request to the identified rider and generates a unique OTP for delivery confirmation.
6. The system sends a dispatch notification — pickup location and package details — to the assigned Delivery Rider.
7. The Delivery Rider accepts the dispatch within the app.
8. The system updates the order status to `Assigned` and notifies the Sender Client with the rider's details and ETA.

### Alternate Flow — A1: No Rider Available Within Radius
*Triggered at Step 3/4 if no active rider is found within the 3 km radius.*

1. A1.1 — The system incrementally expands the search radius (e.g., 3 km → 5 km → 8 km) up to a defined maximum.
2. A1.2 — If no rider is found even at the maximum radius, the system places the request into a pending queue and notifies the Sender Client of the delay along with an estimated wait time.
3. A1.3 — Once a rider becomes available within range, the flow resumes at Main Success Scenario Step 4.

### Exception Flow — E1: Invalid Address Input
*Triggered at Step 2 if address validation fails.*

1. E1.1 — The system displays an error message identifying the invalid field.
2. E1.2 — The Sender Client corrects the input and resubmits; flow resumes at Step 1.

### Business Rules
- BR-1: A rider marked "Offline" (FR-005) is never eligible for matching, regardless of distance.
- BR-2: The OTP generated in Step 5 is single-use and tied to this order only.

### Frequency of Use
High — this is the primary entry-point use case, expected to be triggered on every new order.
