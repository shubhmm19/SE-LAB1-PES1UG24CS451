"""Property-based edge-case tests for the hardened Lab 7 functions."""
import math

from hypothesis import given, strategies as st
import pytest

from airline_baggage import parse_booking, tag_label, total_weight


@given(st.one_of(st.text(), st.none()))
def test_parse_booking_never_crashes(s):
    try:
        result = parse_booking(s)
    except ValueError:
        return
    assert isinstance(result, tuple) and len(result) == 3
    airline, flight, seat = result
    assert airline.isalpha() and airline.isupper() and len(airline) == 2
    assert isinstance(flight, int) and flight > 0
    assert seat.isalpha() and seat.isupper() and len(seat) == 1


@given(st.one_of(st.text(), st.none()))
def test_total_weight_never_crashes(s):
    try:
        result = total_weight(s)
    except ValueError:
        return
    assert math.isfinite(result) and result >= 0


@given(st.one_of(st.text(), st.none()))
def test_tag_label_never_crashes(s):
    try:
        result = tag_label(s)
    except ValueError:
        return
    assert isinstance(result, str) and result.startswith(".") is False
    assert result == result.upper()


@given(st.integers(min_value=1, max_value=9999), st.integers(min_value=1, max_value=999))
def test_valid_booking_round_trip(flight, seat_number):
    assert parse_booking(f"ai-{flight}-{seat_number}b") == ("AI", flight, "B")


@given(st.lists(st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False), min_size=1, max_size=20))
def test_valid_weight_csv_sums(values):
    csv = ",".join(map(str, values))
    assert math.isclose(total_weight(csv), sum(values), rel_tol=1e-12, abs_tol=1e-9)


@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1))
def test_valid_passenger_names(first, last):
    assert tag_label(first + " " + last) == first[0].upper() + ". " + last.upper()


@pytest.mark.parametrize("value", ["", "AI-0-12A", "AI-12-A", "A-12-1A", "AI-x-12A", "AI-12-12AA"])
def test_invalid_booking_is_rejected(value):
    with pytest.raises(ValueError):
        parse_booking(value)


@pytest.mark.parametrize("value", ["", "1,,2", "one,2", "-1", "nan", "inf"])
def test_invalid_weights_are_rejected(value):
    with pytest.raises(ValueError):
        total_weight(value)


@pytest.mark.parametrize("value", ["", "Madonna", "John 123", "123 Smith"])
def test_invalid_names_are_rejected(value):
    with pytest.raises(ValueError):
        tag_label(value)
