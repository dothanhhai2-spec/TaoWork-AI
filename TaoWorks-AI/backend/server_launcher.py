#!/usr/bin/env python3
import os, webbrowser, time, subprocess, sys

def main():
    port = os.environ.get("PORT", "8000")
    url = f"http://localhost:{port}/docs"
    try:
        subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port])
        time.sleep(2)
        webbrowser.open(url)
        print("TaoWorks AI API running at", url)
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
