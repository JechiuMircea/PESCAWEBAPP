from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SpecieStatus(str, Enum):
    """Enum per lo status di identificazione della specie"""

    IDENTIFICATA = "identificata"
    IN_ATTESA = "in_attesa"
    NON_IDENTIFICATA = "non_identificata"


class SpecieIttica(BaseModel):
    """Modello per una specie ittica identificata"""

    id: Optional[int] = None
    nome_comune: str = Field(..., description="Nome comune della specie")
    nome_scientifico: str = Field(..., description="Nome scientifico della specie")
    famiglia: str = Field(..., description="Famiglia tassonomica")
    habitat: str = Field(..., description="Habitat naturale")
    taglia_min: Optional[float] = Field(None, description="Taglia minima in cm")
    taglia_max: Optional[float] = Field(None, description="Taglia massima in cm")
    peso_max: Optional[float] = Field(None, description="Peso massimo in kg")
    periodo_riproduzione: Optional[str] = Field(
        None, description="Periodo di riproduzione"
    )
    note: Optional[str] = Field(None, description="Note aggiuntive")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SpecieItticaCreate(BaseModel):
    """Modello per creare una nuova specie ittica"""

    nome_comune: str = Field(..., description="Nome comune della specie")
    nome_scientifico: str = Field(..., description="Nome scientifico della specie")
    famiglia: str = Field(..., description="Famiglia tassonomica")
    habitat: str = Field(..., description="Habitat naturale")
    taglia_min: Optional[float] = Field(None, description="Taglia minima in cm")
    taglia_max: Optional[float] = Field(None, description="Taglia massima in cm")
    peso_max: Optional[float] = Field(None, description="Peso massimo in kg")
    periodo_riproduzione: Optional[str] = Field(
        None, description="Periodo di riproduzione"
    )
    note: Optional[str] = Field(None, description="Note aggiuntive")


class SpecieItticaUpdate(BaseModel):
    """Modello per aggiornare una specie ittica esistente"""

    nome_comune: Optional[str] = None
    nome_scientifico: Optional[str] = None
    famiglia: Optional[str] = None
    habitat: Optional[str] = None
    taglia_min: Optional[float] = None
    taglia_max: Optional[float] = None
    peso_max: Optional[float] = None
    periodo_riproduzione: Optional[str] = None
    note: Optional[str] = None


class IdentificazioneSpecie(BaseModel):
    """Modello per una richiesta di identificazione specie"""

    id: Optional[int] = None
    immagine_url: str = Field(..., description="URL dell'immagine da identificare")
    utente_id: Optional[str] = Field(
        None, description="ID dell'utente che ha richiesto l'identificazione"
    )
    specie_identificata: Optional[str] = Field(
        None, description="Specie identificata dal sistema ML"
    )
    confidence_score: Optional[float] = Field(
        None, description="Punteggio di confidenza dell'identificazione"
    )
    status: SpecieStatus = Field(
        default=SpecieStatus.IN_ATTESA, description="Status dell'identificazione"
    )
    feedback_utente: Optional[str] = Field(
        None, description="Feedback dell'utente sull'identificazione"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class IdentificazioneSpecieCreate(BaseModel):
    """Modello per creare una nuova richiesta di identificazione"""

    immagine_url: str = Field(..., description="URL dell'immagine da identificare")
    utente_id: Optional[str] = Field(
        None, description="ID dell'utente che ha richiesto l'identificazione"
    )


class IdentificazioneSpecieUpdate(BaseModel):
    """Modello per aggiornare una richiesta di identificazione"""

    specie_identificata: Optional[str] = None
    confidence_score: Optional[float] = None
    status: Optional[SpecieStatus] = None
    feedback_utente: Optional[str] = None
