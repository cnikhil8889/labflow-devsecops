# Operations and failure drills

## Pipeline red

Read the first failing job, reproduce its exact command, record commit/runner/tool version. Python validation failure: replay the malformed JSON test. Image vulnerability: rebuild with a patched base and rerun Trivy. Helm lint/render error: inspect generated YAML before deployment. Do not disable a gate to make the badge green.

## Rollout timeout / ImagePullBackOff

Run `kubectl get pods -n labflow`, `kubectl describe pod -n labflow <pod>`, `kubectl logs -n labflow deployment/labflow` and `helm history labflow -n labflow`. Confirm repository/tag exists, image is loaded in kind, registry access and UID compatibility. `--atomic` restores the previous successful Helm release on upgrade failure. For a manual rollback: `helm rollback labflow <known-good-revision> -n labflow --wait`. Restart/rollback discards memory-only records.

## Failure drill

1. Install the good image and run smoke checks.
2. Upgrade using a deliberately nonexistent image tag and a 30-second timeout with `--atomic`.
3. Expect a nonzero command exit; confirm Helm history and a healthy previous revision.
4. Rerun smoke and record observations in an issue. This drill is documented, not claimed executed.

## Upgrade / deprecation checklist

Weekly: review Dependabot, base-image advisories and failing scans. Monthly: inspect Python/.NET support windows and Action runner changes. Change one tool at a time on a branch; run Linux/Windows tests, container build, scan, Helm deployment and smoke test; retain previous artifact and rollback notes. Move .NET 8 to a supported version before its support window closes.

## Team workflow

Small issues with acceptance criteria; feature branches and PR review; attach test evidence; note risk and rollback. Backlog: database-backed registry, authentication, network policy, image signing/attestation, immutable Action SHAs, automated failure drill and latency metrics. No fabricated production performance claims.
