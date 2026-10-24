# CNK | Nikhil Kumar Choudavarapu | LabFlow DevSecOps
"""Synthetic laboratory run registry. No patient data; ephemeral demo storage."""
import json
import logging
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG = logging.getLogger("labflow")
MAX_BODY = 4096

class Registry:
    def __init__(self):
        self.runs = {}
        self.lock = threading.Lock()

    def add(self, data):
        if not isinstance(data, dict) or set(data) != {"run_id", "instrument", "status"}:
            raise ValueError("Expected run_id, instrument and status only")
        for key in ("run_id", "instrument"):
            if not isinstance(data[key], str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", data[key]):
                raise ValueError("Identifiers must be 1-64 alphanumeric, underscore or dash characters")
        if data["status"] not in ("queued", "running", "completed", "failed"):
            raise ValueError("Invalid status")
        with self.lock:
            if data["run_id"] in self.runs:
                raise KeyError("Duplicate run_id")
            if len(self.runs) >= 1000:
                raise OverflowError("Demo capacity reached")
            self.runs[data["run_id"]] = dict(data)
        return dict(data)

    def snapshot(self):
        with self.lock:
            return [dict(run) for run in self.runs.values()]


def handler_for(registry):
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, code, data):
            payload = json.dumps(data).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path in ("/healthz", "/readyz"):
                self.send_json(200, {"status": "ok"})
            elif self.path == "/runs":
                self.send_json(200, {"runs": registry.snapshot()})
            else:
                self.send_json(404, {"error": "Not found"})

        def do_POST(self):
            if self.path != "/runs":
                self.send_json(404, {"error": "Not found"})
                return
            try:
                if self.headers.get_content_type() != "application/json":
                    self.send_json(415, {"error": "Use application/json"})
                    return
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_BODY:
                    self.send_json(413, {"error": "Body must be 1-4096 bytes"})
                    return
                data = json.loads(self.rfile.read(length))
                self.send_json(201, registry.add(data))
            except (ValueError, TypeError, UnicodeDecodeError):
                self.send_json(400, {"error": "Invalid JSON or run schema"})
            except KeyError:
                self.send_json(409, {"error": "Duplicate run_id"})
            except OverflowError:
                self.send_json(503, {"error": "Demo capacity reached"})

        def log_message(self, format, *args):
            LOG.info(json.dumps({"method": self.command, "message": format % args}))
    return Handler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    LOG.info("CNK | LabFlow DevSecOps | Nikhil Kumar Choudavarapu")
    server = ThreadingHTTPServer((os.getenv("HOST", "127.0.0.1"), int(os.getenv("PORT", "8080"))), handler_for(Registry()))
    server.daemon_threads = True
    server.serve_forever()
