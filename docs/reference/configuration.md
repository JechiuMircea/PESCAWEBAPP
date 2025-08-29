# ⚙️ Configurazione Progetto

## 🎯 Panoramica Configurazione

**Pesca WebApp** utilizza un sistema di configurazione flessibile per gestire diversi ambienti (sviluppo, staging, produzione).

## 🔧 File di Configurazione

### **1. Requirements Files**

#### **`backend/requirements.txt`**
```txt
# Produzione
fastapi==0.112.0
uvicorn==0.30.5
sqlalchemy==2.0.27
python-multipart==0.0.9
requests
pandas
```

#### **`backend/requirements-dev.txt`**
```txt
# Sviluppo
-r requirements.txt

# Code quality tools
flake8
isort
black
pre-commit
cookiecutter
```

### **2. Environment Variables**

#### **`.env` (da creare)**
```bash
# Database
DATABASE_URL=sqlite:///./pesca_webapp.db

# Server
HOST=127.0.0.1
PORT=8080
DEBUG=true

# AWS (per produzione)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=eu-west-1

# ML Service
ML_SERVICE_URL=https://your-ml-service.com
ML_API_KEY=your_api_key
```

## 🗄️ Configurazione Database

### **SQLite (Sviluppo)**
```python
# app/database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./pesca_webapp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

### **PostgreSQL (Produzione)**
```python
# app/database.py
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/pesca_webapp"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

## 🌐 Configurazione Server

### **Uvicorn Settings**
```bash
# Sviluppo
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload

# Produzione
python -m uvicorn app.main:app --host 0.0.0.0 --port 80 --workers 4
```

### **FastAPI Settings**
```python
# app/main.py
app = FastAPI(
    title="Pesca WebApp API",
    version="0.1.0",
    description="API per l'identificazione di specie ittiche",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

## 🔒 Configurazione Sicurezza

### **CORS (Cross-Origin Resource Sharing)**
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specificare domini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Rate Limiting (Futuro)**
```python
# Da implementare
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## 📊 Configurazione Logging

### **Logging Base**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
```

### **File Logging (Produzione)**
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "pesca_webapp.log", 
    maxBytes=10000000, 
    backupCount=5
)
logger.addHandler(handler)
```

## 🚀 Configurazione Deployment

### **Docker (Futuro)**
```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### **Docker Compose (Futuro)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "80:80"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/pesca_webapp
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=pesca_webapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```

## 🔍 Configurazione Testing

### **Pytest (Futuro)**
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### **Coverage (Futuro)**
```ini
# .coveragerc
[run]
source = app
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
```

## 📝 Variabili d'Ambiente per Ambiente

### **Sviluppo**
```bash
export ENVIRONMENT=development
export DEBUG=true
export DATABASE_URL=sqlite:///./pesca_webapp.db
```

### **Produzione**
```bash
export ENVIRONMENT=production
export DEBUG=false
export DATABASE_URL=postgresql://user:pass@localhost/pesca_webapp
```

## 🔗 Link Utili

- **FastAPI Settings**: [https://fastapi.tiangolo.com/tutorial/settings/](https://fastapi.tiangolo.com/tutorial/settings/)
- **SQLAlchemy Config**: [https://docs.sqlalchemy.org/en/20/core/engines.html](https://docs.sqlalchemy.org/en/20/core/engines.html)
- **Uvicorn Config**: [https://www.uvicorn.org/settings/](https://www.uvicorn.org/settings/)

---

**Prossimo**: [Troubleshooting](troubleshooting.md)
