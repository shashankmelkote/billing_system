# Billing System

A serverless billing report system using AWS Lambda, SAM, and DynamoDB.

Deployed via GitHub Actions 🚀


## Running Tests

Install the application and test dependencies (including boto3 for integration tests), then run `pytest`:

```bash
pip install -r src/requirements.txt -r requirements-test.txt
pytest
```

To generate an HTML coverage report, run:

```bash
coverage html
```

The report will be available in the `htmlcov` directory.

GitHub Actions automatically runs all unit and integration tests on every commit so you can be confident in code quality.

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
   pip install -r src/requirements.txt -r requirements-test.txt pytest coverage
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

## Development with GitHub Codespaces

If you prefer a preconfigured cloud environment, this repository includes a
`.devcontainer` that works with [GitHub Codespaces](https://github.com/features/codespaces).

1. On GitHub, click the **Code** dropdown and choose **Codespaces**.
2. Select **Create codespace on main** (or your branch) to start a new instance.
3. The container will be built automatically and run the `postCreateCommand.sh`
   script to install the AWS SAM CLI and configure the AWS CLI using your
   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` codespace secrets.
4. Once the codespace is running, install Python dependencies and run the tests:

   ```bash
   pip install -r src/requirements.txt -r requirements-test.txt
   pytest
   ```

5. To try the API from the codespace, run:

   ```bash
   sam build
   sam local start-api
   ```

   The forwarded port will expose the service at `http://127.0.0.1:3000`.

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

## Infrastructure as Code

All AWS resources for the billing system are defined in `template.yaml`. To
allow GitHub Actions to deploy the stack, an IAM role is provided in
`deploy_role.yaml`. Deploy the role once per AWS account and store the resulting
ARN in the `AWS_ROLE_TO_ASSUME` GitHub secret:

```bash
aws cloudformation deploy \
  --template-file deploy_role.yaml \
  --stack-name github-actions-role \
  --parameter-overrides GitHubRepo=<your-org>/<your-repo> \
  --capabilities CAPABILITY_NAMED_IAM
```

After the role exists, simply run `sam deploy` (or push to `main`) to recreate
the rest of the infrastructure.

## Contributing

We welcome contributions! After setting up your environment:

1. Create a new branch for your feature or fix.
2. Run `pytest` to ensure tests pass.
3. Open a pull request describing your changes.
