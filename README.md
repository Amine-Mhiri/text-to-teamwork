# 📋 Text to Teamwork Converter

Transformez instantanément vos textes de tâches structurées en fichiers Excel compatibles avec **Teamwork Projects**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Fonctionnalités

- ✅ **Conversion automatique** : Texte structuré → Excel Teamwork
- 🎨 **Interface moderne** : Application web Streamlit intuitive
- 📊 **Prévisualisation en temps réel** : Vérifiez avant téléchargement
- 🔧 **Parser intelligent** : Reconnaît priorités, dépendances, critères
- 📥 **Export optimisé** : Fichier Excel prêt pour l'import Teamwork
- 🌐 **Multi-format** : Support numérotation variée et emojis

## 📋 Structure Excel Compatible

| TASKLIST | TASK | DESCRIPTION | ASSIGN TO | START DATE | DUE DATE | PRIORITY | ESTIMATED TIME | TAGS | STATUS |
|----------|------|-------------|-----------|------------|-----------|----------|----------------|------|--------|
| Projet   | Tâche 1 | Détails... |           |            |           | Élevée   |                |      |        |

## 🚀 Installation Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/text-to-teamwork.git
cd text-to-teamwork
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

## 📖 Guide d'Utilisation

### Format de Texte Attendu

Votre texte doit suivre cette structure :

```
Titre du Projet

1. Première tâche
   Description : Détails de la tâche
   Priorité : Élevée
   Critère d'acceptation : Validation requise

2. Deuxième tâche
   Description : Autre description
   Dépendance : 1
   Priorité : Moyenne
```

### Éléments Reconnus Automatiquement

#### Numérotation Supportée
- `1.`, `2.`, `3.` (numérotation classique)
- `a)`, `b)`, `c)` (lettres)
- `•`, `-` (puces)
- `✅`, `✓` (cases cochées)

#### Sections Spéciales
- **Description** : Informations principales de la tâche
- **Priorité** : Élevée, Moyenne, Faible (français/anglais)
- **Dépendance** : Liens entre tâches
- **Critère d'acceptation** : Conditions de validation
- **Livrable** : Éléments à produire
- **Risque** : Points d'attention

### Workflow Recommandé

1. **Préparez votre texte** avec la structure recommandée
2. **Collez-le** dans l'interface web
3. **Vérifiez** la prévisualisation automatique
4. **Ajustez** si nécessaire
5. **Téléchargez** le fichier Excel
6. **Importez** directement dans Teamwork Projects

## 💡 Exemple Complet

### Texte d'Entrée
```
Campagne Réseaux Sociaux – Liste de Tâches

📌 Objectif général :
Planifier et lancer une campagne de visibilité sur Instagram et LinkedIn.

✅ Liste des Tâches :
1. Définir le concept de la campagne  
   Description : Trouver un message central et un thème visuel  
   Critère d'acceptation : Concept validé par l'équipe

2. Créer le calendrier éditorial  
   Description : Planifier les publications sur 4 semaines  
   Dépendance : 1  
   Priorité : Élevée  
   Critère d'acceptation : Calendrier complet avec visuels et dates

3. Rédiger les textes des publications  
   Description : Écrire les textes adaptés à chaque plateforme  
   Dépendance : 2  
   Critère d'acceptation : Textes sans fautes et optimisés SEO
```

### Résultat Excel
| TASKLIST | TASK | DESCRIPTION | PRIORITY |
|----------|------|-------------|----------|
| Campagne Réseaux Sociaux | Définir le concept de la campagne | Trouver un message central et un thème visuel. Critère d'acceptation : Concept validé par l'équipe. | |
| | Créer le calendrier éditorial | Planifier les publications sur 4 semaines. Dépendance : Définir le concept de la campagne. Critère d'acceptation : Calendrier complet avec visuels et dates. | Élevée |
| | Rédiger les textes des publications | Écrire les textes adaptés à chaque plateforme. Dépendance : Créer le calendrier éditorial. Critère d'acceptation : Textes sans fautes et optimisés SEO. | |

## 🛠️ Utilisation Avancée

### Mode CLI (Script Python)
```python
from text_to_teamwork import TextToTeamworkConverter

converter = TextToTeamworkConverter()

# Lire depuis un fichier
with open('mon_projet.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Convertir et sauvegarder
converter.convert_to_excel(text, 'output.xlsx')
print("Conversion terminée !")
```

### Personnalisation
Le parser peut être étendu en modifiant les patterns dans `text_to_teamwork.py` :

```python
# Ajouter de nouveaux patterns de tâches
self.task_patterns.append(r'^→\s*(.+)')  # Support pour → 

# Ajouter des mots-clés de priorité
self.priority_keywords['urgent'] = 'Élevée'
```

## 🔧 Configuration

### Variables d'Environnement (Optionnel)
Créez un fichier `.env` pour la configuration :

```bash
# Pour future intégration OpenAI (optionnel)
OPENAI_API_KEY=your_api_key_here

# Configuration Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

## 📁 Structure du Projet

```
text-to-teamwork/
├── app.py                 # Interface Streamlit
├── text_to_teamwork.py    # Logique de conversion
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── .env.example          # Variables d'environnement
└── examples/             # Exemples de fichiers
    └── sample_text.txt   # Exemple de texte structuré
```

## 🚀 Déploiement

### Streamlit Cloud
1. Poussez votre code sur GitHub
2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)
3. Déployez directement depuis votre repository

### Docker (Optionnel)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🐛 Dépannage

### Erreurs Communes

**ImportError: No module named 'streamlit'**
```bash
pip install streamlit
```

**Erreur d'encodage**
- Assurez-vous que vos fichiers texte sont en UTF-8
- Sur Windows, utilisez `encoding='utf-8'` lors de la lecture

**Tâches non détectées**
- Vérifiez la numérotation (1., 2., etc.)
- Assurez-vous qu'il y a un espace après le numéro
- Utilisez les formats supportés (voir documentation)

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📊 Fonctionnalités Futures

- [ ] Support import depuis fichiers .docx
- [ ] Intégration API Teamwork directe
- [ ] Export vers autres formats (Asana, Trello)
- [ ] Parser IA avec OpenAI GPT
- [ ] Interface mobile responsive
- [ ] Mode batch pour plusieurs projets

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [Streamlit](https://streamlit.io/) pour l'interface web
- [Pandas](https://pandas.pydata.org/) pour la manipulation des données
- [OpenPyXL](https://openpyxl.readthedocs.io/) pour la génération Excel

---

**⭐ N'hésitez pas à star le projet si il vous aide !**

Pour toute question ou suggestion : [Créer une issue](https://github.com/votre-username/text-to-teamwork/issues) 