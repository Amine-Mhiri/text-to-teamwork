# 🔐 Configuration Sécurisée OpenAI

## ⚠️ **IMPORTANT : Sécurité des clés API**

Votre clé OpenAI est sensible et ne doit **JAMAIS** être partagée publiquement. Voici comment la configurer de manière sécurisée.

---

## 🔑 **1. Obtenir votre clé OpenAI**

### **Étapes :**
1. Allez sur [platform.openai.com](https://platform.openai.com/api-keys)
2. Créez un compte ou connectez-vous
3. Cliquez **"Create new secret key"**
4. Copiez la clé (format : `sk-...`)
5. **⚠️ Sauvegardez-la, elle ne sera plus jamais affichée !**

### **💰 Coût :**
- GPT-4o-mini : ~0.15$ / 1M tokens (très économique)
- Usage typique : 0.01-0.05$ par conversion
- Crédit gratuit de 5$ pour nouveaux comptes

---

## 🏠 **2. Configuration Locale (Développement)**

### **Créer le fichier .env :**

```bash
# Dans votre dossier de projet, créez un fichier nommé exactement : .env
# (sans extension, juste .env)
```

### **Contenu du fichier .env :**

```bash
# ===================================================
# CONFIGURATION - Text to Teamwork Converter
# ===================================================

# 🤖 OpenAI Configuration (OBLIGATOIRE pour mode IA)
OPENAI_API_KEY=sk-votre-vraie-cle-ici

# 📊 Configuration App (optionnel)
APP_TITLE="Text to Teamwork Converter"
DEBUG=false

# ===================================================
# ⚠️  NE JAMAIS PARTAGER CE FICHIER !
# ===================================================
```

### **Étapes :**
1. **Créez le fichier** : `.env` dans le dossier principal
2. **Remplacez** `sk-votre-vraie-cle-ici` par votre vraie clé
3. **Sauvegardez** le fichier
4. **Testez** l'application localement

---

## ☁️ **3. Configuration Streamlit Cloud (Production)**

### **🔒 Variables d'environnement sécurisées**

Lors du déploiement sur Streamlit Cloud :

1. **Dans l'interface de déploiement :**
   - Cliquez **"Advanced settings"**
   - Section **"Secrets"**
   
2. **Ajoutez vos variables :**
   ```toml
   [general]
   OPENAI_API_KEY = "sk-votre-vraie-cle-ici"
   ```

3. **Déployez** : Les variables sont sécurisées et non-visibles

### **📸 Capture d'écran du processus :**

```
┌─────────────────────────────────────┐
│     Streamlit Cloud Deployment     │
├─────────────────────────────────────┤
│ Repository: text-to-teamwork        │
│ Branch: main                        │
│ Main file: app.py                   │
│                                     │
│ ⚙️  Advanced settings              │
│ ┌─────────────────────────────────┐ │
│ │ 🔒 Secrets                      │ │
│ │                                 │ │
│ │ OPENAI_API_KEY = "sk-..."       │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│           [Deploy] 🚀               │
└─────────────────────────────────────┘
```

---

## ✅ **4. Vérification de Sécurité**

### **✅ Checklist avant déploiement :**

- [ ] ✅ Fichier `.env` dans `.gitignore` 
- [ ] ✅ Aucun commit contenant la clé
- [ ] ✅ Variables configurées dans Streamlit Cloud
- [ ] ✅ Test local réussi
- [ ] ✅ Repository GitHub ne contient pas la clé

### **🔍 Vérifier le repository :**
```bash
# Chercher si votre clé est présente (ne devrait rien retourner)
git log --all -p | grep "sk-"
```

---

## 🛡️ **5. Bonnes Pratiques de Sécurité**

### **🔐 Rotation des clés :**
- Changez votre clé tous les 3-6 mois
- Désactivez les anciennes clés
- Utilisez des clés spécifiques par projet

### **💰 Monitoring des coûts :**
- Définissez des limites de dépenses
- Surveillez l'usage sur platform.openai.com
- Alertes automatiques recommandées

### **🚨 En cas de compromission :**
1. **Désactivez immédiatement** la clé sur OpenAI
2. **Générez une nouvelle** clé
3. **Mettez à jour** les variables d'environnement
4. **Vérifiez** les logs d'usage

---

## 🧪 **6. Test de Configuration**

### **Vérification locale :**

```bash
# Test avec votre clé configurée
streamlit run app.py

# Dans l'interface :
# 1. Cochez "Utiliser l'IA"
# 2. Collez un texte de test
# 3. Vérifiez "Parsing avec IA réussi"
```

### **Vérification déploiement :**

```bash
# Après déploiement Streamlit Cloud
# 1. Accédez à l'URL publique
# 2. Testez le mode IA
# 3. Vérifiez les logs de déploiement
```

---

## 🆘 **7. Dépannage**

### **❌ "Clé OpenAI manquante"**
- Vérifiez le nom de variable : `OPENAI_API_KEY`
- Vérifiez le format : `sk-...`
- Redémarrez l'application

### **❌ "Erreur API OpenAI"**
- Vérifiez le crédit disponible
- Testez la clé sur platform.openai.com
- Vérifiez les limites de quota

### **❌ "Mode classique forcé"**
- Variables d'environnement non chargées
- Fichier `.env` mal nommé ou mal placé
- Redéploiement Streamlit Cloud nécessaire

---

## 📞 **Support**

**Documentation OpenAI :** [platform.openai.com/docs](https://platform.openai.com/docs)  
**Streamlit Secrets :** [docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

---

## 🎯 **Résumé : Workflow Sécurisé**

1. **Développement** : Créez `.env` local avec votre clé
2. **Test** : Vérifiez que l'IA fonctionne localement  
3. **Git** : Committez SANS le fichier `.env`
4. **Déploiement** : Configurez les secrets Streamlit Cloud
5. **Production** : Testez l'URL publique avec IA

**🔒 Votre clé reste privée et sécurisée à chaque étape !** 