#!/usr/bin/env python3
"""
Quick setup script for the Mood-Based Music Recommender
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please run manually:")
        print("pip install spotipy python-dotenv")
        return False

def create_env_template():
    """Create a .env template file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"Creating {env_file} template...")
        with open(env_file, 'w') as f:
            f.write("# Spotify API Credentials\n")
            f.write("# Get these from: https://developer.spotify.com/dashboard/\n")
            f.write("SPOTIPY_CLIENT_ID='your_spotify_client_id_here'\n")
            f.write("SPOTIPY_CLIENT_SECRET='your_spotify_client_secret_here'\n")
        print(f"Created {env_file} - Please add your Spotify API credentials!")
    else:
        print(f"{env_file} already exists.")

def main():
    """Main setup process"""
    print("=" * 60)
    print("Mood-Based Music Recommender Setup")
    print("=" * 60)
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env template
    create_env_template()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("Next steps:")
    print("1. Get Spotify API credentials from: https://developer.spotify.com/dashboard/")
    print("2. Edit .env file with your actual credentials")
    print("3. Run: python Song_Recomendation.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
