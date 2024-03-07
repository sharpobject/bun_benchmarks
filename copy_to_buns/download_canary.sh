#!/bin/bash

while true; do
    # Set the download URL
    url="https://github.com/oven-sh/bun/releases/download/canary/bun-linux-x64.zip"

    # Create a directory for the canary release
    mkdir -p "canary"

    # Download the canary release
    wget -q -O "canary/bun-canary.zip" "$url"

    # Extract the ZIP file
    unzip -q "canary/bun-canary.zip" -d "canary"

    # Get the revision information
    revision=$(./canary/bun-linux-x64/bun --revision)

    echo "Bun revision: $revision"

    # Create the bun_releases directory if it doesn't exist
    mkdir -p "bun_releases"

    # Check if a folder with the revision name already exists
    if [ ! -d "bun_releases/bun-v$revision" ]; then
        # Create a new folder with the revision name
        mkdir -p "bun_releases/bun-v$revision"

        # Copy the Bun binary to the revision folder
        cp -r "canary/bun-linux-x64" "bun_releases/bun-v$revision"

        echo "Bun binary copied to bun_releases/bun-v$revision"
    else
        echo "Folder bun_releases/bun-v$revision already exists"
    fi

    # Clean up the canary directory
    rm -rf "canary"

    # Sleep for 1 minute
    sleep 60
done
