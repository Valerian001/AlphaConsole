#!/bin/bash
# AgentOps Vast.ai Provisioning & Setup Script (Draft)

INSTANCE_ID=$(vastai create instance "$1" --image agentops/worker-base:latest --onstart "bash /root/bootstrap.sh" --raw | jq -r '.instance_id')

echo "Instance $INSTANCE_ID provisioned. Waiting for initialization..."

# Poll for readiness
while true; do
    STATUS=$(vastai show instances --raw | jq -r ".[] | select(.id == $INSTANCE_ID) | .actual_status")
    if [ "$STATUS" == "running" ]; then
        echo "Instance is running. Triggering setup..."
        break
    fi
    sleep 10
done

# In a real scenario, the instance would self-initialize.
# This script would then wait for the 'objective.complete' signal from NATS.
