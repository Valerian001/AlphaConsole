#!/bin/bash
set -e

echo "Starting AlphaConsole Worker Bootstrap..."

# 1. System Updates & Dependencies
apt-get update && apt-get install -y \
    curl \
    git \
    docker.io \
    python3-pip \
    jq

# 2. Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && apt-get update \
  && apt-get install -y nvidia-container-toolkit

# 3. Configure Docker for NVIDIA
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker

# 4. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 5. Download AgentOps Go Runtime (Placeholder for binary download)
# curl -L https://github.com/alphaconsole/worker-runtime/releases/latest/download/runtime-linux-amd64 -o /usr/local/bin/agentops-runtime
# chmod +x /usr/local/bin/agentops-runtime

# 6. Initialize System (Docker Compose stack)
mkdir -p /opt/alphaconsole/worker
cat <<EOF > /opt/alphaconsole/worker/docker-compose.yml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports: ["6333:6333"]
    volumes: ["/opt/alphaconsole/qdrant:/qdrant/storage"]
EOF

# 7. Start Services
cd /opt/alphaconsole/worker && docker-compose up -d

echo "AlphaConsole Worker Ready."
