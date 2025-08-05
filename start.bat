@echo off
title Text to Teamwork Converter
color 0A

echo.
echo ==========================================
echo  TEXT TO TEAMWORK CONVERTER
echo ==========================================
echo.
echo 🚀 Lancement de l'application...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 📥 Téléchargez Python depuis https://python.org
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo 🔧 Vérification des dépendances...
pip install -r requirements.txt >nul 2>&1

REM Lancer l'application
echo 🌐 Ouverture dans votre navigateur...
echo 📍 URL : http://localhost:8501
echo 🛑 Fermez cette fenêtre pour arrêter l'application
echo.
python -m streamlit run app.py --server.port 8501

pause 