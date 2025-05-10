#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt

# Build the web version using pygbag
python3 -m pygbag --build main.py

# Make sure the output directory exists
mkdir -p build/web

# Check if pygbag created files in the expected location
if [ -d "build/web" ]; then
  echo "Breakout game built successfully for web deployment"
else
  echo "Error: build/web directory not found! Checking for other directories..."
  find . -type d -name "web" | grep .
  
  # If files were created somewhere else, try to move them to the expected location
  if [ -d "./build" ]; then
    echo "Contents of ./build directory:"
    ls -la ./build
  fi
fi 