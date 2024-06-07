#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <place-query>"
    exit 1
fi

PLACE_QUERY=$1

if ! command -v ffmpeg &>/dev/null; then
    echo "ffmpeg could not be found, please install it from https://ffmpeg.org/download.html"
    exit 1
fi

./.venv/bin/python dijkstra.py "$PLACE_QUERY"

if [ ! -f coordinates.csv ]; then
    echo "coordinates.csv not found. Ensure dijkstra.py ran successfully."
    exit 1
fi

./.venv/bin/python animation.py

if [ ! -f animation.mp4 ]; then
    echo "animation.mp4 not found. Ensure animation.py ran successfully."
    exit 1
fi

echo "Dijkstra's pathfinding and animation complete. The animation is saved as animation.mp4."
