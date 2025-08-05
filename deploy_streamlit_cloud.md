# 🚀 Déploiement sur Streamlit Cloud (Gratuit)

## 📋 Étapes de déploiement :

### 1. **Préparer le code pour GitHub**
```bash
# Dans votre dossier de projet
git init
git add .
git commit -m "Initial commit - Text to Teamwork Converter"
```

### 2. **Créer un repository GitHub**
- Allez sur [github.com](https://github.com) et créez un compte si nécessaire
- Cliquez "New repository"
- Nom : `text-to-teamwork-converter`
- Public ✅ (requis pour Streamlit Cloud gratuit)
- Cliquez "Create repository"

### 3. **Pousser le code**
```bash
git remote add origin https://github.com/VOTRE-USERNAME/text-to-teamwork-converter.git
git branch -M main
git push -u origin main
```

### 4. **Déployer sur Streamlit Cloud**
- Allez sur [share.streamlit.io](https://share.streamlit.io)
- Connectez-vous avec GitHub
- Cliquez "New app"
- Repository : `VOTRE-USERNAME/text-to-teamwork-converter`
- Branch : `main`
- Main file path : `app.py`
- Cliquez "Deploy!"

### 5. **Partager avec l'équipe**
Votre app sera disponible à : `https://VOTRE-USERNAME-text-to-teamwork-converter-app-xyz123.streamlit.app`

## ⚡ **Temps total : 10 minutes**
## 💰 **Coût : Gratuit**
## 👥 **Utilisateurs : Illimités** 