from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SpecieItticaDB, get_db
from app.models import SpecieIttica, SpecieItticaCreate, SpecieItticaUpdate

router = APIRouter(prefix="/specie", tags=["specie"])


@router.get("/", response_model=List[SpecieIttica])
def get_specie(
    skip: int = Query(0, description="Numero di record da saltare"),
    limit: int = Query(100, description="Numero massimo di record da restituire"),
    famiglia: Optional[str] = Query(None, description="Filtra per famiglia"),
    habitat: Optional[str] = Query(None, description="Filtra per habitat"),
    db: Session = Depends(get_db),
):
    """
    Ottiene la lista delle specie ittiche con filtri opzionali
    """
    query = db.query(SpecieItticaDB)

    # Applica filtri se specificati
    if famiglia:
        query = query.filter(SpecieItticaDB.famiglia.ilike(f"%{famiglia}%"))
    if habitat:
        query = query.filter(SpecieItticaDB.habitat.ilike(f"%{habitat}%"))

    # Applica paginazione
    specie = query.offset(skip).limit(limit).all()

    # Converte in modelli Pydantic
    return [
        SpecieIttica(
            id=specie.id,
            nome_comune=specie.nome_comune,
            nome_scientifico=specie.nome_scientifico,
            famiglia=specie.famiglia,
            habitat=specie.habitat,
            taglia_min=specie.taglia_min,
            taglia_max=specie.taglia_max,
            peso_max=specie.peso_max,
            periodo_riproduzione=specie.periodo_riproduzione,
            note=specie.note,
            created_at=specie.created_at,
            updated_at=specie.updated_at,
        )
        for specie in specie
    ]


@router.get("/{specie_id}", response_model=SpecieIttica)
def get_specie_by_id(specie_id: int, db: Session = Depends(get_db)):
    """
    Ottiene una specie ittica specifica per ID
    """
    specie = db.query(SpecieItticaDB).filter(SpecieItticaDB.id == specie_id).first()
    if not specie:
        raise HTTPException(status_code=404, detail="Specie ittica non trovata")

    return SpecieIttica(
        id=specie.id,
        nome_comune=specie.nome_comune,
        nome_scientifico=specie.nome_scientifico,
        famiglia=specie.famiglia,
        habitat=specie.habitat,
        taglia_min=specie.taglia_min,
        taglia_max=specie.taglia_max,
        peso_max=specie.peso_max,
        periodo_riproduzione=specie.periodo_riproduzione,
        note=specie.note,
        created_at=specie.created_at,
        updated_at=specie.updated_at,
    )


@router.post("/", response_model=SpecieIttica, status_code=201)
def create_specie(specie: SpecieItticaCreate, db: Session = Depends(get_db)):
    """
    Crea una nuova specie ittica
    """
    # Verifica se esiste già una specie con lo stesso nome scientifico
    existing_specie = (
        db.query(SpecieItticaDB)
        .filter(SpecieItticaDB.nome_scientifico == specie.nome_scientifico)
        .first()
    )

    if existing_specie:
        raise HTTPException(
            status_code=400, detail="Esiste già una specie con questo nome scientifico"
        )

    # Crea la nuova specie
    db_specie = SpecieItticaDB(
        nome_comune=specie.nome_comune,
        nome_scientifico=specie.nome_scientifico,
        famiglia=specie.famiglia,
        habitat=specie.habitat,
        taglia_min=specie.taglia_min,
        taglia_max=specie.taglia_max,
        peso_max=specie.peso_max,
        periodo_riproduzione=specie.periodo_riproduzione,
        note=specie.note,
    )

    db.add(db_specie)
    db.commit()
    db.refresh(db_specie)

    return SpecieIttica(
        id=db_specie.id,
        nome_comune=db_specie.nome_comune,
        nome_scientifico=db_specie.nome_scientifico,
        famiglia=db_specie.famiglia,
        habitat=db_specie.habitat,
        taglia_min=db_specie.taglia_min,
        taglia_max=db_specie.taglia_max,
        peso_max=db_specie.peso_max,
        periodo_riproduzione=db_specie.periodo_riproduzione,
        note=db_specie.note,
        created_at=db_specie.created_at,
        updated_at=db_specie.updated_at,
    )


@router.put("/{specie_id}", response_model=SpecieIttica)
def update_specie(
    specie_id: int, specie_update: SpecieItticaUpdate, db: Session = Depends(get_db)
):
    """
    Aggiorna una specie ittica esistente
    """
    db_specie = db.query(SpecieItticaDB).filter(SpecieItticaDB.id == specie_id).first()
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie ittica non trovata")

    # Aggiorna solo i campi forniti
    update_data = specie_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_specie, field, value)

    db_specie.updated_at = db_specie.updated_at
    db.commit()
    db.refresh(db_specie)

    return SpecieIttica(
        id=db_specie.id,
        nome_comune=db_specie.nome_comune,
        nome_scientifico=db_specie.nome_scientifico,
        famiglia=db_specie.famiglia,
        habitat=db_specie.habitat,
        taglia_min=db_specie.taglia_min,
        taglia_max=db_specie.taglia_max,
        peso_max=db_specie.peso_max,
        periodo_riproduzione=db_specie.periodo_riproduzione,
        note=db_specie.note,
        created_at=db_specie.created_at,
        updated_at=db_specie.updated_at,
    )


@router.delete("/{specie_id}")
def delete_specie(specie_id: int, db: Session = Depends(get_db)):
    """
    Elimina una specie ittica
    """
    db_specie = db.query(SpecieItticaDB).filter(SpecieItticaDB.id == specie_id).first()
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie ittica non trovata")

    db.delete(db_specie)
    db.commit()

    return {"message": "Specie ittica eliminata con successo"}


@router.get("/search/{query}", response_model=List[SpecieIttica])
def search_specie(query: str, db: Session = Depends(get_db)):
    """
    Cerca specie ittiche per nome comune o scientifico
    """
    specie = (
        db.query(SpecieItticaDB)
        .filter(
            (SpecieItticaDB.nome_comune.ilike(f"%{query}%"))
            | (SpecieItticaDB.nome_scientifico.ilike(f"%{query}%"))
        )
        .all()
    )

    return [
        SpecieIttica(
            id=specie.id,
            nome_comune=specie.nome_comune,
            nome_scientifico=specie.nome_scientifico,
            famiglia=specie.famiglia,
            habitat=specie.habitat,
            taglia_min=specie.taglia_min,
            taglia_max=specie.taglia_max,
            peso_max=specie.peso_max,
            periodo_riproduzione=specie.periodo_riproduzione,
            note=specie.note,
            created_at=specie.created_at,
            updated_at=specie.updated_at,
        )
        for specie in specie
    ]
