# Deployment Guide

## Docker

```bash
make docker-build-all
make docker-up
```

## Docker Compose (Full Stack)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Includes: backend, frontend, Redis, PostgreSQL.

## Kubernetes

```bash
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## Environment Variables

See `.env.example` for all configuration options.
