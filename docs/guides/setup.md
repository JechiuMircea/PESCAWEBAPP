# 🚀 Setup Ambiente Sviluppo

## 🎯 Prerequisiti

### **Software Richiesto:**
- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **VS Code** (raccomandato) - [Download](https://code.visualstudio.com/)

### **Account Richiesti:**
- **GitHub** - Per repository
- **AWS** (opzionale) - Per ML reale

## 🔧 Setup Locale

### **1. Clona Repository**
```bash
git clone https://github.com/JechiuMircea/PESCAWEBAPP.git
cd PESCAWEBAPP
```

### **2. Crea Ambiente Virtuale**
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3. Installa Dipendenze**
```bash
# Produzione
pip install -r backend/requirements.txt

# Sviluppo (opzionale)
pip install -r backend/requirements-dev.txt
```

### **4. Verifica Installazione**
```bash
python -c "import fastapi, uvicorn, sqlalchemy; print('✅ Tutte le dipendenze installate!')"
```

## 🗄️ Setup Database

### **1. Avvia Server**
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

### **2. Verifica Database**
```bash
python backend/verify_database.py
```

### **3. Test API**
```bash
python backend/test_api.py
```

## 🌐 Accesso Applicazione

### **URL Locali:**
- **API**: http://127.0.0.1:8080
- **Documentazione**: http://127.0.0.1:8080/docs
- **ReDoc**: http://127.0.0.1:8080/redoc

### **Health Check:**
- **Status**: http://127.0.0.1:8080/health/live

## 🧪 Test Setup

### **1. Test Endpoint Base**
```bash
curl http://127.0.0.1:8080/
```

**Risposta attesa:**
```json
{
  "message": "Benvenuto nella Pesca WebApp API!",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health/live"
}
```

### **2. Test Health Check**
```bash
curl http://127.0.0.1:8080/health/live
```

**Risposta attesa:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-29T22:31:00"
}
```

### **3. Test Lista Specie**
```bash
curl http://127.0.0.1:8080/specie/
```

## 🔍 Troubleshooting

### **Problemi Comuni:**

#### **Porta 8080 Occupata**
```bash
# Trova processo
netstat -ano | findstr :8080

# Termina processo
taskkill /PID <PID> /F
```

#### **ModuleNotFoundError**
```bash
# Verifica ambiente virtuale
venv\Scripts\Activate.ps1

# Reinstalla dipendenze
pip install -r backend/requirements.txt
```

#### **Database Non Creato**
```bash
# Avvia server (crea automaticamente database)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

## 📱 Prossimi Passi

1. **Frontend Setup** - [Guida Sviluppo](development.md)
2. **AWS Integration** - [ML Pipeline](../architecture/ml-pipeline.md)
3. **Deployment** - [Guida Deployment](deployment.md)

## 🔗 Link Utili

- **Repository**: [GitHub](https://github.com/JechiuMircea/PESCAWEBAPP)
- **FastAPI Docs**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **SQLAlchemy Docs**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)

---

**Prossimo**: [Guida Sviluppo](development.md)
