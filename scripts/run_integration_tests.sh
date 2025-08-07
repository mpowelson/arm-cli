#!/bin/bash
set -e

echo "==> Allowing X11 access..."
xhost +local:docker || true

echo "==> Building integration Docker image..."
docker build -t arm-cli-integration ./tests/integration

echo "==> Running integration tests..."
docker run --rm -it \
  --privileged \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  arm-cli-integration
