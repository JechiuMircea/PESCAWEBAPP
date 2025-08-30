#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per aggiornare automaticamente le date nei file di tracking del progetto
Aggiorna PROJECT_MILESTONES.md e PROJECT_PROGRESS.md con la data corrente
"""

import os
import re
from datetime import datetime
from pathlib import Path

class ProjectDateUpdater:
    """Classe per aggiornare le date nei file di tracking"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.limite_chat_dir = self.project_root / "LimiteRaggiuntoChat"
        self.current_date = datetime.now()
        self.date_formats = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}'   # DD-MM-YYYY
        ]
        
    def update_file_dates(self, file_path):
        """Aggiorna le date in un singolo file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # Aggiorna date nel formato YYYY-MM-DD
            content = re.sub(
                r'(\d{4})-(\d{2})-(\d{2})',
                lambda m: self.update_date_if_old(m.group(1), m.group(2), m.group(3)),
                content
            )
            
            # Aggiorna date specifiche menzionate nel progetto
            content = self.update_specific_dates(content)
            
            # Se il contenuto è cambiato, scrivi il file
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ {file_path.name} - Date aggiornate")
                return True
            else:
                print(f"ℹ️  {file_path.name} - Nessuna data da aggiornare")
                return False
                
        except Exception as e:
            print(f"❌ Errore nell'aggiornamento di {file_path.name}: {e}")
            return False
    
    def update_date_if_old(self, year, month, day):
        """Aggiorna una data se è vecchia (prima del 2025)"""
        try:
            file_date = datetime(int(year), int(month), int(day))
            
            # Se la data è prima del 2025, aggiorna alla data corrente
            if file_date.year < 2025:
                return self.current_date.strftime('%Y-%m-%d')
            else:
                return f"{year}-{month}-{day}"
                
        except ValueError:
            return f"{year}-{month}-{day}"
    
    def update_specific_dates(self, content):
        """Aggiorna date specifiche menzionate nel progetto"""
        
        # Aggiorna "2025-01-27" con la data corrente
        content = re.sub(
            r'2025-01-27',
            self.current_date.strftime('%Y-%m-%d'),
            content
        )
        
        # Aggiorna "FishBase Integration COMPLETATA" con data corrente
        content = re.sub(
            r'### \d{4}-\d{2}-\d{2} - FishBase Integration COMPLETATA',
            f'### {self.current_date.strftime("%Y-%m-%d")} - FishBase Integration COMPLETATA',
            content
        )
        
        # Aggiorna "Ultimo Aggiornamento"
        content = re.sub(
            r'(\*\*Ultimo Aggiornamento:\*\* ).*?(\*\*)',
            r'\1' + self.current_date.strftime('%Y-%m-%d') + r' - FishBase Integration COMPLETATA\2',
            content
        )
        
        return content
    
    def update_all_tracking_files(self):
        """Aggiorna SOLO i file specifici del progetto con le date correnti"""
        print(f"🔄 Aggiornamento DATE SPECIFICHE progetto - {self.current_date.strftime('%Y-%m-%d')}")
        print("=" * 60)
        
        # Lista specifica dei file da aggiornare
        specific_files = [
            # Cartella LimiteRaggiuntoChat
            self.limite_chat_dir / "PROJECT_MILESTONES.md",
            self.limite_chat_dir / "PROJECT_PROGRESS.md",
            
            # File specifici nella root
            self.project_root / "StrutturalInteroProgetto.md",
            
            # File spostati in docs/project/
            self.project_root / "docs" / "project" / "PROJECT_CONTEXT.md",
            self.project_root / "docs" / "project" / "PROJECT_SPECIFICATIONS.md",
            self.project_root / "docs" / "project" / "PROJECT_TIMELINE.md",
            self.project_root / "docs" / "project" / "RISK_ASSESSMENT.md",
            self.project_root / "docs" / "project" / "timeline-comparison.md",
            
            # File spostati in docs/architecture/
            self.project_root / "docs" / "architecture" / "technical-stack.md"
        ]
        
        # Filtra solo i file che esistono
        files_to_update = [f for f in specific_files if f.exists()]
        
        updated_count = 0
        
        for file_path in files_to_update:
            if file_path.exists():
                if self.update_file_dates(file_path):
                    updated_count += 1
                    print(f"✅ {file_path.relative_to(self.project_root)} - Date aggiornate")
                else:
                    print(f"ℹ️  {file_path.relative_to(self.project_root)} - Nessuna data da aggiornare")
            else:
                print(f"⚠️  File non trovato: {file_path.name}")
        
        print("=" * 60)
        print(f"📊 Aggiornamento completato: {updated_count}/{len(files_to_update)} file aggiornati")
        
        if updated_count > 0:
            print(f"🎯 Tutte le date sono ora aggiornate al {self.current_date.strftime('%Y-%m-%d')}")
        
        return updated_count
    
    def show_current_project_status(self):
        """Mostra lo stato attuale del progetto"""
        print(f"\n📊 STATO ATTUALE PROGETTO:")
        print(f"📅 Data corrente: {self.current_date.strftime('%Y-%m-%d')}")
        print(f"📁 Directory progetto: {self.project_root.name}")
        print(f"📂 File tracking: {self.limite_chat_dir.name}/")
        print(f"🔍 Target specifici: LimiteRaggiuntoChat/ + 1 file root + 5 file docs/project/ + 1 file docs/architecture/")

def main():
    """Funzione principale"""
    updater = ProjectDateUpdater()
    
    # Mostra stato progetto
    updater.show_current_project_status()
    
    # Aggiorna date
    updated_files = updater.update_all_tracking_files()
    
    if updated_files > 0:
        print(f"\n🎉 Progetto aggiornato con successo!")
        print(f"📝 Ricorda di fare commit delle modifiche!")
    else:
        print(f"\nℹ️  Nessuna modifica necessaria!")

if __name__ == "__main__":
    main()
