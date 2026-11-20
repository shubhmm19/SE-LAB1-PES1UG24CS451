# Lab 7 — Airline Baggage Fuzz Testing

`airline_baggage.py` hardens the three functions from the assigned Lab 7
starter: `parse_booking`, `total_weight`, and `tag_label`. Malformed or
out-of-domain values now fail with a clear `ValueError`; the interactive entry
point catches those validation errors and continues to the next prompt.

Install dependencies from `requirements.txt`, then run from this directory:

```sh
python3 airline_baggage.py
python3 -m pytest -q test_airline_baggage.py
```

The property tests use Hypothesis to generate arbitrary text and `None` values,
plus generated valid booking codes, weight lists, and passenger names. The
valid-input properties verify the returned shape and result. Keep the initial
failing output from testing the unmodified starter and the passing output from
this fixed version for the handout PDF. Captured outputs, original starter,
rendered terminal captures, and the screenshot PDF are in `results/`.
