#!/bin/bash

if [ "$1" == "a" ]; then
  exec python /app/process_a.py
elif [ "$1" == "b" ]; then
  exec python /app/process_b.py
else
  echo "Invalid process specified. Please use 'process_a' or 'process_b'."
  exit 1
fi
