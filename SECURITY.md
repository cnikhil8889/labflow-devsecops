# Security model

Use synthetic data only. The unauthenticated demo must remain on loopback or in an isolated lab. ClusterIP is not an authentication boundary. Before production add identity, per-operation authorization, TLS, durable storage, rate limits, retention controls, audit trails and network policies.

Controls included: schema validation, body and record limits, atomic duplicate protection, non-root UID, dropped capabilities, disabled service-account token, read-only root filesystem and resource limits. HTTP server is Python's educational server, not a production server.

CI gates: CodeQL and Bandit static analysis; Trivy filesystem and image vulnerability scans; TruffleHog verified-secret scanning; CycloneDX SBOM. Standard-library-only Python runtime has no pip dependencies to audit; container OS and .NET SDK/runtime still need patching. Verified-only secret detection can miss unverified credentials: review diffs too. CodeQL availability depends on repository visibility and GitHub plan. Third-party Actions currently use version tags; pin reviewed immutable SHAs before using with privileged credentials.

Triage findings: reproduce → assess severity and exploitability → update dependency/base image or fix code → rerun all checks → record remediation in PR. Do not silently bypass HIGH/CRITICAL failures. Time-bound any justified exception with owner and expiry. No real credentials are needed by this repository.
