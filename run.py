#!/usr/bin/env python3
"""
Script de lancement pour Text to Teamwork Converter
Usage: python run.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Vérifier que toutes les dépendances sont installées."""
    try:
        import streamlit
        import pandas
        import openpyxl
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")
        print("🔧 Installation des dépendances...")
        
        # Installer les dépendances
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        return True

def main():
    """Lance l'application Streamlit."""
    print("🚀 Lancement de Text to Teamwork Converter...")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_requirements():
        print("❌ Impossible d'installer les dépendances")
        sys.exit(1)
    
    # Vérifier que app.py existe
    if not Path("app.py").exists():
        print("❌ Fichier app.py introuvable")
        sys.exit(1)
    
    print("🌐 Ouverture de l'application dans votre navigateur...")
    print("📍 URL : http://localhost:8501")
    print("🛑 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 50)
    
    try:
        # Lancer Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 