import subprocess
import sys
import os
import importlib

def check_and_install(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} not installed; installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
def install_requirements(req_file):
    if not os.path.exists(req_file):
        print(f"Requirements file not found: {req_file}")
        sys.exit(1)
    with open(req_file, "r", encoding="utf-8") as f:
        packages = [line.strip() for line in f if line.strip()]
    for pkg in packages:
        check_and_install(pkg)

def main():
    req_file = "./requirements.txt"
    install_requirements(req_file)
    
    apple_podcast_id = input("Enter Apple Podcast ID: ").strip()
    ret = subprocess.run([sys.executable, "./id2xlsx.py", apple_podcast_id])
    if ret.returncode != 0:
        print("id2xlsx.py failed.")
        sys.exit(1)
    
    ret = subprocess.run([sys.executable, "./podcast_downloader.py"])
    if ret.returncode != 0:
        print("podcast_downloader.py failed.")
        sys.exit(1)
        
    ret = subprocess.run([sys.executable, "./whipser.py"])
    if ret.returncode != 0:
        print("whipser.py failed.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
