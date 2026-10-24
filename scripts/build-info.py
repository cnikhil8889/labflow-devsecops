# CNK | Nikhil Kumar Choudavarapu
"""Write traceable, non-secret project build metadata."""
import json
import os
from pathlib import Path

metadata = {
    "project": "LabFlow DevSecOps",
    "mark": "CNK",
    "owner": "Nikhil Kumar Choudavarapu",
    "commit": os.getenv("GITHUB_SHA", "local"),
    "run_number": os.getenv("GITHUB_RUN_NUMBER", "local"),
}
Path("build-info.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps(metadata))
