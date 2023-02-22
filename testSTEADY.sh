#!/bin/bash

cluster="ecs-ec2"
service="scaling-replication"
desired_status="STEADY_STATE"

while true; do
  # Run the command and capture the output
  output=$(aws ecs describe-services --cluster "$cluster" --services "$service" | jq -r '.services[].taskSets[].stabilityStatus')

  # Check if the status is what we want
  if [ "$output" = "$desired_status" ]; then
    echo "Service is in STEADY_STATE, exiting loop."
    break
  else
    echo "Service is not in STEADY_STATE, waiting 15 seconds and trying 
again..."
    sleep 15
  fi
done

