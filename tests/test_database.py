import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from unittest.mock import MagicMock, patch

import database
from database import DatabaseManager


def test_add_record_puts_item_and_returns_id():
    table_mock = MagicMock()
    with patch.object(database, "boto3") as mock_boto3, \
         patch.object(database.uuid, "uuid4", return_value="test-id"):
        mock_boto3.resource.return_value.Table.return_value = table_mock
        db = DatabaseManager(table_name="tbl")
        record = {"PatientName": "Alice"}
        record_id = db.add_record(record.copy())

    table_mock.put_item.assert_called_once()
    item = table_mock.put_item.call_args.kwargs["Item"]
    assert item["PatientName"] == "Alice"
    assert item["RecordID"] == "test-id"
    assert record_id == "test-id"


def test_fetch_all_records_scans_table():
    table_mock = MagicMock()
    table_mock.scan.return_value = {"Items": [{"foo": "bar"}]}
    with patch.object(database, "boto3") as mock_boto3:
        mock_boto3.resource.return_value.Table.return_value = table_mock
        db = DatabaseManager(table_name="tbl")
        records = db.fetch_all_records()

    table_mock.scan.assert_called_once()
    assert records == [{"foo": "bar"}]
