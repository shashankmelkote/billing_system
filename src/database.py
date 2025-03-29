import boto3
import uuid
import os

class DatabaseManager:
    def __init__(self, table_name=None, region="us-east-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table_name = table_name or os.getenv("TABLE_NAME", "BillingRecords")
        self.table = self.dynamodb.Table(self.table_name)

    def add_record(self, record):
        record["RecordID"] = str(uuid.uuid4())
        self.table.put_item(Item=record)
        return record["RecordID"]

    def fetch_all_records(self):
        response = self.table.scan()
        return response.get("Items", [])