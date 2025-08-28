from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .models import SpecieStatus

# Configurazione database SQLite per sviluppo
SQLALCHEMY_DATABASE_URL = "sqlite:///./pesca_webapp.db"

# Creazione engine e session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necessario per SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base per i modelli SQLAlchemy
Base = declarative_base()

# Modelli database
class SpecieItticaDB(Base):
    """Tabella database per le specie ittiche"""
    __tablename__ = "specie_ittiche"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_comune = Column(String(100), nullable=False, index=True)
    nome_scientifico = Column(String(150), nullable=False, unique=True, index=True)
    famiglia = Column(String(100), nullable=False, index=True)
    habitat = Column(String(200), nullable=False)
    taglia_min = Column(Float, nullable=True)
    taglia_max = Column(Float, nullable=True)
    peso_max = Column(Float, nullable=True)
    periodo_riproduzione = Column(String(100), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class IdentificazioneSpecieDB(Base):
    """Tabella database per le identificazioni specie"""
    __tablename__ = "identificazioni_specie"
    
    id = Column(Integer, primary_key=True, index=True)
    immagine_url = Column(String(500), nullable=False)
    utente_id = Column(String(100), nullable=True, index=True)
    specie_identificata = Column(String(150), nullable=True, index=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(SQLEnum(SpecieStatus), default=SpecieStatus.IN_ATTESA)
    feedback_utente = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Funzione per creare le tabelle
def create_tables():
    """Crea tutte le tabelle nel database"""
    Base.metadata.create_all(bind=engine)

# Funzione per ottenere la sessione database
def get_db():
    """Dependency per ottenere la sessione database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Popolamento dati iniziali per le specie ittiche
def populate_initial_data():
    """Popola il database con dati iniziali di specie ittiche comuni"""
    db = SessionLocal()
    try:
        # Verifica se ci sono già dati
        if db.query(SpecieItticaDB).count() > 0:
            return
        
        # Dati iniziali per specie ittiche comuni
        specie_iniziali = [
            {
                "nome_comune": "Trota",
                "nome_scientifico": "Salmo trutta",
                "famiglia": "Salmonidae",
                "habitat": "Acque dolci fredde e ossigenate",
                "taglia_min": 20.0,
                "taglia_max": 80.0,
                "peso_max": 10.0,
                "periodo_riproduzione": "Novembre-Dicembre",
                "note": "Specie molto apprezzata per la pesca sportiva"
            },
            {
                "nome_comune": "Carpa",
                "nome_scientifico": "Cyprinus carpio",
                "famiglia": "Cyprinidae",
                "habitat": "Laghi, stagni e fiumi a corso lento",
                "taglia_min": 30.0,
                "taglia_max": 120.0,
                "peso_max": 40.0,
                "periodo_riproduzione": "Maggio-Giugno",
                "note": "Specie resistente e adattabile"
            },
            {
                "nome_comune": "Persico",
                "nome_scientifico": "Perca fluviatilis",
                "famiglia": "Percidae",
                "habitat": "Laghi e fiumi con acque limpide",
                "taglia_min": 15.0,
                "taglia_max": 50.0,
                "peso_max": 3.0,
                "periodo_riproduzione": "Aprile-Maggio",
                "note": "Predatore di piccoli pesci"
            },
            {
                "nome_comune": "Luccio",
                "nome_scientifico": "Esox lucius",
                "famiglia": "Esocidae",
                "habitat": "Laghi e fiumi con vegetazione acquatica",
                "taglia_min": 40.0,
                "taglia_max": 150.0,
                "peso_max": 25.0,
                "periodo_riproduzione": "Febbraio-Marzo",
                "note": "Predatore aggressivo, molto apprezzato dai pescatori"
            },
            {
                "nome_comune": "Anguilla",
                "nome_scientifico": "Anguilla anguilla",
                "famiglia": "Anguillidae",
                "habitat": "Fiumi, laghi e acque costiere",
                "taglia_min": 30.0,
                "taglia_max": 100.0,
                "peso_max": 6.0,
                "periodo_riproduzione": "Settembre-Ottobre",
                "note": "Specie migratoria, nasce nel Mar dei Sargassi"
            }
        ]
        
        # Inserimento dati
        for specie_data in specie_iniziali:
            specie = SpecieItticaDB(**specie_data)
            db.add(specie)
        
        db.commit()
        print(f"✅ Popolato database con {len(specie_iniziali)} specie ittiche iniziali")
        
    except Exception as e:
        print(f"❌ Errore nel popolamento dati: {e}")
        db.rollback()
    finally:
        db.close()
