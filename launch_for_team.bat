@echo off
title Text to Teamwork - Serveur Équipe
color 0A

echo.
echo ============================================
echo  TEXT TO TEAMWORK - SERVEUR ÉQUIPE
echo ============================================
echo.

REM Récupérer l'adresse IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :ip_found
)

:ip_found
REM Nettoyer l'IP (supprimer les espaces)
set IP=%IP: =%

echo 🌐 Démarrage du serveur pour votre équipe...
echo.
echo 📍 URL d'accès pour l'équipe : 
echo    http://%IP%:8501
echo.
echo 📋 Partagez cette URL avec votre équipe
echo 🔄 L'application se met à jour automatiquement
echo 🛑 Fermez cette fenêtre pour arrêter le serveur
echo.
echo ============================================
echo.

REM Lancer Streamlit accessible sur le réseau
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

pause 