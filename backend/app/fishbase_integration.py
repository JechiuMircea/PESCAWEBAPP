#!/usr/bin/env python3
"""
Modulo per l'integrazione con FishBase
Popola il database con tutte le specie ittiche disponibili
"""

import requests
import pandas as pd
import sqlite3
from typing import List, Dict, Optional
import time
import logging
from pathlib import Path
import os

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FishBaseIntegration:
    """Classe per l'integrazione con FishBase"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Percorso relativo alla directory del progetto
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            self.db_path = os.path.join(project_root, "pesca_webapp.db")
        else:
            self.db_path = db_path
        
        self.base_url = "https://www.fishbase.se/summary/"
        logger.info(f"🗄️ Database path: {self.db_path}")
        
    def download_fishbase_dataset(self, output_path: str = "fishbase_data.csv") -> bool:
        """
        Scarica il dataset FishBase (simulato per ora)
        In produzione, questo sarà sostituito con download reale
        """
        try:
            logger.info("🔄 Download dataset FishBase...")
            
            # Per ora creiamo un dataset di esempio esteso
            # In produzione, questo sarà sostituito con download reale da FishBase API
            
            # Dataset esteso con specie comuni
            specie_estese = [
                # Salmonidi
                {"nome_comune": "Trota", "nome_scientifico": "Salmo trutta", "famiglia": "Salmonidae", 
                 "habitat": "Acque dolci fredde e ossigenate", "taglia_min": 20.0, "taglia_max": 80.0, 
                 "peso_max": 10.0, "periodo_riproduzione": "Novembre-Dicembre", 
                 "note": "Specie molto apprezzata per la pesca sportiva"},
                
                {"nome_comune": "Salmone", "nome_scientifico": "Salmo salar", "famiglia": "Salmonidae",
                 "habitat": "Mari e fiumi freddi", "taglia_min": 50.0, "taglia_max": 150.0,
                 "peso_max": 40.0, "periodo_riproduzione": "Settembre-Novembre",
                 "note": "Specie migratoria, molto apprezzata"},
                
                # Ciprinidi
                {"nome_comune": "Carpa", "nome_scientifico": "Cyprinus carpio", "famiglia": "Cyprinidae",
                 "habitat": "Laghi, stagni e fiumi a corso lento", "taglia_min": 30.0, "taglia_max": 120.0,
                 "peso_max": 40.0, "periodo_riproduzione": "Maggio-Giugno",
                 "note": "Specie resistente e adattabile"},
                
                {"nome_comune": "Tinca", "nome_scientifico": "Tinca tinca", "famiglia": "Cyprinidae",
                 "habitat": "Laghi e stagni con vegetazione", "taglia_min": 20.0, "taglia_max": 70.0,
                 "peso_max": 8.0, "periodo_riproduzione": "Maggio-Luglio",
                 "note": "Specie molto resistente, sopravvive in acque povere di ossigeno"},
                
                {"nome_comune": "Scardola", "nome_scientifico": "Scardinius erythrophthalmus", "famiglia": "Cyprinidae",
                 "habitat": "Laghi e fiumi a corso lento", "taglia_min": 15.0, "taglia_max": 40.0,
                 "peso_max": 1.5, "periodo_riproduzione": "Aprile-Giugno",
                 "note": "Specie gregaria, forma banchi numerosi"},
                
                # Percidi
                {"nome_comune": "Persico", "nome_scientifico": "Perca fluviatilis", "famiglia": "Percidae",
                 "habitat": "Laghi e fiumi con acque limpide", "taglia_min": 15.0, "taglia_max": 50.0,
                 "peso_max": 3.0, "periodo_riproduzione": "Aprile-Maggio",
                 "note": "Predatore di piccoli pesci"},
                
                {"nome_comune": "Persico Sole", "nome_scientifico": "Lepomis gibbosus", "famiglia": "Centrarchidae",
                 "habitat": "Laghi e stagni con vegetazione", "taglia_min": 10.0, "taglia_max": 30.0,
                 "peso_max": 1.0, "periodo_riproduzione": "Maggio-Giugno",
                 "note": "Specie introdotta dall'America, molto colorata"},
                
                # Esocidi
                {"nome_comune": "Luccio", "nome_scientifico": "Esox lucius", "famiglia": "Esocidae",
                 "habitat": "Laghi e fiumi con vegetazione acquatica", "taglia_min": 40.0, "taglia_max": 150.0,
                 "peso_max": 25.0, "periodo_riproduzione": "Febbraio-Marzo",
                 "note": "Predatore aggressivo, molto apprezzato dai pescatori"},
                
                # Anguillidi
                {"nome_comune": "Anguilla", "nome_scientifico": "Anguilla anguilla", "famiglia": "Anguillidae",
                 "habitat": "Fiumi, laghi e acque costiere", "taglia_min": 30.0, "taglia_max": 100.0,
                 "peso_max": 6.0, "periodo_riproduzione": "Settembre-Ottobre",
                 "note": "Specie migratoria, nasce nel Mar dei Sargassi"},
                
                # Altri predatori
                {"nome_comune": "Siluro", "nome_scientifico": "Silurus glanis", "famiglia": "Siluridae",
                 "habitat": "Fiumi e laghi grandi", "taglia_min": 50.0, "taglia_max": 300.0,
                 "peso_max": 150.0, "periodo_riproduzione": "Maggio-Giugno",
                 "note": "Il più grande pesce d'acqua dolce d'Europa"},
                
                {"nome_comune": "Storione", "nome_scientifico": "Acipenser sturio", "famiglia": "Acipenseridae",
                 "habitat": "Mari e fiumi", "taglia_min": 100.0, "taglia_max": 500.0,
                 "peso_max": 400.0, "periodo_riproduzione": "Aprile-Maggio",
                 "note": "Specie protetta, molto rara in natura"},
                
                # Specie marine comuni
                {"nome_comune": "Branzino", "nome_scientifico": "Dicentrarchus labrax", "famiglia": "Moronidae",
                 "habitat": "Mari e lagune costiere", "taglia_min": 25.0, "taglia_max": 100.0,
                 "peso_max": 12.0, "periodo_riproduzione": "Dicembre-Marzo",
                 "note": "Specie molto apprezzata in cucina"},
                
                {"nome_comune": "Orata", "nome_scientifico": "Sparus aurata", "famiglia": "Sparidae",
                 "habitat": "Mari e lagune costiere", "taglia_min": 20.0, "taglia_max": 70.0,
                 "peso_max": 8.0, "periodo_riproduzione": "Ottobre-Dicembre",
                 "note": "Specie ermafrodita, cambia sesso durante la vita"},
                
                {"nome_comune": "Sgombro", "nome_scientifico": "Scomber scombrus", "famiglia": "Scombridae",
                 "habitat": "Mari aperti", "taglia_min": 20.0, "taglia_max": 50.0,
                 "peso_max": 3.0, "periodo_riproduzione": "Maggio-Luglio",
                 "note": "Specie pelagica, forma grandi banchi"},
                
                {"nome_comune": "Tonno", "nome_scientifico": "Thunnus thynnus", "famiglia": "Scombridae",
                 "habitat": "Mari aperti e profondi", "taglia_min": 100.0, "taglia_max": 400.0,
                 "peso_max": 600.0, "periodo_riproduzione": "Giugno-Agosto",
                 "note": "Specie migratoria, molto apprezzata per la pesca sportiva"}
            ]
            
            # Converti in DataFrame
            df = pd.DataFrame(specie_estese)
            
            # Salva su file
            df.to_csv(output_path, index=False)
            
            logger.info(f"✅ Dataset creato con {len(specie_estese)} specie")
            logger.info(f"📁 Salvato in: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore nel download: {e}")
            return False
    
    def populate_database(self, csv_path: str = "fishbase_data.csv") -> bool:
        """
        Popola il database con i dati FishBase
        """
        try:
            logger.info("🔄 Popolamento database con dati FishBase...")
            
            # Verifica che il database esista
            if not os.path.exists(self.db_path):
                logger.error(f"❌ Database non trovato: {self.db_path}")
                return False
            
            # Leggi il CSV
            df = pd.read_csv(csv_path)
            
            # Connessione al database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Conta specie esistenti
            cursor.execute("SELECT COUNT(*) FROM specie_ittiche")
            count_before = cursor.fetchone()[0]
            
            # Inserisci nuove specie
            for _, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO specie_ittiche 
                        (nome_comune, nome_scientifico, famiglia, habitat, taglia_min, taglia_max, peso_max, periodo_riproduzione, note)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['nome_comune'],
                        row['nome_scientifico'],
                        row['famiglia'],
                        row['habitat'],
                        row['taglia_min'],
                        row['taglia_max'],
                        row['peso_max'],
                        row['periodo_riproduzione'],
                        row['note']
                    ))
                except Exception as e:
                    logger.warning(f"⚠️ Errore nell'inserimento di {row['nome_scientifico']}: {e}")
                    continue
            
            # Commit delle modifiche
            conn.commit()
            
            # Conta specie dopo l'inserimento
            cursor.execute("SELECT COUNT(*) FROM specie_ittiche")
            count_after = cursor.fetchone()[0]
            
            # Statistiche
            nuove_specie = count_after - count_before
            totale_specie = count_after
            
            logger.info(f"✅ Database popolato con successo!")
            logger.info(f"📊 Specie prima: {count_before}")
            logger.info(f"📊 Nuove specie inserite: {nuove_specie}")
            logger.info(f"📊 Totale specie nel database: {totale_specie}")
            
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore nel popolamento database: {e}")
            return False
    
    def get_database_stats(self) -> Dict:
        """
        Ottiene statistiche del database
        """
        try:
            if not os.path.exists(self.db_path):
                logger.error(f"❌ Database non trovato: {self.db_path}")
                return {}
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Conta totale specie
            cursor.execute("SELECT COUNT(*) FROM specie_ittiche")
            totale_specie = cursor.fetchone()[0]
            
            # Conta per famiglia
            cursor.execute("""
                SELECT famiglia, COUNT(*) as count 
                FROM specie_ittiche 
                GROUP BY famiglia 
                ORDER BY count DESC
            """)
            famiglie = dict(cursor.fetchall())
            
            # Conta per habitat
            cursor.execute("""
                SELECT habitat, COUNT(*) as count 
                FROM specie_ittiche 
                GROUP BY habitat 
                ORDER BY count DESC
            """)
            habitat = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "totale_specie": totale_specie,
                "famiglie": famiglie,
                "habitat": habitat
            }
            
        except Exception as e:
            logger.error(f"❌ Errore nel recupero statistiche: {e}")
            return {}

def main():
    """Funzione principale per l'integrazione FishBase"""
    logger.info("🚀 Avvio integrazione FishBase...")
    
    # Crea istanza
    fishbase = FishBaseIntegration()
    
    # Step 1: Download dataset
    if fishbase.download_fishbase_dataset():
        logger.info("✅ Dataset scaricato con successo")
        
        # Step 2: Popolamento database
        if fishbase.populate_database():
            logger.info("✅ Database popolato con successo")
            
            # Step 3: Statistiche
            stats = fishbase.get_database_stats()
            logger.info("📊 Statistiche database:")
            logger.info(f"   Totale specie: {stats.get('totale_specie', 0)}")
            logger.info(f"   Famiglie: {len(stats.get('famiglie', {}))}")
            logger.info(f"   Habitat: {len(stats.get('habitat', {}))}")
            
        else:
            logger.error("❌ Errore nel popolamento database")
    else:
        logger.error("❌ Errore nel download dataset")

if __name__ == "__main__":
    main()
