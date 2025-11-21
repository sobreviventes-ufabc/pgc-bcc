#!/bin/bash

# Script to tail Lambda logs using AWS CLI
LOG_GROUP="/aws/lambda/RagCdkInfraStack-ApiFunc9527395A-CbVbFfQfMSzf"

echo "Tailing logs from: $LOG_GROUP"
echo "Press Ctrl+C to stop"
echo "----------------------------------------"

# Tail logs in real-time
aws logs tail "$LOG_GROUP" --follow --format short
