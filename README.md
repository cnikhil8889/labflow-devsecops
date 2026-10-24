# LabFlow DevSecOps

A portfolio delivery platform for a **synthetic laboratory run registry**. Built by Nikhil Kumar Choudavarapu as an independent learning project aligned to Thermo Fisher Scientific Engineer II, DevOps Engineering (R-01361623). No affiliation, company code, production data or validated medical functionality.

The engineering focus is the delivery system: cross-platform testing, Linux containers, secure SDLC gates, packaged artifacts, Kubernetes/Helm deployment and systematic incident diagnosis.

## Try it in two minutes

Requires Python 3.12; runtime has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python -m app.server
```

In a second terminal:

```bash
python scripts/smoke.py
curl http://127.0.0.1:8080/runs
```

Alternatively `docker compose up --build`. Use `docker compose down` to stop.

Endpoints: `GET /healthz`, `GET /readyz`, `GET /runs`, `POST /runs`. Example body:

```json
{"run_id":"demo-001","instrument":"microscope-01","status":"queued"}
```

The service validates identifiers and states, rejects duplicates atomically, limits request and registry size, and emits structured access logs. Storage is memory-only: restart loses all records. Keep a single replica for this demo; a shared transactional database is needed before scaling.

## Delivery path

Git push / PR → Linux + Windows Python tests and .NET build → code, dependency, secrets and image scans → Docker image → local kind cluster → atomic Helm install/upgrade → Python + .NET smoke checks → Helm chart and CycloneDX SBOM artifacts.

GitHub Actions does not deploy to a paid cloud or publish packages. It runs an ephemeral Kubernetes integration test. The .NET 8 console client validates the deployed service; PowerShell provides a Windows check entrypoint. The web delivery track is implemented; C++/Qt/CMake desktop delivery is outside this project's scope.

## Kubernetes / Rancher

Requires Docker, kind, kubectl and Helm 3:

```bash
kind create cluster --name labflow-demo
docker build -t labflow:0.1.0 .
kind load docker-image labflow:0.1.0 --name labflow-demo
IMAGE_TAG=0.1.0 bash scripts/deploy.sh
kubectl port-forward -n labflow service/labflow 8080:8080
# second terminal
python scripts/smoke.py
dotnet run --project clients/LabFlow.Check
```

For Rancher-managed Kubernetes, select an authorized kubeconfig context and make the image available in its registry. Set `IMAGE_REPOSITORY` and an immutable `IMAGE_TAG` before running the same script. No Rancher cluster is provisioned or claimed tested.

Cleanup: `helm uninstall labflow -n labflow`, `kubectl delete namespace labflow`, `kind delete cluster --name labflow-demo`.

## Evidence and limitations

See [validation](docs/VALIDATION.md), [role mapping](docs/ROLE-MAPPING.md), [operations](docs/RUNBOOK.md), [security](SECURITY.md) and [AI usage](docs/AI-USAGE.md). CI results must be checked on GitHub after upload; workflow presence alone does not prove it passed. This is a demo with no authentication, persistence, TLS ingress or production SLA. Bind only to loopback / private lab networks. Do not use real laboratory or personal data.

## License

MIT. See LICENSE.
