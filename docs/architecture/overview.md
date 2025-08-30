# 🏗️ Overview Architettura Sistema

## 🎯 Panoramica Generale

**Pesca WebApp** è un sistema completo per l'identificazione di specie ittiche che combina:

- **Backend API** (FastAPI + Python)
- **Frontend Web** (React + TypeScript)
- **Machine Learning** (AWS Rekognition)
- **Database** (SQLite + SQLAlchemy)

## 🏛️ Architettura a Livelli

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                        │
│                    UI/UX Layer                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                   │
│                    Business Logic Layer                     │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    ML Service (AWS)                        │
│                    AI/ML Layer                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database (SQLite)                       │
│                    Data Layer                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flusso Dati Principale

### 1. **Identificazione Specie**
```
Utente → Frontend → API → ML Service → Database → Risposta
```

### 2. **Gestione Specie**
```
Utente → Frontend → API → Database → Risposta
```

### 3. **Ricerca e Filtri**
```
Utente → Frontend → API → Database → Risposta
```

## 🎯 Componenti Chiave

### **Backend (FastAPI)**
- **API RESTful** per tutte le operazioni ✅
- **Validazione dati** con Pydantic ✅
- **Database ORM** con SQLAlchemy ✅
- **Server attivo** su porta 8080 ✅

### **Frontend (React)**
- **Setup tecnico** React + TypeScript + Vite ✅
- **Server attivo** su porta 5173 ✅
- **Hot reload** funzionante ✅
- **Struttura base** configurata ✅
- **Sviluppo web app** in corso 🔄

### **ML Pipeline**
- **AWS Rekognition** per identificazione immagini
- **Preprocessing** immagini
- **Post-processing** risultati
- **Fallback** a database locale

### **Database**
- **SQLite** per sviluppo
- **PostgreSQL** per produzione
- **Migrazioni** automatiche
- **Backup** e recovery

## 🔒 Sicurezza

- **CORS** configurato per sviluppo
- **Validazione input** rigorosa
- **Rate limiting** per API
- **Logging** completo

## 📊 Scalabilità

- **Microservizi** ready
- **Load balancing** supportato
- **Caching** implementabile
- **Monitoring** e alerting

---

**Prossimo**: [Backend Architecture](backend.md)

---

## ⚠️ **NOTA IMPORTANTE - GITHUB**

**Branch `main` è protetta su GitHub** - Le modifiche devono essere fatte attraverso Pull Request da branch feature.
