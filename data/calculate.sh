#!/bin/bash

# Remove any existing hash_digest file
rm -f hash_digest.txt

# Iterate through all .txt files in the current directory
for file in *.txt; do
    # Calculate the SHA-256 hash
    hash=$(sha256sum "$file" | awk '{print $1}')
    
    # Extract the filename without the .txt extension
    filename=$(basename "$file" .txt)
    
    # Append the result to the hash_digest file
    echo "${filename}: ${hash}" >> hash_digest.txt
done

echo "Hash values have been recorded in hash_digest.txt ."
