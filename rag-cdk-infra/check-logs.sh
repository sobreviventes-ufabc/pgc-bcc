#!/bin/bash

# Script to check latest Lambda logs
LOG_GROUP="/aws/lambda/RagCdkInfraStack-ApiFunc9527395A-CbVbFfQfMSzf"

echo "Fetching logs from: $LOG_GROUP"
echo "Last 10 minutes of logs:"
echo "----------------------------------------"

# Use aws logs tail with --since flag for last 10 minutes
aws logs tail "$LOG_GROUP" --since 10m --format short