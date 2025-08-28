from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.health import router as health_router
from .routers.specie import router as specie_router
from .routers.identificazioni import router as identificazioni_router
from .database import create_tables, populate_initial_data

# Creazione app FastAPI
app = FastAPI(
    title="Pesca WebApp API", 
    version="0.1.0",
    description="API per l'identificazione di specie ittiche tramite machine learning",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurazione CORS per sviluppo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specificare domini specifici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusione router
app.include_router(health_router)
app.include_router(specie_router)
app.include_router(identificazioni_router)

@app.on_event("startup")
async def startup_event():
    """
    Evento eseguito all'avvio dell'applicazione
    """
    print("🚀 Avvio Pesca WebApp API...")
    
    # Crea le tabelle del database
    create_tables()
    print("✅ Tabelle database create")
    
    # Popola il database con dati iniziali
    populate_initial_data()
    print("✅ Database inizializzato con dati di esempio")
    
    print("🎯 API pronta per l'uso!")

@app.get("/")
async def root():
    """
    Endpoint root dell'API
    """
    return {
        "message": "Benvenuto nella Pesca WebApp API!",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health/live"
    }

