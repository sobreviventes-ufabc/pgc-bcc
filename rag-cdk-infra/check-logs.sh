#!/bin/bash

# Script to check latest Lambda logs
LOG_GROUP="/aws/lambda/RagCdkInfraStack-ApiFunc9527395A-CbVbFfQfMSzf"

# Get the latest log stream
LATEST_STREAM=$(aws logs describe-log-streams \
  --log-group-name "$LOG_GROUP" \
  --order-by LastEventTime --descending --max-items 1 \
  --query 'logStreams[0].logStreamName' --output text)

echo "Checking logs from stream: $LATEST_STREAM"
echo "----------------------------------------"

# Get logs from the last 10 minutes
START_TIME=$(date -d '10 minutes ago' +%s)000

aws logs get-log-events \
  --log-group-name "$LOG_GROUP" \
  --log-stream-name "$LATEST_STREAM" \
  --start-time "$START_TIME" \
  --query 'events[*].message' --output text