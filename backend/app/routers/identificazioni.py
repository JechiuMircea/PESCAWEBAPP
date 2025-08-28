from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import random
from ..database import get_db, IdentificazioneSpecieDB, SpecieItticaDB
from ..models import (
    IdentificazioneSpecie, 
    IdentificazioneSpecieCreate, 
    IdentificazioneSpecieUpdate,
    SpecieStatus
)

router = APIRouter(prefix="/identificazioni", tags=["identificazioni"])

def simulate_ml_identification(image_url: str) -> tuple[str, float]:
    """
    Simula l'identificazione ML di una specie ittica
    In produzione, questo sarà sostituito da AWS Rekognition
    """
    # Specie comuni per la simulazione
    specie_comuni = [
        "Trota", "Carpa", "Persico", "Luccio", "Anguilla",
        "Tinca", "Scardola", "Cavedano", "Barbo", "Salmone"
    ]
    
    # Simula un punteggio di confidenza realistico
    confidence = random.uniform(0.6, 0.95)
    
    # Simula anche casi di non identificazione
    if confidence < 0.7:
        return None, confidence
    
    # Seleziona una specie casuale
    specie = random.choice(specie_comuni)
    
    return specie, confidence

@router.get("/", response_model=List[IdentificazioneSpecie])
def get_identificazioni(
    skip: int = Query(0, description="Numero di record da saltare"),
    limit: int = Query(100, description="Numero massimo di record da restituire"),
    status: Optional[SpecieStatus] = Query(None, description="Filtra per status"),
    utente_id: Optional[str] = Query(None, description="Filtra per utente"),
    db: Session = Depends(get_db)
):
    """
    Ottiene la lista delle identificazioni con filtri opzionali
    """
    query = db.query(IdentificazioneSpecieDB)
    
    # Applica filtri se specificati
    if status:
        query = query.filter(IdentificazioneSpecieDB.status == status)
    if utente_id:
        query = query.filter(IdentificazioneSpecieDB.utente_id == utente_id)
    
    # Ordina per data di creazione (più recenti prima)
    query = query.order_by(IdentificazioneSpecieDB.created_at.desc())
    
    # Applica paginazione
    identificazioni = query.offset(skip).limit(limit).all()
    
    # Converte in modelli Pydantic
    return [
        IdentificazioneSpecie(
            id=ident.id,
            immagine_url=ident.immagine_url,
            utente_id=ident.utente_id,
            specie_identificata=ident.specie_identificata,
            confidence_score=ident.confidence_score,
            status=ident.status,
            feedback_utente=ident.feedback_utente,
            created_at=ident.created_at,
            updated_at=ident.updated_at
        )
        for ident in identificazioni
    ]

@router.get("/{identificazione_id}", response_model=IdentificazioneSpecie)
def get_identificazione_by_id(identificazione_id: int, db: Session = Depends(get_db)):
    """
    Ottiene una identificazione specifica per ID
    """
    ident = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.id == identificazione_id
    ).first()
    
    if not ident:
        raise HTTPException(status_code=404, detail="Identificazione non trovata")
    
    return IdentificazioneSpecie(
        id=ident.id,
        immagine_url=ident.immagine_url,
        utente_id=ident.utente_id,
        specie_identificata=ident.specie_identificata,
        confidence_score=ident.confidence_score,
        status=ident.status,
        feedback_utente=ident.feedback_utente,
        created_at=ident.created_at,
        updated_at=ident.updated_at
    )

@router.post("/", response_model=IdentificazioneSpecie, status_code=201)
def create_identificazione(
    identificazione: IdentificazioneSpecieCreate, 
    db: Session = Depends(get_db)
):
    """
    Crea una nuova richiesta di identificazione e simula l'identificazione ML
    """
    # Simula l'identificazione ML
    specie_identificata, confidence_score = simulate_ml_identification(
        identificazione.immagine_url
    )
    
    # Determina lo status basato sul risultato
    if specie_identificata:
        status = SpecieStatus.IDENTIFICATA
    else:
        status = SpecieStatus.NON_IDENTIFICATA
    
    # Crea la nuova identificazione
    db_ident = IdentificazioneSpecieDB(
        immagine_url=identificazione.immagine_url,
        utente_id=identificazione.utente_id,
        specie_identificata=specie_identificata,
        confidence_score=confidence_score,
        status=status
    )
    
    db.add(db_ident)
    db.commit()
    db.refresh(db_ident)
    
    return IdentificazioneSpecie(
        id=db_ident.id,
        immagine_url=db_ident.immagine_url,
        utente_id=db_ident.utente_id,
        specie_identificata=db_ident.specie_identificata,
        confidence_score=db_ident.confidence_score,
        status=db_ident.status,
        feedback_utente=db_ident.feedback_utente,
        created_at=db_ident.created_at,
        updated_at=db_ident.updated_at
    )

@router.put("/{identificazione_id}", response_model=IdentificazioneSpecie)
def update_identificazione(
    identificazione_id: int, 
    identificazione_update: IdentificazioneSpecieUpdate, 
    db: Session = Depends(get_db)
):
    """
    Aggiorna una identificazione esistente (es. per feedback utente)
    """
    db_ident = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.id == identificazione_id
    ).first()
    
    if not db_ident:
        raise HTTPException(status_code=404, detail="Identificazione non trovata")
    
    # Aggiorna solo i campi forniti
    update_data = identificazione_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ident, field, value)
    
    db_ident.updated_at = db_ident.updated_at
    db.commit()
    db.refresh(db_ident)
    
    return IdentificazioneSpecie(
        id=db_ident.id,
        immagine_url=db_ident.immagine_url,
        utente_id=db_ident.utente_id,
        specie_identificata=db_ident.specie_identificata,
        confidence_score=db_ident.confidence_score,
        status=db_ident.status,
        feedback_utente=db_ident.feedback_utente,
        created_at=db_ident.created_at,
        updated_at=db_ident.updated_at
    )

@router.delete("/{identificazione_id}")
def delete_identificazione(identificazione_id: int, db: Session = Depends(get_db)):
    """
    Elimina una identificazione
    """
    db_ident = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.id == identificazione_id
    ).first()
    
    if not db_ident:
        raise HTTPException(status_code=404, detail="Identificazione non trovata")
    
    db.delete(db_ident)
    db.commit()
    
    return {"message": "Identificazione eliminata con successo"}

@router.post("/{identificazione_id}/feedback")
def add_feedback(
    identificazione_id: int, 
    feedback: str, 
    db: Session = Depends(get_db)
):
    """
    Aggiunge feedback utente a una identificazione
    """
    db_ident = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.id == identificazione_id
    ).first()
    
    if not db_ident:
        raise HTTPException(status_code=404, detail="Identificazione non trovata")
    
    db_ident.feedback_utente = feedback
    db_ident.updated_at = db_ident.updated_at
    db.commit()
    
    return {"message": "Feedback aggiunto con successo"}

@router.get("/stats/overview")
def get_identificazioni_stats(db: Session = Depends(get_db)):
    """
    Ottiene statistiche generali sulle identificazioni
    """
    total = db.query(IdentificazioneSpecieDB).count()
    identificate = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.status == SpecieStatus.IDENTIFICATA
    ).count()
    non_identificate = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.status == SpecieStatus.NON_IDENTIFICATA
    ).count()
    in_attesa = db.query(IdentificazioneSpecieDB).filter(
        IdentificazioneSpecieDB.status == SpecieStatus.IN_ATTESA
    ).count()
    
    # Calcola percentuali
    if total > 0:
        success_rate = (identificate / total) * 100
    else:
        success_rate = 0
    
    return {
        "total_identificazioni": total,
        "identificate": identificate,
        "non_identificate": non_identificate,
        "in_attesa": in_attesa,
        "success_rate_percent": round(success_rate, 2)
    }
