#!/bin/bash

echo "=== Environment Information ==="
echo "Current working directory: $(pwd)"
echo "Files in current directory:"
ls -la

echo ""
echo "=== Python Installation ==="
which python3 || echo "Python3 not found"
python3 --version || echo "Python3 version check failed"

echo ""
echo "=== Pip Installation ==="
which pip3 || echo "Pip3 not found"
pip3 --version || echo "Pip3 version check failed"

echo ""
echo "=== Build Process ==="
echo "Creating build directory structure"
mkdir -p build/web

echo "Creating test files in build directory"
echo "<html><body><h1>Test Build Success</h1></body></html>" > build/web/index.html

echo ""
echo "=== Verification ==="
echo "Contents of build directory:"
ls -la build || echo "Build directory not found"
echo "Contents of build/web directory:"
ls -la build/web || echo "Build/web directory not found"

# Make the build directory and files accessible
chmod -R 755 build 