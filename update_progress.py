#!/usr/bin/env python3
"""
Script per aggiornamento automatico del progress tracking del progetto WebApp Pesca
Questo script aggiorna automaticamente PROJECT_PROGRESS.md e PROJECT_MILESTONES.md
"""

import os
import datetime
import re
from pathlib import Path

class ProgressTracker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.progress_file = self.project_root / "PROJECT_PROGRESS.md"
        self.milestones_file = self.project_root / "PROJECT_MILESTONES.md"
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def add_operation(self, operation_type, description, details=None, files_modified=None, commands_executed=None):
        """
        Aggiunge una nuova operazione al progress tracking
        
        Args:
            operation_type (str): Tipo di operazione (es. "Setup", "Development", "Testing")
            description (str): Descrizione dell'operazione
            details (str, optional): Dettagli aggiuntivi
            files_modified (list, optional): Lista file modificati
            commands_executed (list, optional): Lista comandi eseguiti
        """
        print(f"🔄 Aggiornamento progress tracking: {operation_type} - {description}")
        
        # Aggiorna PROJECT_PROGRESS.md
        self._update_progress_file(operation_type, description, details, files_modified, commands_executed)
        
        # Aggiorna PROJECT_MILESTONES.md se necessario
        self._update_milestones_file(operation_type, description)
        
        print("✅ Progress tracking aggiornato con successo!")
        
    def _update_progress_file(self, operation_type, description, details, files_modified, commands_executed):
        """Aggiorna il file PROJECT_PROGRESS.md"""
        if not self.progress_file.exists():
            print("❌ File PROJECT_PROGRESS.md non trovato!")
            return
            
        content = self.progress_file.read_text(encoding='utf-8')
        
        # Trova la sezione "Dettaglio Operazioni Completate"
        operations_section = re.search(r'(## 📝 Dettaglio Operazioni Completate.*?)(## 🎯 Prossimi Step Immediati)', 
                                     content, re.DOTALL)
        
        if operations_section:
            # Crea la nuova operazione
            new_operation = f"""
### {self.current_date} - {operation_type}
**Operazioni Eseguite:**
1. **{operation_type}** - {description}"""
            
            if details:
                new_operation += f"\n   - {details}"
                
            if files_modified:
                new_operation += f"\n2. **File Modificati:**"
                for file in files_modified:
                    new_operation += f"\n   - ✅ `{file}`"
                    
            if commands_executed:
                new_operation += f"\n3. **Comandi Eseguiti:**"
                new_operation += "\n```bash"
                for cmd in commands_executed:
                    new_operation += f"\n{cmd}"
                new_operation += "\n```"
                
            new_operation += "\n"
            
            # Inserisci la nuova operazione dopo l'ultima esistente
            updated_content = content.replace(
                operations_section.group(1),
                operations_section.group(1) + new_operation
            )
            
            # Aggiorna la data dell'ultimo aggiornamento
            updated_content = re.sub(
                r'(\*\*Ultimo Aggiornamento:\*\* )\d{4}-\d{2}-\d{2}',
                f'\\1{self.current_date}',
                updated_content
            )
            
            self.progress_file.write_text(updated_content, encoding='utf-8')
            
    def _update_milestones_file(self, operation_type, description):
        """Aggiorna il file PROJECT_MILESTONES.md se necessario"""
        if not self.milestones_file.exists():
            return
            
        content = self.milestones_file.read_text(encoding='utf-8')
        
        # Aggiorna la data dell'ultimo aggiornamento
        updated_content = re.sub(
            r'(\*\*Ultimo Aggiornamento:\*\* )\d{4}-\d{2}-\d{2}',
            f'\\1{self.current_date}',
            content
        )
        
        self.milestones_file.write_text(updated_content, encoding='utf-8')
        
    def mark_milestone_complete(self, milestone_path):
        """
        Marca una milestone come completata
        
        Args:
            milestone_path (str): Percorso della milestone (es. "2.1", "3.2")
        """
        if not self.milestones_file.exists():
            print("❌ File PROJECT_MILESTONES.md non trovato!")
            return
            
        content = self.milestones_file.read_text(encoding='utf-8')
        
        # Trova e marca la milestone come completata
        pattern = rf'(\[ \] \*\*{milestone_path}\*\* - .*?)(\n)'
        replacement = r'[x] **\1** ✅\2'
        
        updated_content = re.sub(pattern, replacement, content)
        
        if updated_content != content:
            self.milestones_file.write_text(updated_content, encoding='utf-8')
            print(f"✅ Milestone {milestone_path} marcata come completata!")
        else:
            print(f"❌ Milestone {milestone_path} non trovata!")
            
    def update_progress_percentage(self, phase, new_percentage):
        """
        Aggiorna la percentuale di progresso di una fase
        
        Args:
            phase (str): Nome della fase (es. "Backend Core", "Frontend")
            new_percentage (int): Nuova percentuale (0-100)
        """
        if not self.milestones_file.exists():
            return
            
        content = self.milestones_file.read_text(encoding='utf-8')
        
        # Aggiorna la percentuale nella tabella
        pattern = rf'(\| \*\*{phase}\*\* \| .*? \| )\d+%(\| .*? \|)'
        replacement = rf'\1{new_percentage}%\2'
        
        updated_content = re.sub(pattern, replacement, content)
        
        if updated_content != content:
            self.milestones_file.write_text(updated_content, encoding='utf-8')
            print(f"📊 Progresso {phase} aggiornato al {new_percentage}%")

def main():
    """Funzione principale per test dello script"""
    tracker = ProgressTracker()
    
    print("🚀 Progress Tracker - WebApp Pesca")
    print("=" * 50)
    
    # Esempio di utilizzo
    tracker.add_operation(
        operation_type="Setup",
        description="Configurazione ambiente di sviluppo",
        details="Setup completo ambiente Python e dipendenze",
        files_modified=["requirements.txt", "backend/app/main.py"],
        commands_executed=["pip install -r requirements.txt", "python -m uvicorn app.main:app --reload"]
    )
    
    print("\n✅ Script di esempio completato!")

if __name__ == "__main__":
    main()
