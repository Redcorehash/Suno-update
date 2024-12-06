import requests
import os
import subprocess
import sys

# Define the URL for checking the latest version
VERSION_CHECK_URL = "https://api.suno.com/version"
# Define the URL for downloading the latest version
DOWNLOAD_URL = "https://download.suno.com/suno_4.0_latest.zip"
# Define the local directory to store the downloaded file
DOWNLOAD_DIR = os.path.expanduser("~/suno_updates")
# Define the local file name for the downloaded file
DOWNLOAD_FILE = os.path.join(DOWNLOAD_DIR, "suno_4.0_latest.zip")
# Define the installation directory
INSTALL_DIR = os.path.expanduser("~/suno_4.0")

def check_for_updates():
    try:
        response = requests.get(VERSION_CHECK_URL)
        response.raise_for_status()
        latest_version = response.json().get("version")
        current_version = get_current_version()
        
        if latest_version > current_version:
            print(f"New version available: {latest_version}")
            return True
        else:
            print("You are already on the latest version.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")
        return False

def get_current_version():
    # Implement logic to get the current version of Suno 4.0
    # This could be reading a version file or checking the installed version
    # For simplicity, let's assume the current version is stored in a file
    version_file = os.path.join(INSTALL_DIR, "version.txt")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "0.0.0"  # Default version if no version file is found

def download_update():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    try:
        response = requests.get(DOWNLOAD_URL, stream=True)
        response.raise_for_status()
        
        with open(DOWNLOAD_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading update: {e}")

def install_update():
    try:
        # Unzip the downloaded file
        subprocess.run(["unzip", DOWNLOAD_FILE, "-d", INSTALL_DIR], check=True)
        print("Installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing update: {e}")

def main():
    if check_for_updates():
        download_update()
        install_update()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
