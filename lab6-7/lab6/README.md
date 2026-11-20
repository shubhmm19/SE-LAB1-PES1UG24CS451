# Lab 6 — Airline Baggage Coverage

This folder contains a local copy of the assigned baggage-fee application and
two focused pytest suites. The application is intentionally kept as provided
so the coverage tests measure its original decisions.

Install `requirements.txt`, then run from this directory:

```sh
coverage run --source=airline_baggage -m pytest -q CodeCoverageTest_airline_baggage.py
coverage report -m
coverage erase
coverage run --branch --source=airline_baggage -m pytest -q BranchCoverageTest_airline_baggage.py
coverage report -m
```

The two test files use the comprehensive boundary cases; the branch-named suite
is intended for the separate branch measurement. Keep the terminal output from
each successful `coverage report -m` for the handout screenshots.

Captured outputs and the two-page screenshot PDF are in `results/`.
