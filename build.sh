#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Build the web version using pygbag
python -m pygbag --build main.py

# Output success message
echo "Breakout game built successfully for web deployment" 