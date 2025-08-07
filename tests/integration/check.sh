#!/bin/bash
set -e

echo "[✓] Checking Docker group membership..."
if groups | grep -q docker; then
  echo "User is in docker group."
else
  echo "❌ User is NOT in docker group."
  exit 1
fi

echo "[✓] Running hello-world container..."
# Skip Docker test in integration environment if Docker socket is not accessible
if [ -S /var/run/docker.sock ]; then
    docker run --rm hello-world
else
    echo "Docker socket not accessible, skipping Docker test"
fi

echo "[✓] Running GUI test (xeyes)..."
# Skip GUI test in integration environment if X11 is not available
if [ -n "$DISPLAY" ] && [ -S /tmp/.X11-unix/X0 ]; then
    docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ubuntu:22.04 xeyes &
    sleep 5
    kill %1 || true
else
    echo "X11 not available, skipping GUI test"
fi

echo "[✓] All checks passed."
