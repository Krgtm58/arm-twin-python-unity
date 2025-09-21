import http.server
import socketserver
import threading
import json
import os
import time

# Configuration: JSON files to monitor
json_files = {
    "shoulder_angle.json": {"last_modified": 0, "last_value": None},
    "elbow_angle.json": {"last_modified": 0, "last_value": None},
    "base_angle.json": {"last_modified": 0, "last_value": None},
}

# Base directory containing the JSON files
base_dir = r"C:\Users\LENOVO\OneDrive\Desktop\Unity_Project\angle_data"
os.chdir(base_dir)

# Custom HTTP handler with CORS & application/json support
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        if path.endswith(".json"):
            return "application/json"
        return super().guess_type(path)

# Start local HTTP server
def start_server():
    with socketserver.TCPServer(("", 8000), CORSRequestHandler) as httpd:
        print("✅ Serving JSON files at http://localhost:8000")
        httpd.serve_forever()

# Monitor JSON files for manual changes
def monitor_json_files():
    print("👁️ Watching JSON files for manual edits...")
    while True:
        for file_name, info in json_files.items():
            file_path = os.path.join(base_dir, file_name)
            try:
                modified = os.path.getmtime(file_path)
                if modified != info["last_modified"]:
                    info["last_modified"] = modified
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        angle = data.get("angle", None)
                        if angle != info["last_value"]:
                            print(f"[Updated] {file_name} angle = {angle}")
                            json_files[file_name]["last_value"] = angle
            except Exception as e:
                print(f"❌ Error reading {file_name}: {e}")
        time.sleep(0.5)

# Start HTTP server in background
threading.Thread(target=start_server, daemon=True).start()

# Start JSON file monitoring in main thread
monitor_json_files()
