FROM python:3.15.0-alpine3.24
# CNK: patch the minimal runtime; keep HIGH/CRITICAL image scanning enforced.
RUN apk upgrade --no-cache
LABEL org.opencontainers.image.authors="CNK - Nikhil Kumar Choudavarapu" org.opencontainers.image.title="CNK LabFlow DevSecOps"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=8080
WORKDIR /service
COPY --chown=10001:10001 app /service/app
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=2)"]
CMD ["python", "-m", "app.server"]
