#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per analizzare il venv e verificare le best practice
Analizza pacchetti, dipendenze, strumenti di sviluppo e identifica problemi
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import importlib.metadata
import importlib

class VenvAnalyzer:
    """Classe per analizzare il venv e verificare le best practice"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / "venv"
        self.venv_site_packages = self.venv_path / "Lib" / "site-packages"
        self.current_date = datetime.now()
        
        # Colori per output
        self.colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def print_header(self, title):
        """Stampa header colorato"""
        print(f"\n{self.colors['bold']}{self.colors['blue']}{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}{self.colors['end']}")
    
    def print_section(self, title):
        """Stampa sezione colorata"""
        print(f"\n{self.colors['cyan']}📋 {title}{self.colors['end']}")
        print("-" * 40)
    
    def print_success(self, message):
        """Stampa messaggio di successo"""
        print(f"{self.colors['green']}✅ {message}{self.colors['end']}")
    
    def print_warning(self, message):
        """Stampa messaggio di warning"""
        print(f"{self.colors['yellow']}⚠️  {message}{self.colors['end']}")
    
    def print_error(self, message):
        """Stampa messaggio di errore"""
        print(f"{self.colors['red']}❌ {message}{self.colors['end']}")
    
    def print_info(self, message):
        """Stampa messaggio informativo"""
        print(f"{self.colors['purple']}ℹ️  {message}{self.colors['end']}")
    
    def analyze_venv_structure(self):
        """Analizza la struttura del venv"""
        self.print_header("ANALISI STRUTTURA VENV")
        
        if not self.venv_path.exists():
            self.print_error(f"VENV non trovato in: {self.venv_path}")
            return False
        
        self.print_success(f"VENV trovato in: {self.venv_path}")
        
        # Analizza cartelle principali
        main_dirs = ['Include', 'Lib', 'Scripts', 'pyvenv.cfg']
        for dir_name in main_dirs:
            dir_path = self.venv_path / dir_name
            if dir_path.exists():
                if dir_path.is_dir():
                    file_count = len(list(dir_path.rglob('*')))
                    self.print_info(f"{dir_name}/: {file_count:,} elementi")
                else:
                    self.print_info(f"{dir_name}: File di configurazione")
            else:
                self.print_warning(f"{dir_name}/: Mancante")
        
        # Analizza site-packages
        if self.venv_site_packages.exists():
            packages = list(self.venv_site_packages.glob('*'))
            self.print_info(f"Site-packages: {len(packages)} pacchetti")
        else:
            self.print_error("Site-packages non trovato")
            return False
        
        return True
    
    def analyze_installed_packages(self):
        """Analizza i pacchetti installati"""
        self.print_header("ANALISI PACCHETTI INSTALLATI")
        
        try:
            # Lista pacchetti installati
            installed_packages = [importlib.metadata.Distribution.from_name(d) for d in importlib.metadata.distributions()]
            
            self.print_info(f"Totale pacchetti: {len(installed_packages)}")
            
            # Categorizza pacchetti
            categories = {
                'web_framework': [],
                'database': [],
                'ml_ai': [],
                'dev_tools': [],
                'utilities': [],
                'other': []
            }
            
            for package in installed_packages:
                name = package.metadata['Name'].lower()
                
                if any(x in name for x in ['fastapi', 'starlette', 'uvicorn', 'django', 'flask']):
                    categories['web_framework'].append(package)
                elif any(x in name for x in ['sqlalchemy', 'psycopg2', 'pymongo', 'redis']):
                    categories['database'].append(package)
                elif any(x in name for x in ['tensorflow', 'torch', 'sklearn', 'opencv', 'rekognition']):
                    categories['ml_ai'].append(package)
                elif any(x in name for x in ['black', 'flake8', 'isort', 'pre-commit', 'pytest']):
                    categories['dev_tools'].append(package)
                elif any(x in name for x in ['requests', 'pandas', 'numpy', 'pillow']):
                    categories['utilities'].append(package)
                else:
                    categories['other'].append(package)
            
            # Mostra categorie
            for category, packages in categories.items():
                if packages:
                    self.print_section(f"{category.upper().replace('_', ' ')} ({len(packages)} pacchetti)")
                    for package in packages:
                        version = package.metadata['Version']
                        if 'dev' in version or 'alpha' in version or 'beta' in version:
                            self.print_warning(f"  {package.metadata['Name']} {version} (VERSIONE INSTABILE)")
                        else:
                            self.print_success(f"  {package.metadata['Name']} {version}")
            
        except Exception as e:
            self.print_error(f"Errore nell'analisi pacchetti: {e}")
    
    def analyze_dependencies(self):
        """Analizza le dipendenze e i conflitti"""
        self.print_header("ANALISI DIPENDENZE E CONFLITTI")
        
        try:
            # Verifica requirements.txt
            requirements_file = self.project_root / "backend" / "requirements.txt"
            if requirements_file.exists():
                self.print_success("requirements.txt trovato")
                
                with open(requirements_file, 'r') as f:
                    requirements = f.read().splitlines()
                
                self.print_info(f"Dipendenze produzione: {len(requirements)}")
                
                # Verifica se tutti i pacchetti sono installati
                missing_packages = []
                for req in requirements:
                    if req.strip() and not req.startswith('#'):
                        package_name = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
                        try:
                            importlib.import_module(package_name.replace('-', '_'))
                        except ImportError:
                            missing_packages.append(package_name)
                
                if missing_packages:
                    self.print_warning(f"Pacchetti mancanti: {', '.join(missing_packages)}")
                else:
                    self.print_success("Tutti i pacchetti di produzione sono installati")
            else:
                self.print_warning("requirements.txt non trovato")
            
            # Verifica requirements-dev.txt
            dev_requirements_file = self.project_root / "backend" / "requirements-dev.txt"
            if dev_requirements_file.exists():
                self.print_success("requirements-dev.txt trovato")
                
                with open(dev_requirements_file, 'r') as f:
                    dev_requirements = f.read().splitlines()
                
                self.print_info(f"Dipendenze sviluppo: {len(dev_requirements)}")
            else:
                self.print_warning("requirements-dev.txt non trovato")
                
        except Exception as e:
            self.print_error(f"Errore nell'analisi dipendenze: {e}")
    
    def test_development_tools(self):
        """Testa gli strumenti di sviluppo"""
        self.print_header("TEST STRUMENTI DI SVILUPPO")
        
        tools_to_test = {
            'isort': 'Ordinatore import',
            'black': 'Formattatore codice',
            'flake8': 'Linter codice',
            'pre-commit': 'Pre-commit hooks'
        }
        
        for tool, description in tools_to_test.items():
            try:
                result = subprocess.run([tool, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.print_success(f"{tool}: {version} - {description}")
                else:
                    self.print_warning(f"{tool}: Errore - {result.stderr.strip()}")
            except FileNotFoundError:
                self.print_error(f"{tool}: Non installato - {description}")
            except subprocess.TimeoutExpired:
                self.print_warning(f"{tool}: Timeout durante il test")
            except Exception as e:
                self.print_error(f"{tool}: Errore - {e}")
    
    def check_potential_issues(self):
        """Controlla potenziali problemi"""
        self.print_header("CONTROLLO PROBLEMI POTENZIALI")
        
        issues_found = []
        
        # Controlla versioni duplicate
        try:
            packages = [importlib.metadata.Distribution.from_name(d) for d in importlib.metadata.distributions()]
            package_names = [p.metadata['Name'].lower() for p in packages]
            
            duplicates = []
            seen = set()
            for name in package_names:
                if name in seen:
                    duplicates.append(name)
                seen.add(name)
            
            if duplicates:
                self.print_warning(f"Pacchetti con nomi simili: {', '.join(duplicates)}")
                issues_found.append("Pacchetti con nomi simili")
            
            # Controlla versioni instabili
            unstable_packages = []
            for package in packages:
                version = package.metadata['Version'].lower()
                if any(x in version for x in ['dev', 'alpha', 'beta', 'rc']):
                    unstable_packages.append(f"{package.metadata['Name']} {package.metadata['Version']}")
            
            if unstable_packages:
                self.print_warning(f"Versioni instabili: {', '.join(unstable_packages)}")
                issues_found.append("Versioni instabili")
            
            # Controlla conflitti noti
            known_conflicts = [
                ('pydantic', 'pydantic-core'),
                ('fastapi', 'starlette'),
                ('uvicorn', 'watchfiles')
            ]
            
            for pkg1, pkg2 in known_conflicts:
                try:
                    pkg1_ver = importlib.metadata.version(pkg1)
                    pkg2_ver = importlib.metadata.version(pkg2)
                    self.print_info(f"Compatibilità {pkg1} {pkg1_ver} + {pkg2} {pkg2_ver}")
                except importlib.metadata.PackageNotFoundError:
                    pass
            
        except Exception as e:
            self.print_error(f"Errore nel controllo problemi: {e}")
        
        if not issues_found:
            self.print_success("Nessun problema potenziale identificato")
        else:
            self.print_warning(f"Problemi identificati: {len(issues_found)}")
    
    def generate_recommendations(self):
        """Genera raccomandazioni per migliorare il venv"""
        self.print_header("RACCOMANDAZIONI E BEST PRACTICE")
        
        recommendations = [
            "✅ Usa sempre versioni specifiche nei requirements.txt",
            "✅ Mantieni separati requirements.txt e requirements-dev.txt",
            "✅ Aggiorna regolarmente i pacchetti per la sicurezza",
            "✅ Usa pre-commit hooks per mantenere la qualità del codice",
            "✅ Testa regolarmente gli strumenti di sviluppo",
            "✅ Documenta le versioni dei pacchetti critici",
            "✅ Usa virtual environment per ogni progetto",
            "✅ Non installare pacchetti globalmente"
        ]
        
        for rec in recommendations:
            print(f"  {rec}")
        
        self.print_section("PROSSIMI PASSI CONSIGLIATI")
        next_steps = [
            "1. Verifica che tutti i tool di sviluppo funzionino",
            "2. Testa il progetto con le dipendenze attuali",
            "3. Considera l'aggiornamento di pacchetti obsoleti",
            "4. Configura pre-commit hooks se non già fatto",
            "5. Documenta le versioni dei pacchetti critici"
        ]
        
        for step in next_steps:
            print(f"  {step}")
    
    def run_full_analysis(self):
        """Esegue l'analisi completa del venv"""
        print(f"{self.colors['bold']}{self.colors['blue']}")
        print("🚀 ANALISI COMPLETA VENV - BEST PRACTICE VERIFIER")
        print(f"📅 Data analisi: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Progetto: {self.project_root.name}")
        print(f"{self.colors['end']}")
        
        # Esegui tutte le analisi
        if self.analyze_venv_structure():
            self.analyze_installed_packages()
            self.analyze_dependencies()
            self.test_development_tools()
            self.check_potential_issues()
            self.generate_recommendations()
        
        print(f"\n{self.colors['bold']}{self.colors['green']}")
        print("🎉 ANALISI VENV COMPLETATA!")
        print(f"{self.colors['end']}")

def main():
    """Funzione principale"""
    analyzer = VenvAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
