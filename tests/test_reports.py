import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest

from reports import ReportGenerator


class StubDBManager:
    def __init__(self, records):
        self._records = records

    def fetch_all_records(self):
        return self._records


def test_unpaid_patients_filters_out_paid_records():
    records = [
        {
            "PatientName": "Alice",
            "AmountBilled": "100",
            "AmountPaid": "50",
        },
        {
            "PatientName": "Bob",
            "AmountBilled": "200",
            "AmountPaid": "200",
        },
        {
            "PatientName": "Charlie",
            "AmountBilled": "150",
            "AmountPaid": "0",
        },
    ]
    rg = ReportGenerator(StubDBManager(records))
    result = rg.unpaid_patients()

    expected = [
        {"PatientName": "Alice", "Outstanding": 50.0},
        {"PatientName": "Charlie", "Outstanding": 150.0},
    ]
    assert result == expected
