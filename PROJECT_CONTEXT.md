# Contesto Progetto WebApp Pesca

## Overview
Applicazione web per l'identificazione e catalogazione delle specie ittiche, con funzionalità di riconoscimento immagini e database completo di informazioni.

## Stack Tecnologico
- Frontend: React.js + TypeScript + Tailwind CSS
- Backend: Python + FastAPI
- Database: PostgreSQL
- Cloud: AWS (EC2, S3, RDS, Lambda, Rekognition, CloudFront)
- ML: AWS Rekognition per identificazione immagini

## Timeline
- Durata totale: 18-24 settimane
- Fasi principali:
  1. Ricerca e Pianificazione (3-4 settimane)
  2. Backend e ML (5-7 settimane)
  3. Frontend (4-6 settimane)
  4. Testing (3-4 settimane)
  5. Deployment (2-3 settimane)
  6. Post-Launch (Ongoing)

## Funzionalità Core
1. Identificazione specie ittiche via immagine
2. Database completo con:
   - Specie
   - Catena alimentare
   - Abitudini
   - Alimentazione
3. Ricerca avanzata
4. Autenticazione utenti

## File di Documentazione
- `PROJECT_SPECIFICATIONS.md`: Requisiti e specifiche
- `TECHNICAL_STACK.md`: Stack tecnologico dettagliato
- `PROJECT_TIMELINE.md`: Timeline di sviluppo
- `TIMELINE_COMPARISON.md`: Analisi comparativa timeline

## Stato Attuale
- Fase: Backend base funzionante
- Ultimo aggiornamento: [Data]
- Prossimi step: Modelli database e API CRUD

## Note Importanti
- Dominio già acquistato su Porkbun
- Focus su UX/UI moderna
- Integrazione AWS per scalabilità
- Approccio MVP-first con iterazioni

## Decisioni Chiave
1. Stack tecnologico scelto per:
   - Scalabilità
   - Manutenibilità
   - Performance
   - Integrazione AWS

2. Timeline estesa per:
   - Ricerca approfondita
   - Testing esteso
   - Qualità prodotto
   - Stabilità

## Contatti e Risorse
- Repository: [URL - DA CREARE SU GITHUB]
- Documentazione: [URL]
- AWS Account: [Configurato]
- Dominio: [Configurato]

## Integrazione GitHub
- ✅ GitHub collegato a Cursor
- ✅ Username: JechiuMircea
- ✅ Repository: DA CREARE
- 🔄 Prossimo step: Creare repository e fare primo commit

## Endpoint Funzionanti
- **Server**: http://127.0.0.1:8080
- **Health Live**: http://127.0.0.1:8080/health/live → `{"status":"live"}`
- **Health Ready**: http://127.0.0.1:8080/health/ready → `{"status":"ready"}`
- **Documentazione Swagger**: http://127.0.0.1:8080/docs
- **Documentazione ReDoc**: http://127.0.0.1:8080/redoc

## Comando Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8080
```

## Problemi Risolti
- ✅ FastAPI installato e configurato
- ✅ Server Uvicorn funzionante su porta 8080
- ✅ Endpoint health check operativi
- ✅ Documentazione automatica generata
- ❌ Porta 8000 bloccata (usare 8080) 