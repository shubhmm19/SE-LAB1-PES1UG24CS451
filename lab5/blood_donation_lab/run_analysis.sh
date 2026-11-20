#!/usr/bin/env bash
# Installs the tools and saves the three reports for the lab.
set -e
python -m pip install pylint bandit flake8
python -m pylint blood_donation.py > pylint_report.txt || true
python -m bandit -r blood_donation.py > bandit_report.txt || true
python -m flake8 blood_donation.py > flake8_report.txt || true
echo "Reports written: pylint_report.txt bandit_report.txt flake8_report.txt"
