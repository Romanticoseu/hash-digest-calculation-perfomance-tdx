#!/bin/bash

# Check if a single argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <size (e.g., 1kb, 50kb, 100kb, 1mb, 10mb)>"
    exit 1
fi

# Extract the size and unit from the argument
input_size="$1"
unit="${input_size: -2}"
size="${input_size:0: -2}"

# Define the size in bytes based on the unit
case "$unit" in
    kb)
        size_bytes=$((size * 1024))
        ;;
    mb)
        size_bytes=$((size * 1024 * 1024))
        ;;
    *)
        echo "Invalid unit. Use 'kb' or 'mb'."
        exit 1
        ;;
esac

# Generate a random filename based on the specified size
filename="${1}.txt"

# Generate the file with random content
tr -dc "A-Za-z0-9" < /dev/urandom | fold -w 100 | head -c "$size_bytes" > "$filename"

echo "File $filename generated with size $input_size."
