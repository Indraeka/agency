#!/bin/bash
# Lottery Analyst launcher for macOS / Linux: double-click to start.
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "Python 3 is not installed. Get it from https://www.python.org/downloads/ and run this again."
  read -r -p "Press Enter to close."; exit 1
fi
"$PY" -c "import numpy" 2>/dev/null || "$PY" -m pip install --user numpy || {
  echo "Could not install numpy. Run:  $PY -m pip install numpy"
  read -r -p "Press Enter to close."; exit 1
}
"$PY" app.py
