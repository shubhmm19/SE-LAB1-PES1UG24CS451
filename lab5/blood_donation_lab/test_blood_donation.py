"""Unit tests for blood_donation.py (run: python -m unittest)."""

import unittest
from datetime import date, timedelta

import blood_donation as bd


class BloodDonationTests(unittest.TestCase):
    """Basic behaviour checks."""

    def setUp(self):
        bd.DONORS.clear()
        for group in bd.STOCK:
            bd.STOCK[group] = 0

    def test_age_limits(self):
        self.assertFalse(bd.register_donor("Young", "O+", 17))
        self.assertFalse(bd.register_donor("Old", "O+", 66))
        self.assertTrue(bd.register_donor("Ok", "O+", 30))

    def test_unknown_group_raises(self):
        with self.assertRaises(ValueError):
            bd.register_donor("X", "Z+", 30)

    def test_ninety_day_gap(self):
        recent = date.today() - timedelta(days=30)
        bd.register_donor("Priya", "A+", 30, recent)
        self.assertFalse(bd.record_donation("Priya"))

    def test_record_and_units(self):
        bd.register_donor("Arjun", "O-", 25)
        self.assertTrue(bd.record_donation("Arjun", 2))
        self.assertEqual(bd.units_for("AB-"), 2)
        self.assertEqual(bd.units_for("Z+"), 0)

    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            bd.record_donation("Nobody", 0)

    def test_universal_and_low_stock(self):
        self.assertTrue(bd.is_universal("O-"))
        self.assertFalse(bd.is_universal("A+"))
        self.assertEqual(len(bd.low_stock()), 8)

    def test_notify_rejects_bad_number(self):
        with self.assertRaises(ValueError):
            bd.notify_donors(["123; rm -rf ~"])


if __name__ == "__main__":
    unittest.main()
