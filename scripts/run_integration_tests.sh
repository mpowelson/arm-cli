#!/bin/bash
set -e

echo "==> Allowing X11 access..."
xhost +local:docker || true

echo "==> Building integration Docker image..."
docker build -t arm-cli-integration -f ./tests/integration/Dockerfile .

echo "==> Running integration tests..."
docker run --rm -it \
  --privileged \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /var/run/docker.sock:/var/run/docker.sock \
  arm-cli-integration
