"""Fuzzing target: booking, baggage-weight and passenger-tag input handling."""

import math
import re


def parse_booking(code):
    if not isinstance(code, str):
        raise ValueError("booking code must be text")
    match = re.fullmatch(r"\s*([A-Za-z]{2})-(\d{1,4})-(\d{1,3})([A-Za-z])\s*", code)
    if not match:
        raise ValueError("booking code must look like AI-203-12A")
    airline, flight, _seat_number, seat_letter = match.groups()
    flight_number = int(flight)
    if flight_number <= 0:
        raise ValueError("flight number must be positive")
    return airline.upper(), flight_number, seat_letter.upper()


def total_weight(weights_csv):
    if not isinstance(weights_csv, str):
        raise ValueError("weights must be supplied as CSV text")
    fields = weights_csv.split(",")
    if not fields or any(not field.strip() for field in fields):
        raise ValueError("weight list cannot contain empty values")
    weights = []
    for field in fields:
        try:
            value = float(field.strip())
        except (TypeError, ValueError) as exc:
            raise ValueError("each weight must be numeric") from exc
        if not math.isfinite(value) or value < 0:
            raise ValueError("weights must be finite and non-negative")
        weights.append(value)
    return sum(weights)


def tag_label(name):
    if not isinstance(name, str):
        raise ValueError("passenger name must be text")
    parts = name.split()
    if len(parts) < 2 or not parts[0].isalpha() or not parts[-1].isalpha():
        raise ValueError("passenger name must contain alphabetic first and last names")
    return parts[0][0].upper() + ". " + parts[-1].upper()


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    try:
        result = parse_booking(user_input)
        print("Airline, Flight and Seat Letter:", result)
    except ValueError as exc:
        print("Invalid booking code:", exc)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    try:
        result = total_weight(user_input)
        print("Total Weight:", result)
    except ValueError as exc:
        print("Invalid bag weights:", exc)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    try:
        result = tag_label(user_input)
        print("Tag Label:", result)
    except ValueError as exc:
        print("Invalid passenger name:", exc)


if __name__ == "__main__":
    main()
