#!/bin/bash

# Initialize variables with default values
mode=""

# Function to display usage information
usage() {
  echo "Usage: $0 -m <mode> -s <size>"
  echo "Options:"
  echo "  -m Specify the mode (client or server)"
  exit 1
}


# Parse command-line options using getopts
while getopts ":m:s:" opt; do
  case $opt in
    m)
      mode="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument."
      usage
      ;;
  esac
done

# Check if the mode is not empty and execute the appropriate Python script
if [ -n "$mode" ]; then
  case "$mode" in
    client)
      python client.py
      ;;
    server)
      python server.py
      ;;
    *)
      echo "Invalid mode. Use 'client' or 'server'."
      usage
      ;;
  esac
else
  echo "Mode option (-m) is required."
  usage
fi