# Bug Reports — Hyperlocal Courier Dispatch & Tracking Engine

> Sample bug-tracking records prepared from Lab 1 requirements. They are
> examples for entry into Jira and are not defects verified in a running app.

## HCDE-1 — Offline rider appears in dispatch results

- **Type:** Bug
- **Priority / severity:** Highest / Critical
- **Status:** To Do
- **Component:** Dispatch Matching
- **Requirement:** FR-001, FR-005
- **Description:** The matcher can return an offline rider when that rider is
  closest to the pickup point.
- **Preconditions:** Rider A is Offline and 0.5 km from pickup. Rider B is
  Online and 1.2 km from pickup.
- **Steps to reproduce:** 1. Create a delivery request at the pickup point.
  2. Run rider matching. 3. Inspect the assigned rider.
- **Expected:** Rider B is selected; offline riders are excluded.
- **Actual:** Rider A can be selected because the availability state is not
  applied to the candidate query.
- **Acceptance for fix:** Only online riders within 3 km are eligible; choose
  the nearest eligible rider.

## HCDE-2 — Expired OTP can complete delivery

- **Type:** Bug
- **Priority / severity:** Highest / Critical
- **Status:** In Progress
- **Component:** Proof of Delivery
- **Requirement:** FR-003
- **Description:** An expired one-time password may still be accepted by the
  delivery verification endpoint.
- **Preconditions:** A dispatched order has an OTP whose validity period has
  elapsed.
- **Steps to reproduce:** 1. Open the rider delivery screen. 2. Enter the
  expired OTP. 3. Submit verification.
- **Expected:** Reject the expired code and keep the order out of Delivered.
- **Actual:** The order may be marked Delivered if only the code value is
  checked.
- **Acceptance for fix:** Validate expiry, single use, and attempt limit before
  changing the order state.

## HCDE-3 — Sender status notification arrives after the five-second target

- **Type:** Bug
- **Priority / severity:** High / Major
- **Status:** Done
- **Component:** Notifications
- **Requirement:** FR-004
- **Description:** A sender receives a status update later than the requirement
  target after a delivery state changes.
- **Preconditions:** Sender is subscribed to an active order's updates.
- **Steps to reproduce:** 1. Change the order to Picked Up. 2. Record the
  backend transition and notification delivery timestamps.
- **Expected:** Notification arrives within 5 seconds.
- **Actual:** The sample scenario records a 9-second delay when the push queue
  is retried.
- **Resolution note:** Simulated fix batches retries without delaying the first
  push attempt; verify with an integration timing test.

## HCDE-4 — Availability toggle takes longer than two seconds to affect matching

- **Type:** Bug
- **Priority / severity:** Medium / Major
- **Status:** To Do
- **Component:** Rider Availability
- **Requirement:** FR-005
- **Description:** The rider UI shows Offline, but the dispatch cache continues
  treating the rider as Online beyond the two-second propagation target.
- **Preconditions:** Rider is Online and eligible for dispatch.
- **Steps to reproduce:** 1. Toggle the rider to Offline. 2. Submit a nearby
  delivery request within two seconds. 3. Inspect dispatch candidates.
- **Expected:** The status change takes effect within 2 seconds and the rider
  is excluded.
- **Actual:** A stale cache entry can keep the rider eligible.
- **Acceptance for fix:** Invalidate or update dispatch eligibility as part of
  the availability state change.

## HCDE-5 — Multi-stop route is longer than the assignment-order route

- **Type:** Bug
- **Priority / severity:** Medium / Major
- **Status:** Done
- **Component:** Route Optimization
- **Requirement:** FR-002
- **Description:** The route optimizer returns a stop sequence whose distance
  is greater than the naive assignment-order sequence.
- **Preconditions:** Rider has three active stops with known route distances.
- **Steps to reproduce:** 1. Add the three stops in a deliberately inefficient
  order. 2. Request an optimized route. 3. Compare its distance to the input
  order.
- **Expected:** Return a sequence no longer than the naive route within the
  3-second target.
- **Actual:** The sample scenario returns a longer sequence when one stop is
  omitted from the optimization set.
- **Resolution note:** Simulated fix includes all active stops in the candidate
  route and checks total distance before returning it.
