#!/usr/bin/env python3
"""
Script di test per l'API Pesca WebApp
Testa le principali funzionalità dell'API
"""

import requests
import json
import time

# Configurazione
BASE_URL = "http://127.0.0.1:8080"  # Porta corretta come da PROJECT_CONTEXT.md
API_URL = f"{BASE_URL}/docs"

def test_health_endpoints():
    """Testa gli endpoint di health check"""
    print("🔍 Testando endpoint di health...")
    
    # Test endpoint live
    response = requests.get(f"{BASE_URL}/health/live")
    if response.status_code == 200:
        print("✅ /health/live: OK")
    else:
        print(f"❌ /health/live: FAILED - {response.status_code}")
    
    # Test endpoint ready
    response = requests.get(f"{BASE_URL}/health/ready")
    if response.status_code == 200:
        print("✅ /health/ready: OK")
    else:
        print(f"❌ /health/ready: FAILED - {response.status_code}")

def test_specie_endpoints():
    """Testa gli endpoint delle specie ittiche"""
    print("\n🐟 Testando endpoint delle specie...")
    
    # Test lista specie
    response = requests.get(f"{BASE_URL}/specie/")
    if response.status_code == 200:
        specie = response.json()
        print(f"✅ /specie/: OK - Trovate {len(specie)} specie")
        
        # Mostra la prima specie se disponibile
        if specie:
            prima_specie = specie[0]
            print(f"   Prima specie: {prima_specie['nome_comune']} ({prima_specie['nome_scientifico']})")
    else:
        print(f"❌ /specie/: FAILED - {response.status_code}")
    
    # Test ricerca specie
    response = requests.get(f"{BASE_URL}/specie/search/Trota")
    if response.status_code == 200:
        risultati = response.json()
        print(f"✅ /specie/search/Trota: OK - Trovati {len(risultati)} risultati")
    else:
        print(f"❌ /specie/search/Trota: FAILED - {response.status_code}")

def test_identificazioni_endpoints():
    """Testa gli endpoint delle identificazioni"""
    print("\n🔍 Testando endpoint delle identificazioni...")
    
    # Test statistiche
    response = requests.get(f"{BASE_URL}/identificazioni/stats/overview")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ /identificazioni/stats/overview: OK")
        print(f"   Statistiche: {stats}")
    else:
        print(f"❌ /identificazioni/stats/overview: FAILED - {response.status_code}")
    
    # Test creazione identificazione (simulata)
    test_data = {
        "immagine_url": "https://example.com/test-fish.jpg",
        "utente_id": "test_user_123"
    }
    
    response = requests.post(
        f"{BASE_URL}/identificazioni/",
        json=test_data
    )
    
    if response.status_code == 201:
        identificazione = response.json()
        print(f"✅ /identificazioni/ (POST): OK")
        print(f"   ID: {identificazione['id']}")
        print(f"   Specie: {identificazione['specie_identificata']}")
        print(f"   Confidence: {identificazione['confidence_score']}")
        print(f"   Status: {identificazione['status']}")
    else:
        print(f"❌ /identificazioni/ (POST): FAILED - {response.status_code}")
        print(f"   Response: {response.text}")

def test_root_endpoint():
    """Testa l'endpoint root"""
    print("\n🏠 Testando endpoint root...")
    
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ /: OK")
        print(f"   Message: {data['message']}")
        print(f"   Version: {data['version']}")
    else:
        print(f"❌ /: FAILED - {response.status_code}")

def main():
    """Funzione principale di test"""
    print("🚀 Avvio test API Pesca WebApp")
    print("=" * 50)
    print(f"🌐 Testando API su: {BASE_URL}")
    print("=" * 50)
    
    # Aspetta che l'API sia pronta
    print("⏳ Aspettando che l'API sia pronta...")
    time.sleep(3)
    
    try:
        # Test endpoint root
        test_root_endpoint()
        
        # Test health endpoints
        test_health_endpoints()
        
        # Test specie endpoints
        test_specie_endpoints()
        
        # Test identificazioni endpoints
        test_identificazioni_endpoints()
        
        print("\n" + "=" * 50)
        print("🎯 Test completati!")
        print(f"📖 Documentazione API disponibile su: {API_URL}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Errore di connessione: l'API non è ancora pronta")
        print("   Assicurati che l'API sia in esecuzione con: uvicorn backend.app.main:app --host 127.0.0.1 --port 8080")
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")

if __name__ == "__main__":
    main()
