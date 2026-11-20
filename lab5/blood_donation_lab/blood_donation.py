"""Blood Donation Management System.

A small donor register for a blood bank. It registers donors after an age
check, decides who may donate again (90-day gap), records donations into
blood-group stock and works out how many compatible units are available
for a patient.
"""

import logging
import os
import re
import subprocess
import tempfile
from datetime import date, timedelta

LOGGER = logging.getLogger(__name__)

# The officer password is no longer hard-coded in the source. If it is ever
# needed, supply it through the environment (never commit secrets to Git).
OFFICER_PASSWORD = os.environ.get("BLOODBANK_OFFICER_PASSWORD")

MIN_AGE = 18
MAX_AGE = 65
DONATION_GAP_DAYS = 90
PHONE_PATTERN = re.compile(r"^\+?[0-9]{7,15}$")

DONORS = []

STOCK = {"A+": 0, "A-": 0, "B+": 0, "B-": 0,
         "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}

# Which donor groups can safely give to each patient group.
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(STOCK),
    "AB-": ["A-", "B-", "O-", "AB-"],
}


def register_donor(donor_name, blood_group, age, last_donation=None):
    """Register a donor after validating blood group and age.

    Returns True when the donor was registered and False when the donor is
    outside the allowed age range. Raises ValueError for an unknown group.
    """
    if blood_group not in STOCK:
        raise ValueError(f"Unknown blood group: {blood_group}")
    if age < MIN_AGE or age > MAX_AGE:
        LOGGER.info("%s is not eligible because of age", donor_name)
        return False
    DONORS.append({"name": donor_name, "group": blood_group,
                   "last": last_donation})
    return True


def can_donate(donor):
    """Return True if the donor has never donated or waited 90+ days."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=DONATION_GAP_DAYS)


def record_donation(donor_name, units=1):
    """Add units to stock for an eligible, registered donor."""
    if units <= 0:
        raise ValueError("units must be a positive number")
    for donor in DONORS:
        if donor["name"] == donor_name and can_donate(donor):
            STOCK[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Return the number of compatible units in stock for a patient group."""
    return sum(STOCK[group] for group in COMPATIBLE.get(patient_group, []))


def is_universal(blood_group):
    """Return True for O- (universal donor) and AB+ (universal recipient)."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """Return the blood groups whose stock is below the threshold."""
    return [group for group, units in STOCK.items() if units < threshold]


def donor_sheet_path():
    """Create a private temporary CSV file and return its path."""
    # Helper kept for the lab: not called by the demo
    # mkstemp creates the file atomically with safe permissions, unlike
    # the insecure, race-prone tempfile.mktemp.
    file_descriptor, path = tempfile.mkstemp(suffix=".csv")
    os.close(file_descriptor)
    return path


def notify_donors(phone_list):
    """Send an SMS to each valid phone number using the send-sms tool."""
    # Helper kept for the lab: not called by the demo
    for phone in phone_list:
        if not PHONE_PATTERN.match(phone):
            raise ValueError(f"Invalid phone number: {phone}")
    # An argument list with no shell prevents command injection.
    subprocess.run(["send-sms", *phone_list], check=True, shell=False)


def main():
    """Run a short demonstration of the system."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", STOCK)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())  # below 2 units
    eligible = [donor["name"] for donor in DONORS if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
