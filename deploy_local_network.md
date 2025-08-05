# 🏢 Déploiement Réseau Local (Entreprise)

## 📋 Configuration serveur local :

### 1. **Sur le PC serveur** (celui qui va héberger)
```bash
# Lancer l'app accessible sur le réseau
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 2. **Trouver l'IP du serveur**
```bash
# Windows
ipconfig
# Chercher "Adresse IPv4" (ex: 192.168.1.100)

# Linux/Mac  
ifconfig
```

### 3. **Partager l'URL avec l'équipe**
URL d'accès : `http://IP-DU-SERVEUR:8501`
Exemple : `http://192.168.1.100:8501`

### 4. **Script de démarrage automatique**
Créer `launch_server.bat` :
```batch
@echo off
echo Lancement du Text to Teamwork Converter pour l'équipe...
echo URL d'accès : http://192.168.1.100:8501
echo.
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
pause
```

## ⚙️ **Configuration avancée**

### **Démarrage automatique (Windows)**
```batch
# Ajouter au démarrage Windows
# Créer un raccourci de launch_server.bat dans :
# C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

### **Pare-feu**
- Autoriser le port 8501 dans le pare-feu Windows
- Ou désactiver temporairement pour tester

## 💡 **Avantages :**
- ✅ Privé et sécurisé
- ✅ Rapide (réseau local)
- ✅ Contrôle total
- ✅ Pas de limite d'utilisateurs

## ⚠️ **Requis :**
- PC serveur toujours allumé
- Même réseau pour tous les utilisateurs 