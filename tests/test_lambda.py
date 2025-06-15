import os, sys, json, importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from unittest.mock import MagicMock, patch


def load_lambda_with_stubs(db_stub, report_stub):
    """Reload lambda_function with boto3 mocked and global stubs injected."""
    with patch("database.boto3.resource") as mock_resource:
        mock_resource.return_value.Table.return_value = MagicMock()
        module = importlib.import_module("lambda_function")
        importlib.reload(module)
        module.db_manager = db_stub
        module.report_generator = report_stub
        return module


class StubDB:
    def __init__(self, record_id="123"):
        self.record_id = record_id
        self.add_record = MagicMock(return_value=record_id)


class StubReport:
    def __init__(self, data):
        self._data = data

    def outstanding_billables(self):
        return self._data


def test_lambda_handler_routes_to_report():
    stub_report = StubReport({"ok": True})
    module = load_lambda_with_stubs(StubDB(), stub_report)
    event = {"httpMethod": "GET", "path": "/reports/outstanding_billables"}
    resp = module.lambda_handler(event, None)
    assert json.loads(resp["body"]) == {"ok": True}
    assert resp["statusCode"] == 200


def test_lambda_add_record_uses_db_stub():
    db = StubDB(record_id="abc")
    module = load_lambda_with_stubs(db, StubReport({}))
    event = {
        "httpMethod": "POST",
        "path": "/add_record",
        "body": json.dumps({"foo": "bar"}),
    }
    resp = module.lambda_handler(event, None)
    db.add_record.assert_called_once_with({"foo": "bar"})
    body = json.loads(resp["body"])
    assert body == {"message": "Record added successfully!", "RecordID": "abc"}
    assert resp["statusCode"] == 200
