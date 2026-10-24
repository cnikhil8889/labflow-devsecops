# CNK | Nikhil Kumar Choudavarapu | LabFlow DevSecOps
"""Fail fast if deployed service is unhealthy or cannot register synthetic runs."""
import json
import os
import urllib.request
import uuid

base = os.getenv("LABFLOW_URL", "http://127.0.0.1:8080")
if not base.startswith(("http://127.0.0.1:", "http://localhost:")):
    raise SystemExit("Smoke test allows loopback only; port-forward the cluster service first")
with urllib.request.urlopen(base + "/healthz", timeout=5) as response:
    assert response.status == 200
run = {"run_id": "smoke-" + uuid.uuid4().hex, "instrument": "synthetic", "status": "completed"}
request = urllib.request.Request(base + "/runs", json.dumps(run).encode(), {"Content-Type": "application/json"})
with urllib.request.urlopen(request, timeout=5) as response:
    assert response.status == 201
with urllib.request.urlopen(base + "/runs", timeout=5) as response:
    assert run in json.load(response)["runs"]
print("PASS: health, synthetic write and read")
