# Validation — 2026-10-24

Executed in Python 3.12.14 on Linux:

- `python -m unittest discover -s tests -v`: 5 tests passed, including real HTTP requests and concurrent duplicate rejection.
- `python -m compileall -q app scripts tests`: passed.
- `bash -n scripts/deploy.sh`: passed.
- Started `python -m app.server`, then `python scripts/smoke.py`: health, synthetic create and read passed.

Not executed here: Docker build, Helm render/lint, Kubernetes rollout/rollback, Windows PowerShell, .NET compile/runtime, CodeQL, Bandit, Trivy or TruffleHog. Required executables are unavailable locally. GitHub Actions configures these checks; inspect its actual run before claiming success. Rancher compatibility is documented, not tested.
