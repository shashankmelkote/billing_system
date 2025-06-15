import os
import sys
import json
import importlib

import boto3
from moto import mock_aws

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@mock_aws
def test_add_record_and_query_outstanding():
    table_name = "BillingRecords"
    os.environ["TABLE_NAME"] = table_name

    dynamodb = boto3.client("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "RecordID", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "RecordID", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    import lambda_function
    importlib.reload(lambda_function)

    record = {
        "PatientName": "John Doe",
        "DateOfVisit": "2025-03-27",
        "Clinician": "Dr. Alice",
        "Insurance": "Aetna",
        "DateClaimSubmitted": "2025-03-28",
        "DateClaimApproved": "2025-03-30",
        "AmountBilled": 200,
        "AmountPaid": 100,
    }

    add_event = {"httpMethod": "POST", "path": "/add_record", "body": json.dumps(record)}
    add_resp = lambda_function.lambda_handler(add_event, None)
    assert add_resp["statusCode"] == 200

    report_event = {"httpMethod": "GET", "path": "/reports/outstanding_billables"}
    report_resp = lambda_function.lambda_handler(report_event, None)
    assert report_resp["statusCode"] == 200
    assert json.loads(report_resp["body"]) == {"Total Outstanding Billables": "$100.00"}
