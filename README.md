# Billing System

A serverless billing report system using AWS Lambda, SAM, and DynamoDB.

Deployed via GitHub Actions 🚀


## Running Tests

Install dependencies from `src/requirements.txt` and run `pytest`:

```bash
pip install -r src/requirements.txt
pytest
```

To generate an HTML coverage report, run:

```bash
coverage html
```

The report will be available in the `htmlcov` directory.

## Local Development

1. Clone this repository and create a Python 3.9 virtual environment:

   ```bash
   git clone <your-fork-url>
   cd billing_system
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies and development tools:

   ```bash
   pip install -r src/requirements.txt pytest coverage
   ```

3. Run the unit tests to verify everything is set up correctly:

   ```bash
   pytest
   ```

4. If you plan to run the API locally, install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) and start the local API:

   ```bash
   sam build
   sam local start-api
   ```

   The service will be available at `http://127.0.0.1:3000`.

## Manual End-to-End Testing with Postman

1. Ensure the local API is running (`sam local start-api`).
2. In Postman, create a new request:
   - **Method:** `POST`
   - **URL:** `http://127.0.0.1:3000/add_record`
   - **Headers:** `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "PatientName": "John Doe",
       "DateOfVisit": "2025-03-27",
       "Clinician": "Dr. Alice",
       "Insurance": "Aetna",
       "DateClaimSubmitted": "2025-03-28",
       "DateClaimApproved": "2025-03-30",
       "AmountBilled": 200,
       "AmountPaid": 100
     }
     ```

   Send the request and verify the success message with the generated `RecordID`.

3. Use additional `GET` requests to test the reports:
   - `http://127.0.0.1:3000/reports/outstanding_billables`
   - `http://127.0.0.1:3000/reports/unpaid_patients`
   - `http://127.0.0.1:3000/reports/revenue_per_month`
   - `http://127.0.0.1:3000/reports/top_insurance_providers`

## Contributing

We welcome contributions! After setting up your environment:

1. Create a new branch for your feature or fix.
2. Run `pytest` to ensure tests pass.
3. Open a pull request describing your changes.
