#!/bin/bash

# Configuration
CLIENT_SCRIPT="udp.client.py"
SERVER_HOST="127.0.0.1"  # Server IP (change if remote)
SERVER_PORT=5000         # Port to connect to
FILE_SIZES=("100mb.dat" "200mb.dat" "500mb.dat" "1gb.dat" "2gb.dat")  # Match server configuration
BUFFER_SIZES=(1024 4096 8192 16384 32768)

# Ensure client script is executable
chmod +x ${CLIENT_SCRIPT}

# Loop through each file and buffer size
for file_size in "${FILE_SIZES[@]}"; do
    for buffer_size in "${BUFFER_SIZES[@]}"; do
        echo "========================================"
        echo "Starting client: Expecting File: ${file_size}, Buffer Size: ${buffer_size} bytes"
        echo "========================================"

        # Run client
        python ${CLIENT_SCRIPT} --host ${SERVER_HOST} --port ${SERVER_PORT} \
            --buffer ${buffer_size} --file ${file_size}

        echo "Client completed for File: ${file_size}, Buffer Size: ${buffer_size}"

        sleep 3
    done
done

echo "All client tests completed!"
