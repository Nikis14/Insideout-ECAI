#!/bin/bash

# Define the destination directory
DEST_DIR="data"
cd ..
# Create the destination directory if it doesn't exist
mkdir -p ${DEST_DIR}

# Define the URL of the file to download
FILE_URL="https://dl.fbaipublicfiles.com/parlai/empatheticdialogues/empatheticdialogues.tar.gz"

# Download the file into the specified directory
wget ${FILE_URL} -P ${DEST_DIR}/

cd ${DEST_DIR}
tar -xzvf empatheticdialogues.tar.gz
rm empatheticdialogues.tar.gz

echo "Process completed successfully."
