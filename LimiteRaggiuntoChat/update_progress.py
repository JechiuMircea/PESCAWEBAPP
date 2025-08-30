#!/usr/bin/env python3
"""
Script per aggiornamento automatico del progress tracking del progetto WebApp Pesca
Questo script aggiorna automaticamente PROJECT_PROGRESS.md e PROJECT_MILESTONES.md
"""

import datetime
import os
import re
import hashlib
from pathlib import Path


class ProgressTracker:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent  # Torna alla root del progetto
        self.progress_file = self.project_root / "LimiteRaggiuntoChat" / "PROJECT_PROGRESS.md"
        self.milestones_file = self.project_root / "LimiteRaggiuntoChat" / "PROJECT_MILESTONES.md"
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
        
        # Trova la sezione "Dettaglio Operazioni Completate" con pattern più flessibile
        operations_section = re.search(r'(## 📝 DETTAGLIO OPERAZIONI COMPLETATE.*?)(## 🔄 Come Usare Questo File)', 
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
            print(f"✅ File PROJECT_PROGRESS.md aggiornato con successo!")
        else:
            print("❌ Sezione 'DETTAGLIO OPERAZIONI COMPLETATE' non trovata!")
            print("🔍 Pattern cercato: '## 📝 DETTAGLIO OPERAZIONI COMPLETATE'")
            
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

    def scan_project_changes(self):
        """
        Scansiona automaticamente tutte le modifiche del progetto
        usando timestamp, dimensioni e hash
        """
        print("🔍 Scansione automatica modifiche progetto...")
        
        changes = {
            'timestamp_changes': self._scan_timestamp_changes(),
            'size_changes': self._scan_size_changes(),
            'hash_changes': self._scan_hash_changes()
        }
        
        return changes

    def _scan_timestamp_changes(self):
        """
        Scanner timestamp - Controlla quando i file sono stati modificati
        """
        print("⏰ Scanner timestamp in corso...")
        timestamp_changes = {}
        
        # Cartelle da scansionare
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                timestamp_changes[folder] = self._get_recent_files(folder_path)
        
        return timestamp_changes

    def _scan_size_changes(self):
        """
        Scanner dimensioni - Controlla se i file sono cambiati di dimensione
        """
        print("📏 Scanner dimensioni in corso...")
        size_changes = {}
        
        # Cartelle da scansionare
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                size_changes[folder] = self._get_size_changes(folder_path)
        
        return size_changes

    def _scan_hash_changes(self):
        """
        Scanner hash - Controlla se il contenuto è cambiato
        """
        print("🔐 Scanner hash in corso...")
        hash_changes = {}
        
        # Cartelle da scansionare
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                hash_changes[folder] = self._get_hash_changes(folder_path)
        
        return hash_changes

    def _get_recent_files(self, folder_path, days=1):
        """
        Ottiene file modificati negli ultimi N giorni
        """
        recent_files = []
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
        
        for file_path in folder_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored_file(file_path):
                try:
                    mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > cutoff_time:
                        recent_files.append(str(file_path.relative_to(self.project_root)))
                except:
                    continue
        
        return recent_files

    def _get_size_changes(self, folder_path):
        """
        Ottiene file con dimensioni cambiate
        """
        size_changes = []
        
        for file_path in folder_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored_file(file_path):
                try:
                    size = file_path.stat().st_size
                    size_changes.append({
                        'file': str(file_path.relative_to(self.project_root)),
                        'size': size,
                        'size_kb': round(size / 1024, 2)
                    })
                except:
                    continue
        
        return size_changes

    def _get_hash_changes(self, folder_path):
        """
        Calcola hash dei file per rilevare cambiamenti di contenuto
        """
        hash_changes = []
        
        for file_path in folder_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored_file(file_path):
                try:
                    file_hash = self._calculate_file_hash(file_path)
                    hash_changes.append({
                        'file': str(file_path.relative_to(self.project_root)),
                        'hash': file_hash
                    })
                except:
                    continue
        
        return hash_changes

    def _calculate_file_hash(self, file_path):
        """
        Calcola hash MD5 di un file
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return "error"

    def _is_ignored_file(self, file_path):
        """
        Controlla se un file deve essere ignorato
        """
        ignored_patterns = [
            '__pycache__', '.pyc', '.pyo', '.pyd',
            'node_modules', '.git', '.DS_Store',
            '*.log', '*.tmp', '*.cache'
        ]
        
        file_str = str(file_path)
        for pattern in ignored_patterns:
            if pattern in file_str:
                return True
        
        return False

    def auto_update_progress(self):
        """
        Aggiorna automaticamente il progresso basandosi sulla scansione
        SOVRASCRIVE l'ultima entrata Auto-Scan per mantenere il file leggibile
        """
        print("🚀 Aggiornamento automatico progresso...")
        
        # Scansiona modifiche
        changes = self.scan_project_changes()
        
        # Crea report automatico
        operation_type = "Auto-Scan"
        description = "Scansione automatica modifiche progetto"
        
        # Dettagli basati sui risultati
        details = []
        if changes['timestamp_changes']:
            for folder, files in changes['timestamp_changes'].items():
                if files:
                    details.append(f"📁 {folder}: {len(files)} file modificati")
        
        # File modificati
        all_modified_files = []
        for folder, files in changes['timestamp_changes'].items():
            all_modified_files.extend(files)
        
        # SOVRASCRIVI l'ultima entrata Auto-Scan invece di aggiungerne una nuova
        self._update_or_replace_auto_scan(
            operation_type=operation_type,
            description=description,
            details="\n   - ".join(details) if details else "Nessuna modifica rilevata",
            files_modified=all_modified_files[:20],  # Limita a 20 file per leggibilità
            commands_executed=["python update_progress.py --auto"]
        )

    def _update_or_replace_auto_scan(self, operation_type, description, details, files_modified, commands_executed):
        """
        SOVRASCRIVE l'ultima entrata Auto-Scan invece di aggiungerne una nuova
        """
        if not self.progress_file.exists():
            print("❌ File PROJECT_PROGRESS.md non trovato!")
            return
            
        content = self.progress_file.read_text(encoding='utf-8')
        
        # Trova l'ultima entrata Auto-Scan per sostituirla
        auto_scan_pattern = r'(### \d{4}-\d{2}-\d{2} - Auto-Scan.*?)(?=### \d{4}-\d{2}-\d{2} -|$)'
        auto_scan_matches = list(re.finditer(auto_scan_pattern, content, re.DOTALL))
        
        if auto_scan_matches:
            # Sostituisci l'ultima entrata Auto-Scan
            last_auto_scan = auto_scan_matches[-1]
            old_content = last_auto_scan.group(1)
            
            # Crea nuova entrata Auto-Scan
            new_auto_scan = f"""### {self.current_date} - {operation_type}
**Operazioni Eseguite:**
1. **{operation_type}** - {description}
   - {details}
2. **File Modificati:**
"""
            
            if files_modified:
                for file in files_modified:
                    new_auto_scan += f"   - ✅ `{file}`\n"
            else:
                new_auto_scan += "   - Nessun file modificato\n"
                
            if commands_executed:
                new_auto_scan += f"3. **Comandi Eseguiti:**\n```bash"
                for cmd in commands_executed:
                    new_auto_scan += f"\n{cmd}"
                new_auto_scan += "\n```\n"
            
            # Sostituisci l'ultima entrata Auto-Scan
            updated_content = content.replace(old_content, new_auto_scan)
            
            # Aggiorna la data dell'ultimo aggiornamento
            updated_content = re.sub(
                r'(\*\*Ultimo Aggiornamento:\*\* )\d{4}-\d{2}-\d{2}',
                f'\\1{self.current_date}',
                updated_content
            )
            
            self.progress_file.write_text(updated_content, encoding='utf-8')
            print(f"✅ Ultima entrata Auto-Scan SOVRASCRITTA con successo!")
        else:
            # Se non ci sono entrate Auto-Scan precedenti, aggiungi la prima
            print("📝 Prima entrata Auto-Scan - aggiunta nuova sezione")
            self.add_operation(
                operation_type=operation_type,
                description=description,
                details=details,
                files_modified=files_modified,
                commands_executed=commands_executed
            )

def main():
    """Funzione principale per test dello script"""
    tracker = ProgressTracker()
    
    print("🚀 Progress Tracker - WebApp Pesca")
    print("=" * 50)
    
    # Test delle nuove funzionalità automatiche
    print("🔍 Test scanner automatici...")
    
    # 1. Scanner timestamp
    print("\n1️⃣ Test Scanner Timestamp:")
    timestamp_changes = tracker._scan_timestamp_changes()
    for folder, files in timestamp_changes.items():
        if files:
            print(f"   📁 {folder}: {len(files)} file modificati")
        else:
            print(f"   📁 {folder}: Nessuna modifica")
    
    # 2. Scanner dimensioni
    print("\n2️⃣ Test Scanner Dimensioni:")
    size_changes = tracker._scan_size_changes()
    for folder, files in size_changes.items():
        if files:
            print(f"   📁 {folder}: {len(files)} file analizzati")
        else:
            print(f"   📁 {folder}: Nessun file")
    
    # 3. Scanner hash
    print("\n3️⃣ Test Scanner Hash:")
    hash_changes = tracker._scan_hash_changes()
    for folder, files in hash_changes.items():
        if files:
            print(f"   📁 {folder}: {len(files)} file con hash calcolato")
        else:
            print(f"   📁 {folder}: Nessun file")
    
    # 4. Aggiornamento automatico
    print("\n4️⃣ Test Aggiornamento Automatico:")
    tracker.auto_update_progress()
    
    print("\n✅ Test scanner automatici completato!")

if __name__ == "__main__":
    main()
