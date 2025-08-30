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
        
        # Prima pulisci le duplicazioni esistenti
        content = self._clean_duplicate_operations(content)
        
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
        """Aggiorna il file PROJECT_MILESTONES.md"""
        if not self.milestones_file.exists():
            print("❌ File PROJECT_MILESTONES.md non trovato!")
            return
            
        print("🔄 Aggiornamento PROJECT_MILESTONES.md...")
        
        # Aggiorna automaticamente le milestone completate
        self._auto_update_milestones()
        
    def _auto_update_milestones(self):
        """Aggiorna automaticamente le milestone basandosi sui file esistenti"""
        print("🔍 Rilevamento automatico milestone completate...")
        
        # 1. Controlla se React è stato setup
        if self._check_react_setup_complete():
            self._mark_milestone_complete("Setup React", "PROJECT_MILESTONES.md")
            self._mark_milestone_complete("Setup React", "PROJECT_PROGRESS.md")
            self._update_progress_percentage("Frontend React", 25, "PROJECT_MILESTONES.md")
            self._update_progress_percentage("Setup Frontend", 25, "PROJECT_PROGRESS.md")
            print("✅ Milestone 'Setup React' marcata come completata!")
        
        # 2. Controlla se i componenti UI sono stati creati
        if self._check_ui_components_complete():
            self._mark_milestone_complete("Componenti UI", "PROJECT_MILESTONES.md")
            self._mark_milestone_complete("Creazione componenti UI base", "PROJECT_PROGRESS.md")
            self._update_progress_percentage("Frontend React", 75, "PROJECT_MILESTONES.md")
            self._update_progress_percentage("Setup Frontend", 75, "PROJECT_PROGRESS.md")
            print("✅ Milestone 'Componenti UI' marcata come completata!")
        
        # 3. Controlla se l'integrazione API è completa
        if self._check_api_integration_complete():
            self._mark_milestone_complete("Integrazione API", "PROJECT_MILESTONES.md")
            self._mark_milestone_complete("Integrazione con API backend", "PROJECT_PROGRESS.md")
            self._update_progress_percentage("Frontend React", 100, "PROJECT_MILESTONES.md")
            self._update_progress_percentage("Setup Frontend", 100, "PROJECT_PROGRESS.md")
            print("✅ Milestone 'Integrazione API' marcata come completata!")
            
    def _check_react_setup_complete(self):
        """Controlla se React è stato setup completamente"""
        frontend_dir = self.project_root / "frontend"
        
        # Controlla se esistono i file essenziali per React
        essential_files = [
            "package.json",
            "tsconfig.json", 
            "vite.config.ts",
            "src/App.tsx",
            "src/main.tsx"
        ]
        
        for file_path in essential_files:
            if not (frontend_dir / file_path).exists():
                return False
        return True
        
    def _check_ui_components_complete(self):
        """Controlla se i componenti UI sono stati creati"""
        components_dir = self.project_root / "frontend" / "src" / "components"
        
        # Controlla se esistono i componenti principali
        required_components = [
            "Dashboard.tsx",
            "Header.tsx", 
            "Navigation.tsx",
            "FishCatalog.tsx",
            "FishIdentifier.tsx",
            "DatabaseManager.tsx"
        ]
        
        for component in required_components:
            if not (components_dir / component).exists():
                return False
        return True
        
    def _check_api_integration_complete(self):
        """Controlla se l'integrazione API è completa"""
        # Per ora controlla solo se esistono i file di configurazione API
        frontend_dir = self.project_root / "frontend"
        
        # Controlla se esiste un file di configurazione API o servizi
        api_files = [
            "src/services/api.ts",
            "src/api/config.ts",
            "src/utils/api.ts"
        ]
        
        for api_file in api_files:
            if (frontend_dir / api_file).exists():
                return True
        return False
        
    def _mark_milestone_complete(self, milestone_name, file_path):
        """Marca una milestone come completata cambiando [ ] in [x]"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ File {file_path} non trovato!")
            return
            
        content = file_path.read_text(encoding='utf-8')
        
        # Pattern per trovare checkbox non completati
        # Gestisce sia "Setup React" che "Setup React - TypeScript + Vite"
        pattern = rf'(- \[ \]) (.*?{re.escape(milestone_name)}.*?)(?=\n|$)'
        replacement = rf'- [x] \2 ✅'
        
        # Aggiorna il contenuto
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✅ Milestone '{milestone_name}' marcata come completata in {file_path.name}")
        else:
            print(f"⚠️ Milestone '{milestone_name}' non trovata in {file_path.name}")
            
    def _update_progress_percentage(self, phase_name, new_percentage, file_path):
        """Aggiorna la percentuale di progresso di una fase"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ File {file_path} non trovato!")
            return
            
        content = file_path.read_text(encoding='utf-8')
        
        # Pattern per trovare percentuali (0%), (25%), (75%), (100%)
        pattern = rf'({re.escape(phase_name)} \([0-9]+%\))'
        replacement = rf'{phase_name} ({new_percentage}%)'
        
        # Aggiorna il contenuto
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✅ Percentuale '{phase_name}' aggiornata al {new_percentage}% in {file_path.name}")
        else:
            print(f"⚠️ Fase '{phase_name}' non trovata in {file_path.name}")
            
    def auto_update_milestones(self):
        """Funzione principale per aggiornamento automatico milestone"""
        print("🚀 Aggiornamento automatico milestone...")
        
        # Aggiorna automaticamente le milestone
        self._auto_update_milestones()
        
        print("✅ Aggiornamento milestone completato!")
        
    def scan_project_changes(self):
        """Scansiona le modifiche del progetto usando tutti i metodi disponibili"""
        print("🔍 Scansione completa modifiche progetto...")
        
        changes = {
            'timestamp_changes': self._scan_timestamp_changes(),
            'size_changes': self._scan_size_changes(),
            'hash_changes': self._scan_hash_changes()
        }
        
        return changes
        
    def _scan_timestamp_changes(self):
        """Scansiona modifiche basate sui timestamp dei file"""
        print("   📅 Scanner timestamp...")
        
        changes = {}
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                changes[folder] = []
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        changes[folder].append(str(file_path.relative_to(self.project_root)))
        
        return changes
        
    def _scan_size_changes(self):
        """Scansiona modifiche basate sulle dimensioni dei file"""
        print("   📏 Scanner dimensioni...")
        
        changes = {}
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                changes[folder] = []
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        changes[folder].append(str(file_path.relative_to(self.project_root)))
        
        return changes
        
    def _scan_hash_changes(self):
        """Scansiona modifiche basate sugli hash dei file"""
        print("   🔐 Scanner hash...")
        
        changes = {}
        folders_to_scan = ['app', 'frontend', 'docs', 'backend', 'scripts']
        
        for folder in folders_to_scan:
            folder_path = self.project_root / folder
            if folder_path.exists():
                changes[folder] = []
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        changes[folder].append(str(file_path.relative_to(self.project_root)))
        
        return changes

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

    def _clean_duplicate_operations(self, content):
        """
        Pulisce le operazioni duplicate nel file
        """
        print("🧹 Pulizia operazioni duplicate...")
        
        # Trova tutte le operazioni
        operation_pattern = r'(### \d{4}-\d{2}-\d{2} - .*?)(?=### \d{4}-\d{2}-\d{2} -|## 🔄 Come Usare Questo File|$)'
        operations = re.findall(operation_pattern, content, re.DOTALL)
        
        # Raggruppa per tipo e data
        unique_operations = {}
        for op in operations:
            # Estrai data e tipo
            match = re.search(r'### (\d{4}-\d{2}-\d{2}) - (.+?)\n', op)
            if match:
                date = match.group(1)
                op_type = match.group(2)
                key = f"{date}_{op_type}"
                
                # Mantieni solo l'ultima versione di ogni operazione
                unique_operations[key] = op
        
        # Ricostruisci il contenuto senza duplicazioni
        if unique_operations:
            # Trova l'inizio della sezione operazioni
            start_match = re.search(r'(## 📝 DETTAGLIO OPERAZIONI COMPLETATE\n)', content)
            if start_match:
                start_section = start_match.group(1)
                
                # Ricostruisci con operazioni uniche
                new_operations = start_section
                for op in unique_operations.values():
                    new_operations += op + "\n"
                
                # Sostituisci la sezione operazioni
                old_section_pattern = r'(## 📝 DETTAGLIO OPERAZIONI COMPLETATE\n).*?(## 🔄 Come Usare Questo File)'
                new_content = re.sub(old_section_pattern, new_operations + r'\2', content, flags=re.DOTALL)
                
                print(f"✅ Rimosse {len(operations) - len(unique_operations)} operazioni duplicate")
                return new_content
        
        return content

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
        
        # 🆕 AGGIORNAMENTO AUTOMATICO MILESTONE
        print("\n🎯 Aggiornamento automatico milestone...")
        self.auto_update_milestones()

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
    
    # 5. 🆕 Test Aggiornamento Milestone
    print("\n5️⃣ Test Aggiornamento Milestone:")
    tracker.auto_update_milestones()
    
    print("\n✅ Test scanner automatici completato!")

if __name__ == "__main__":
    main()
