#!/usr/bin/env python3
"""
Script per pulire le operazioni duplicate in PROJECT_PROGRESS.md
"""

import re
from pathlib import Path

def clean_duplicates():
    """Pulisce le operazioni duplicate nel file PROJECT_PROGRESS.md"""
    
    progress_file = Path("PROJECT_PROGRESS.md")
    
    if not progress_file.exists():
        print("❌ File PROJECT_PROGRESS.md non trovato!")
        return
    
    print("🧹 Pulizia operazioni duplicate...")
    
    content = progress_file.read_text(encoding='utf-8')
    
    # Trova tutte le operazioni
    operation_pattern = r'(### \d{4}-\d{2}-\d{2} - .*?)(?=### \d{4}-\d{2}-\d{2} -|## 🔄 COME USARE QUESTO FILE|$)'
    operations = re.findall(operation_pattern, content, re.DOTALL)
    
    print(f"📋 Trovate {len(operations)} operazioni totali")
    
    # Raggruppa per tipo e data
    unique_operations = {}
    for op in operations:
        # Estrai data e tipo
        match = re.search(r'### (\d{4}-\d{2}-\d{2}) - (.+?)\n', op)
        if match:
            date = match.group(1)
            op_type = match.group(2).strip()
            key = f"{date}_{op_type}"
            
            # Mantieni solo l'ultima versione di ogni operazione
            unique_operations[key] = op
            
    print(f"✨ Operazioni uniche: {len(unique_operations)}")
    print(f"🗑️ Operazioni duplicate da rimuovere: {len(operations) - len(unique_operations)}")
    
    # Ricostruisci il contenuto senza duplicazioni
    if unique_operations:
        # Trova l'inizio della sezione operazioni
        start_match = re.search(r'(## 📝 DETTAGLIO OPERAZIONI COMPLETATE\n)', content)
        if start_match:
            # Trova tutto prima della sezione operazioni
            before_operations = content[:start_match.start()]
            
            # Ricostruisci la sezione operazioni
            new_operations = "## 📝 DETTAGLIO OPERAZIONI COMPLETATE\n\n"
            
            # Ordina le operazioni per data (più recenti prima)
            sorted_operations = sorted(unique_operations.items(), 
                                     key=lambda x: x[0], reverse=True)
            
            for key, op in sorted_operations:
                new_operations += op.strip() + "\n\n"
            
            # Trova la sezione "COME USARE QUESTO FILE"
            come_usare_match = re.search(r'(## 🔄 COME USARE QUESTO FILE.*)', content, re.DOTALL)
            if come_usare_match:
                come_usare_section = come_usare_match.group(1)
            else:
                come_usare_section = ""
            
            # Ricostruisci tutto il file
            new_content = before_operations + new_operations + "---\n\n" + come_usare_section
            
            # Scrivi il file pulito
            progress_file.write_text(new_content, encoding='utf-8')
            
            print(f"✅ File pulito con successo!")
            print(f"📊 Rimosse {len(operations) - len(unique_operations)} operazioni duplicate")
            
            # Mostra riassunto operazioni uniche
            print("\n📋 OPERAZIONI UNICHE MANTENUTE:")
            for key, _ in sorted_operations:
                date, op_type = key.split("_", 1)
                print(f"   - {date}: {op_type}")
                
        else:
            print("❌ Sezione 'DETTAGLIO OPERAZIONI COMPLETATE' non trovata!")
    else:
        print("❌ Nessuna operazione trovata!")

if __name__ == "__main__":
    clean_duplicates()
