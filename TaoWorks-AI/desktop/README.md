# Desktop Packaging Options

1. **Backend EXE (PyInstaller)**: Build `server_launcher.py` into a single executable.
2. **Frontend**: Build static site `npm run build` and host via a local webview wrapper:
   - Tauri (Rust), Neutralino, or Electron (Node). Point the webview to `http://localhost:8000` or embed the static build.
3. **All-in-one**: Start the API in the background then launch the webview pointing to `http://127.0.0.1:8000`.

This repo ships a backend-first EXE path for simplicity.
