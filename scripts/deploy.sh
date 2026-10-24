#!/usr/bin/env bash
set -euo pipefail
: "${IMAGE_TAG:?Set IMAGE_TAG to a tested image tag}"
IMAGE_REPOSITORY="${IMAGE_REPOSITORY:-labflow}"
helm upgrade --install labflow charts/labflow --namespace labflow --create-namespace \
  --set-string image.repository="$IMAGE_REPOSITORY" --set-string image.tag="$IMAGE_TAG" \
  --atomic --wait --timeout 120s
kubectl rollout status deployment/labflow -n labflow --timeout=120s
