#!/bin/bash

set -e

echo "🛠️  Setting up AWS SAM dev environment..."

# Install AWS SAM CLI
echo "🔧 Installing AWS SAM CLI..."
curl -Lo sam.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip sam.zip -d sam-install
sudo ./sam-install/install

# Configure AWS CLI with environment-provided secrets (from Codespaces)
echo "🔐 Configuring AWS CLI with Codespaces secrets..."
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "us-east-1"

# Clean up install files
rm -rf sam.zip sam-install

echo "✅ SAM CLI and AWS CLI are ready!"