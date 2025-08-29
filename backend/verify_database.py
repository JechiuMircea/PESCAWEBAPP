#!/usr/bin/env python3
"""
Script per verificare la struttura e i dati del database Pesca WebApp
"""

import sqlite3
import os
from pathlib import Path

def verify_database_structure():
    """Verifica la struttura del database"""
    print("🔍 VERIFICA STRUTTURA DATABASE")
    print("=" * 50)
    
    # Verifica esistenza database
    db_path = "pesca_webapp.db"
    if not os.path.exists(db_path):
        print(f"❌ Database non trovato: {db_path}")
        return False
    
    print(f"✅ Database trovato: {db_path}")
    
    # Connessione al database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Connessione database riuscita")
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return False
    
    # 1. Verifica tabelle esistenti
    print("\n📋 TABELLE NEL DATABASE:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    if not tables:
        print("❌ Nessuna tabella trovata!")
        return False
    
    for table in tables:
        print(f"  ✅ {table[0]}")
    
    # 2. Verifica schema tabella specie_ittiche
    print("\n🏗️ SCHEMA TABELLA 'specie_ittiche':")
    try:
        cursor.execute("PRAGMA table_info(specie_ittiche)")
        columns = cursor.fetchall()
        
        print("  Colonna | Tipo | Nullable | Default | Primary Key")
        print("  --------|------|----------|---------|------------")
        
        for col in columns:
            cid, name, type_name, not_null, default_value, pk = col
            nullable = "NO" if not_null else "YES"
            pk_mark = "YES" if pk else "NO"
            print(f"  {name:8} | {type_name:6} | {nullable:8} | {str(default_value):7} | {pk_mark:11}")
            
    except Exception as e:
        print(f"❌ Errore verifica schema: {e}")
    
    # 3. Verifica schema tabella identificazioni_specie
    print("\n🏗️ SCHEMA TABELLA 'identificazioni_specie':")
    try:
        cursor.execute("PRAGMA table_info(identificazioni_specie)")
        columns = cursor.fetchall()
        
        print("  Colonna | Tipo | Nullable | Default | Primary Key")
        print("  --------|------|----------|---------|------------")
        
        for col in columns:
            cid, name, type_name, not_null, default_value, pk = col
            nullable = "NO" if not_null else "YES"
            pk_mark = "YES" if pk else "NO"
            print(f"  {name:8} | {type_name:6} | {nullable:8} | {str(default_value):7} | {pk_mark:11}")
            
    except Exception as e:
        print(f"❌ Errore verifica schema: {e}")
    
    # 4. Verifica indici
    print("\n🔍 INDICI NEL DATABASE:")
    cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'")
    indexes = cursor.fetchall()
    
    if indexes:
        for idx in indexes:
            print(f"  ✅ {idx[0]} (tabella: {idx[1]})")
    else:
        print("  ⚠️ Nessun indice trovato")
    
    # 5. Verifica vincoli
    print("\n🔒 VINCOLI NEL DATABASE:")
    cursor.execute("PRAGMA foreign_key_list(specie_ittiche)")
    foreign_keys = cursor.fetchall()
    
    if foreign_keys:
        for fk in foreign_keys:
            print(f"  ✅ Foreign Key: {fk[3]} -> {fk[2]}.{fk[4]}")
    else:
        print("  ℹ️ Nessun foreign key configurato")
    
    conn.close()
    return True

def verify_database_data():
    """Verifica i dati nel database"""
    print("\n📊 VERIFICA DATI DATABASE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect("pesca_webapp.db")
        cursor = conn.cursor()
        
        # 1. Conteggio specie
        cursor.execute("SELECT COUNT(*) FROM specie_ittiche")
        total_species = cursor.fetchone()[0]
        print(f"🐟 Totale specie nel database: {total_species}")
        
        # 2. Conteggio identificazioni
        cursor.execute("SELECT COUNT(*) FROM identificazioni_specie")
        total_identifications = cursor.fetchone()[0]
        print(f"🔍 Totale identificazioni: {total_identifications}")
        
        # 3. Statistiche per famiglia
        print("\n🏷️ SPECIE PER FAMIGLIA:")
        cursor.execute("""
            SELECT famiglia, COUNT(*) as count 
            FROM specie_ittiche 
            GROUP BY famiglia 
            ORDER BY count DESC
        """)
        families = cursor.fetchall()
        
        for family, count in families:
            print(f"  {family}: {count} specie")
        
        # 4. Statistiche per habitat
        print("\n🌊 SPECIE PER HABITAT:")
        cursor.execute("""
            SELECT habitat, COUNT(*) as count 
            FROM specie_ittiche 
            GROUP BY habitat 
            ORDER BY count DESC
        """)
        habitats = cursor.fetchall()
        
        for habitat, count in habitats:
            print(f"  {habitat}: {count} specie")
        
        # 5. Esempi di dati
        print("\n📝 ESEMPI DI SPECIE:")
        cursor.execute("SELECT nome_comune, nome_scientifico, famiglia FROM specie_ittiche LIMIT 5")
        examples = cursor.fetchall()
        
        for nome, scientifico, famiglia in examples:
            print(f"  {nome} ({scientifico}) - {famiglia}")
        
        # 6. Verifica integrità dati
        print("\n🔍 VERIFICA INTEGRITÀ DATI:")
        
        # Specie senza nome scientifico
        cursor.execute("SELECT COUNT(*) FROM specie_ittiche WHERE nome_scientifico IS NULL OR nome_scientifico = ''")
        missing_scientific = cursor.fetchone()[0]
        print(f"  Specie senza nome scientifico: {missing_scientific}")
        
        # Specie duplicate
        cursor.execute("""
            SELECT nome_scientifico, COUNT(*) 
            FROM specie_ittiche 
            GROUP BY nome_scientifico 
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        print(f"  Nomi scientifici duplicati: {len(duplicates)}")
        
        if duplicates:
            for scientific, count in duplicates:
                print(f"    ⚠️ {scientific}: {count} volte")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Errore verifica dati: {e}")

def run_database_tests():
    """Esegue test di funzionalità database"""
    print("\n🧪 TEST FUNZIONALITÀ DATABASE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect("pesca_webapp.db")
        cursor = conn.cursor()
        
        # Test 1: Inserimento nuova specie
        print("\n🧪 TEST 1: Inserimento nuova specie")
        try:
            cursor.execute("""
                INSERT INTO specie_ittiche 
                (nome_comune, nome_scientifico, famiglia, habitat, taglia_min, taglia_max)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("Test Fish", "Testus fishus", "Testidae", "Test Habitat", 10.0, 20.0))
            
            # Verifica inserimento
            cursor.execute("SELECT COUNT(*) FROM specie_ittiche WHERE nome_scientifico = 'Testus fishus'")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print("  ✅ Inserimento specie: SUCCESSO")
                
                # Rimuovi specie di test
                cursor.execute("DELETE FROM specie_ittiche WHERE nome_scientifico = 'Testus fishus'")
                print("  ✅ Rimozione specie di test: SUCCESSO")
            else:
                print("  ❌ Inserimento specie: FALLITO")
                
        except Exception as e:
            print(f"  ❌ Errore test inserimento: {e}")
        
        # Test 2: Ricerca specie
        print("\n🧪 TEST 2: Ricerca specie")
        try:
            cursor.execute("SELECT * FROM specie_ittiche WHERE famiglia = 'Salmonidae'")
            salmonids = cursor.fetchall()
            print(f"  ✅ Ricerca Salmonidae: {len(salmonids)} risultati")
        except Exception as e:
            print(f"  ❌ Errore test ricerca: {e}")
        
        # Test 3: Aggiornamento specie
        print("\n🧪 TEST 3: Aggiornamento specie")
        try:
            cursor.execute("""
                UPDATE specie_ittiche 
                SET note = 'Test update' 
                WHERE nome_scientifico = 'Salmo trutta'
            """)
            
            cursor.execute("SELECT note FROM specie_ittiche WHERE nome_scientifico = 'Salmo trutta'")
            note = cursor.fetchone()
            
            if note and 'Test update' in note[0]:
                print("  ✅ Aggiornamento specie: SUCCESSO")
                
                # Ripristina nota originale
                cursor.execute("""
                    UPDATE specie_ittiche 
                    SET note = 'Specie molto apprezzata per la pesca sportiva' 
                    WHERE nome_scientifico = 'Salmo trutta'
                """)
                print("  ✅ Ripristino nota originale: SUCCESSO")
            else:
                print("  ❌ Aggiornamento specie: FALLITO")
                
        except Exception as e:
            print(f"  ❌ Errore test aggiornamento: {e}")
        
        # Test 4: Inserimento identificazione
        print("\n🧪 TEST 4: Inserimento identificazione")
        try:
            cursor.execute("""
                INSERT INTO identificazioni_specie 
                (immagine_url, utente_id, specie_identificata, confidence_score, status)
                VALUES (?, ?, ?, ?, ?)
            """, ("test_image.jpg", "test_user", "Testus fishus", 0.95, "identificata"))
            
            # Verifica inserimento
            cursor.execute("SELECT COUNT(*) FROM identificazioni_specie WHERE immagine_url = 'test_image.jpg'")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print("  ✅ Inserimento identificazione: SUCCESSO")
                
                # Rimuovi identificazione di test
                cursor.execute("DELETE FROM identificazioni_specie WHERE immagine_url = 'test_image.jpg'")
                print("  ✅ Rimozione identificazione di test: SUCCESSO")
            else:
                print("  ❌ Inserimento identificazione: FALLITO")
                
        except Exception as e:
            print(f"  ❌ Errore test identificazione: {e}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Errore test funzionalità: {e}")

def main():
    """Funzione principale"""
    print("🚀 VERIFICA COMPLETA DATABASE PESCA WEBAPP")
    print("=" * 60)
    
    # Verifica struttura
    if verify_database_structure():
        # Verifica dati
        verify_database_data()
        
        # Esegui test
        run_database_tests()
        
        print("\n🎉 VERIFICA COMPLETATA!")
        print("=" * 60)
    else:
        print("\n❌ VERIFICA FALLITA - Database non valido!")

if __name__ == "__main__":
    main()
