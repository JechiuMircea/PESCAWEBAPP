# ADR 0001: Stack Tecnologico

## Status
Accepted

## Context
Il progetto richiede un sistema scalabile per riconoscimento immagini e gestione dati ittici, con UX moderna e deployment su cloud.

## Decision
- Frontend: React + TypeScript + Tailwind CSS
- Backend: Python + FastAPI
- Database: PostgreSQL (AWS RDS)
- Cloud: AWS (S3, CloudFront, Lambda, Rekognition)

## Rationale
- Ecosistema maturo, grande community
- Tipizzazione per ridurre bug e migliorare maintainability
- FastAPI per performance e DX, autogen API docs
- PostgreSQL per dati relazionali + JSON
- AWS per scalabilità, servizi gestiti e integrazioni ML

## Consequences
- Tooling multipiattaforma (Node + Python)
- Necessità CI/CD ibrida
- Costi AWS da monitorare e ottimizzare

