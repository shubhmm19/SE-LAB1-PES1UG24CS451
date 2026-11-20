import pytest

from airline_baggage import baggage_fee, carry_on_ok, check_in_status


@pytest.mark.parametrize("cabin,allowance", [("economy", 15), ("premium", 25), ("business", 40)])
def test_allowance_boundary(cabin, allowance):
    assert baggage_fee(cabin, allowance, "domestic", False) == 0
    assert baggage_fee(cabin, allowance + 1, "domestic", False) == 20


@pytest.mark.parametrize("cabin,expected", [("economy", 25), ("premium", 35), ("business", 40)])
def test_member_allowance(cabin, expected):
    assert baggage_fee(cabin, expected, "domestic", True) == 0
    assert baggage_fee(cabin, expected + 1, "domestic", True) == 20


def test_unknown_cabin_and_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("first", 10, "domestic", False)
    with pytest.raises(ValueError):
        baggage_fee("economy", -0.1, "domestic", False)


def test_route_and_high_excess_rates():
    assert baggage_fee("economy", 20, "domestic", False) == 100
    assert baggage_fee("economy", 36, "domestic", False) == 840
    assert baggage_fee("economy", 36, "international", False) == 2100
    # Unknown routes intentionally follow the non-domestic base rate.
    assert baggage_fee("economy", 16, "unknown", False) == 45


def test_carry_on_all_paths():
    assert carry_on_ok(100, 2, True) is True
    assert carry_on_ok(100, 3, True) is False
    assert carry_on_ok(8, 0, False) is False
    assert carry_on_ok(7, 1, False) is True
    assert carry_on_ok(7, 2, False) is False


@pytest.mark.parametrize("has_baggage,international,cutoff", [
    (True, False, 60), (False, False, 45),
    (True, True, 120), (False, True, 105),
])
def test_check_in_open_late_closed_boundaries(has_baggage, international, cutoff):
    assert check_in_status(cutoff, has_baggage, international) == "open"
    assert check_in_status(cutoff - 1, has_baggage, international) == "late"
    assert check_in_status(cutoff - 15, has_baggage, international) == "late"
    assert check_in_status(cutoff - 16, has_baggage, international) == "closed"
