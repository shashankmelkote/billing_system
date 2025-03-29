import json
from database import DatabaseManager
from reports import ReportGenerator

db_manager = DatabaseManager()
report_generator = ReportGenerator(db_manager)

def lambda_handler(event, context):
    path = event.get("path")
    method = event.get("httpMethod")

    if method == "POST" and path == "/add_record":
        return add_record(event)

    if method == "GET":
        if path == "/reports/outstanding_billables":
            return generate_response(report_generator.outstanding_billables())
        elif path == "/reports/unpaid_patients":
            return generate_response(report_generator.unpaid_patients())
        elif path == "/reports/revenue_per_month":
            return generate_response(report_generator.revenue_per_month())
        elif path == "/reports/top_insurance_providers":
            return generate_response(report_generator.top_insurance_providers())

    return generate_response({"error": "Invalid request"}, status=400)

def add_record(event):
    data = json.loads(event["body"])
    record_id = db_manager.add_record(data)
    return generate_response({"message": "Record added successfully!", "RecordID": record_id})

def generate_response(body, status=200):
    return {
        "statusCode": status,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"}
    }