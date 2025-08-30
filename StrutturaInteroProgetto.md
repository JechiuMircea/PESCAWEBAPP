# 📁 STRUTTURA PROGETTO PESCA WEBAPP

```
PESCAWEBAPP/
├── app/                                    # Applicazione FastAPI principale
│   ├── __pycache__/
│   │   ├── __init__.cpython-312.pyc
│   │   ├── database.cpython-312.pyc
│   │   ├── main.cpython-312.pyc
│   │   └── models.cpython-312.pyc
│   ├── routers/                            # Endpoint API
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── health.cpython-312.pyc
│   │   │   ├── identificazioni.cpython-312.pyc
│   │   │   └── specie.cpython-312.pyc
│   │   ├── __init__.py
│   │   ├── health.py                       # Health check endpoint
│   │   ├── identificazioni.py              # Endpoint identificazione pesci
│   │   └── specie.py                       # Endpoint gestione specie
│   ├── __init__.py
│   ├── database.py                         # Configurazione database
│   ├── fishbase_integration.py             # Integrazione FishBase
│   ├── main.py                             # Entry point FastAPI
│   └── models.py                           # Modelli dati SQLAlchemy
├── backend/                                # Backend e testing
│   ├── __pycache__/
│   │   ├── __init__.cpython-312.pyc
│   │   └── test_app.cpython-312.pyc
│   ├── __init__.py
│   ├── fishbase_data.csv                   # Dataset FishBase
│   ├── pesca_webapp.db                     # Database SQLite
│   ├── requirements.txt                    # Dipendenze produzione
│   ├── requirements-dev.txt                # Dipendenze sviluppo
│   ├── test_api.py                         # Test API
│   ├── test_app.py                         # Test applicazione
│   └── verify_database.py                  # Verifica database
├── docs/                                   # Documentazione progetto
│   ├── ADR/                                # Architecture Decision Records
│   │   └── 0001-stack-decision.md         # Decisione stack tecnologico
│   ├── api/                                # Documentazione API
│   │   └── README.md                       # Overview API
│   ├── architecture/                       # Documentazione architettura
│   │   ├── overview.md                     # Overview architettura
│   │   └── TECHNICAL_STACK.md              # Stack tecnologico dettagliato
│   ├── business_strategy/                  # Strategia business
│   │   └── README.md                       # Overview strategia
│   ├── guides/                             # Guide operative
│   │   └── README.md                       # Guide setup e utilizzo
│   ├── project/                            # Documenti progetto
│   │   ├── PROJECT_CONTEXT.md              # Contesto e obiettivi
│   │   ├── PROJECT_SPECIFICATIONS.md       # Specifiche funzionali
│   │   ├── PROJECT_TIMELINE.md             # Timeline sviluppo
│   │   ├── RISK_ASSESSMENT.md              # Analisi rischi
│   │   └── TIMELINE_COMPARISON.md          # Confronto timeline
│   ├── reference/                          # Riferimenti tecnici
│   │   └── README.md                       # Configurazioni e riferimenti
│   └── README.md                           # Overview documentazione
├── LimiteRaggiuntoChat/                    # Tracking progresso progetto
│   ├── PROGRESS_TRACKING_GUIDE.md          # Guida tracking
│   ├── PROJECT_MILESTONES.md               # Milestone completate
│   ├── PROJECT_PROGRESS.md                 # Progresso attuale
│   ├── README.md                           # Overview tracking
│   └── update_progress.py                  # Script aggiornamento progresso
├── scripts/                                # Script di utilità
│   └── analyze_venv.py                     # Analisi ambiente virtuale
├── venv/                                   # Ambiente virtuale Python
│   ├── Include/                            # Header C per estensioni
│   │   └── Include \ site \ python3.12 \ greenlet
│   │       └── C greenlet.h                # File header C per estensioni Python - compila coroutines greenlet
│   ├── Lib/                                # Librerie Python
│   │   └── site-packages/                  # Pacchetti installati
│   │       ├── __pycache__/
│   │       ├── _yaml/
│   │       ├── annotated_types/
│   │       ├── annotated_types-0.7.0.dist-info/
│   │       ├── anyio/
│   │       ├── anyio-4.10.0.dist-info/
│   │       ├── click/
│   │       ├── click-8.2.1.dist-info/
│   │       ├── colorama/
│   │       ├── colorama-0.4.6.dist-info/
│   │       ├── dotenv/
│   │       ├── fastapi/
│   │       ├── fastapi-0.112.0.dist-info/
│   │       ├── greenlet/
│   │       ├── greenlet-3.2.4.dist-info/
│   │       ├── h11/
│   │       ├── h11-0.16.0.dist-info/
│   │       ├── httptools/
│   │       ├── httptools-0.6.4.dist-info/
│   │       ├── idna/
│   │       ├── idna-3.10.dist-info/
│   │       ├── multipart/
│   │       ├── pip/
│   │       ├── pip-25.2.dist-info/
│   │       ├── pydantic/
│   │       ├── pydantic_core/
│   │       ├── pydantic_core-2.33.2.dist-info/
│   │       ├── pydantic-2.11.7.dist-info/
│   │       ├── python_dotenv-1.1.1.dist-info/
│   │       ├── python_multipart-0.0.9.dist-info/
│   │       ├── PyYAML-6.0.2.dist-info/
│   │       ├── sniffio/
│   │       ├── sniffio-1.3.1.dist-info/
│   │       ├── sqlalchemy/
│   │       ├── SQLAlchemy-2.0.27.dist-info/
│   │       ├── starlette/
│   │       ├── starlette-0.37.2.dist-info/
│   │       ├── typing_extensions-4.15.0.dist-info/
│   │       ├── typing_inspection/
│   │       ├── typing_inspection-0.4.1.dist-info/
│   │       ├── uvicorn-0.30.5.dist-info/
│   │       ├── watchfiles/
│   │       ├── watchfiles-1.1.0.dist-info/
│   │       ├── websockets/
│   │       ├── websockets-15.0.1.dist-info/
│   │       ├── yaml/
│   │       └── typing_extensions.py
│   ├── Scripts/                            # Script eseguibili
│   │   ├── activate                        # Attivazione venv
│   │   ├── activate.bat                    # Attivazione venv (Windows)
│   │   ├── Activate.ps1                    # Attivazione venv (PowerShell)
│   │   ├── deactivate.bat                  # Disattivazione venv
│   │   ├── dotenv.exe                      # Gestione variabili ambiente
│   │   ├── fastapi.exe                     # CLI FastAPI
│   │   ├── pip.exe                         # Gestore pacchetti Python
│   │   ├── pip3.12.exe                     # Gestore pacchetti Python 3.12
│   │   ├── pip3.exe                        # Gestore pacchetti Python 3
│   │   ├── python.exe                      # Interprete Python
│   │   ├── pythonw.exe                     # Interprete Python (Windows)
│   │   ├── uvicorn.exe                     # Server ASGI
│   │   ├── watchfiles.exe                  # Monitoraggio file
│   │   └── websockets.exe                  # Gestione WebSocket
│   └── pyvenv.cfg                          # Configurazione ambiente virtuale
├── .editorconfig                            # Configurazione editor
├── .gitignore                               # File ignorati da Git
├── .python-version                          # Versione Python progetto
├── fishbase_data.csv                        # Dataset FishBase (copia)
├── pesca_webapp.db                          # Database SQLite (copia)
├── README.md                                # Documentazione principale progetto
├── StrutturaInteroProgetto.md               # Questo file - struttura progetto
└── update_dates.py                          # Script aggiornamento date progetto
