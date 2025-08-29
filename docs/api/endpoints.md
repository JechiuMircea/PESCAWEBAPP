# 🔌 API Endpoints - Pesca WebApp

## 🎯 Panoramica API

**Pesca WebApp** fornisce un'API RESTful completa per la gestione di specie ittiche e identificazioni tramite machine learning.

## 🌐 Base URL

```
http://127.0.0.1:8080  # Sviluppo locale
```

## 📚 Documentazione Interattiva

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

## 🔍 Endpoint Principali

### **Root**
```
GET / - Informazioni generali API
```

### **Health Check**
```
GET /health/live - Stato API
```

## 🐟 Gestione Specie Ittiche

### **Lista Specie**
```http
GET /specie/
```

**Parametri Query:**
- `skip` (int): Record da saltare (default: 0)
- `limit` (int): Record massimi (default: 100)
- `famiglia` (string): Filtra per famiglia
- `habitat` (string): Filtra per habitat

**Risposta:**
```json
[
  {
    "id": 1,
    "nome_comune": "Trota",
    "nome_scientifico": "Salmo trutta",
    "famiglia": "Salmonidae",
    "habitat": "Acque dolci fredde e ossigenate",
    "taglia_min": 20.0,
    "taglia_max": 80.0,
    "peso_max": 10.0,
    "periodo_riproduzione": "Novembre-Dicembre",
    "note": "Specie molto apprezzata per la pesca sportiva",
    "created_at": "2025-08-29T22:31:00",
    "updated_at": "2025-08-29T22:31:00"
  }
]
```

### **Specie per ID**
```http
GET /specie/{specie_id}
```

### **Crea Nuova Specie**
```http
POST /specie/
```

**Body:**
```json
{
  "nome_comune": "Carpa",
  "nome_scientifico": "Cyprinus carpio",
  "famiglia": "Cyprinidae",
  "habitat": "Laghi e stagni",
  "taglia_min": 30.0,
  "taglia_max": 120.0,
  "peso_max": 40.0,
  "periodo_riproduzione": "Maggio-Giugno",
  "note": "Specie resistente"
}
```

### **Aggiorna Specie**
```http
PUT /specie/{specie_id}
```

### **Elimina Specie**
```http
DELETE /specie/{specie_id}
```

### **Ricerca Specie**
```http
GET /specie/search/{query}
```

## 🔍 Identificazioni Specie

### **Lista Identificazioni**
```http
GET /identificazioni/
```

**Parametri Query:**
- `skip` (int): Record da saltare
- `limit` (int): Record massimi
- `status` (enum): Filtra per status
- `utente_id` (string): Filtra per utente

### **Identificazione per ID**
```http
GET /identificazioni/{identificazione_id}
```

### **Crea Identificazione**
```http
POST /identificazioni/
```

**Body:**
```json
{
  "immagine_url": "https://example.com/fish.jpg",
  "utente_id": "user123"
}
```

### **Aggiorna Identificazione**
```http
PUT /identificazioni/{identificazione_id}
```

### **Elimina Identificazione**
```http
DELETE /identificazioni/{identificazione_id}
```

### **Aggiungi Feedback**
```http
POST /identificazioni/{identificazione_id}/feedback
```

### **Statistiche Identificazioni**
```http
GET /identificazioni/stats/overview
```

## 📊 Status Codes

- **200**: Successo
- **201**: Creato
- **400**: Bad Request
- **404**: Non trovato
- **500**: Errore interno

## 🔐 Autenticazione

*Attualmente non implementata - in sviluppo*

## 📝 Esempi di Utilizzo

Vedi [examples.md](examples.md) per esempi completi.

---

**Prossimo**: [Modelli API](models.md)
