"""
server.py — Urban Analytics dev server
Serves static files AND runs the pipeline via /run-pipeline?country=Japan

Usage:
    python server.py          (starts on port 8080)
    python server.py 9000     (custom port)
"""

import http.server
import socketserver
import subprocess
import json
import sys
import os
import urllib.parse
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
BASE = Path(__file__).parent.resolve()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ── /run-pipeline?country=Japan ──────────────────────────────
        if self.path.startswith("/run-pipeline"):
            params  = urllib.parse.parse_qs(parsed.query)
            country = params.get("country", [""])[0].strip()

            if not country:
                self._json(400, {"error": "country parameter required"})
                return

            print(f"\n[pipeline] Running for: {country}")
            try:
                env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
                result = subprocess.run(
                    [sys.executable, str(BASE / "generate_gravity.py"), country],
                    capture_output=True, text=True, timeout=60, cwd=str(BASE),
                    env=env, encoding="utf-8"
                )
                if result.returncode != 0:
                    err = result.stderr.strip() or result.stdout.strip() or "Pipeline failed"
                    print(f"[pipeline] ERROR: {err}")
                    self._json(500, {"error": err})
                else:
                    print(f"[pipeline] Done.\n{result.stdout.strip()}")
                    self._json(200, {"success": True, "country": country, "log": result.stdout})
            except subprocess.TimeoutExpired:
                self._json(500, {"error": "Pipeline timed out (>60s)"})
            except Exception as e:
                self._json(500, {"error": str(e)})
            return

        # ── Everything else → static files ──────────────────────────
        super().do_GET()

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Only print pipeline-related logs; suppress noisy static file requests
        msg = args[0] if args else ""
        if "/run-pipeline" in msg or "500" in str(args):
            super().log_message(fmt, *args)


# Set allow_reuse_address BEFORE binding (class-level, not instance-level)
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Urban Analytics server running at http://localhost:{PORT}")
    print(f"   Serving files from: {BASE}")
    print(f"   Pipeline API: http://localhost:{PORT}/run-pipeline?country=Japan")
    print(f"   ⚠️  Using port {PORT} (port 8080 is reserved by Apache/XAMPP)")
    print(f"   Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
