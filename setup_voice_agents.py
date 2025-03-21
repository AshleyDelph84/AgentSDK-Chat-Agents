#!/usr/bin/env python
"""
Setup script for Voice Agent dependencies
This script helps install all necessary dependencies for the voice agent system
"""

import subprocess
import sys
import os

def install_packages():
    """Install required packages for the voice agent system"""
    print("Installing required packages...")
    
    # Basic requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Voice-specific dependencies (some might require special handling)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-agents[voice]>=0.0.6"])
        print("Successfully installed OpenAI Agents voice dependencies")
    except Exception as e:
        print(f"Warning: Could not install openai-agents[voice]: {e}")
        print("You may need to install it manually with: pip install 'openai-agents[voice]>=0.0.6'")
    
    print("\nAll dependencies installed successfully.")
    print("\nTo run the voice agent system: python voice_multi_agent.py")
    print("Note: You need a working microphone and speakers for this to work.")

if __name__ == "__main__":
    install_packages() 