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
docker run --rm hello-world

echo "[✓] Running GUI test (xeyes)..."
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix x11-apps xeyes &
sleep 5
kill %1 || true

echo "[✓] All checks passed."
