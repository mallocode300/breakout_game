#!/usr/bin/env python3
import os
import subprocess
import webbrowser
import time
import sys

def main():
    print("Starting Breakout Game Web Deployment")
    print("-------------------------------------")
    
    # Check if pygbag is installed
    try:
        import pygbag
    except ImportError:
        print("Pygbag not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag"])
    
    # Check if pygame is installed
    try:
        import pygame
    except ImportError:
        print("Pygame not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygame"])
    
    print("\nDeploying game to web...")
    pygbag_process = subprocess.Popen([sys.executable, "-m", "pygbag", "main.py"])
    
    # Wait for the server to start
    time.sleep(3)
    
    # Open the game in the browser
    print("\nOpening game in web browser...")
    webbrowser.open("http://localhost:8000")
    
    print("\nGame is now running in your browser!")
    print("Press Ctrl+C in this terminal to stop the server when you're done.")
    
    try:
        # Keep the script running until user interrupts
        pygbag_process.wait()
    except KeyboardInterrupt:
        print("\nStopping server...")
        pygbag_process.terminate()
        print("Server stopped. Goodbye!")

if __name__ == "__main__":
    main() 