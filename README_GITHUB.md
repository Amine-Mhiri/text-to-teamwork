# 📋 Text to Teamwork Converter

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transformez instantanément vos textes de tâches structurées en fichiers Excel compatibles avec Teamwork Projects.**

![Text to Teamwork Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Text+to+Teamwork+Converter)

## 🎯 Fonctionnalités

- ✅ **Conversion automatique** : Texte structuré → Excel Teamwork
- 🎨 **Interface moderne** : Application web Streamlit intuitive  
- 📊 **Prévisualisation temps réel** : Vérifiez avant téléchargement
- 🔧 **Parser intelligent** : Reconnaît priorités, dépendances, critères
- 📥 **Export optimisé** : Fichier Excel prêt pour l'import Teamwork
- 🌐 **Multi-format** : Support numérotation hiérarchique et emojis

## 🚀 Utilisation

### **🌐 Application en ligne (Recommandé)**
👉 **[Lancer l'application](https://share.streamlit.io)**

### **💻 Installation locale**
```bash
git clone https://github.com/VOTRE-USERNAME/text-to-teamwork-converter.git
cd text-to-teamwork-converter
pip install -r requirements.txt
streamlit run app.py
```

## 📝 Format d'entrée

```
Nom de Votre Projet

2.5 – Tâche Principale
Description : Détails de la tâche principale
Priorité : Élevée

2.5.1 – Première sous-tâche
Description : Détails de la sous-tâche
Dépendance : 2.5
Priorité : Moyenne

2.5.2 – Deuxième sous-tâche
Description : Autres détails
Critère d'acceptation : Validation requise
```

## 📊 Résultat Excel

| TASKLIST | TASK | DESCRIPTION | PRIORITY |
|----------|------|-------------|----------|
| Tâche Principale | | Détails de la tâche principale | Élevée |
| | Première sous-tâche | Détails de la sous-tâche. Dépendance : Tâche Principale | Moyenne |
| | Deuxième sous-tâche | Autres détails. Critère d'acceptation : Validation requise | |

**✨ Compatible 100% avec l'import Teamwork Projects**

## 🔧 Fonctionnalités Avancées

### **Parser Intelligent**
- Reconnaissance automatique de la hiérarchie (2.5, 2.5.1, 2.5.2)
- Suppression automatique de la numérotation
- Extraction des priorités (Élevée, Moyenne, Faible)
- Gestion des dépendances et critères d'acceptation

### **Formats Supportés**
- **Numérotation** : `1.`, `2.5.1`, `•`, `-`, `✅`
- **Priorités** : Élevée, Haute, Moyenne, Faible (FR/EN)
- **Sections** : Description, Dépendance, Critère, Livrable, Risque

### **Interface Moderne**
- Prévisualisation instantanée
- Statistiques de projet
- Design responsive (mobile friendly)
- Aide contextuelle intégrée

## 🛠️ Stack Technique

- **Frontend** : Streamlit
- **Backend** : Python 3.8+
- **Parsing** : Regex + pandas
- **Export** : openpyxl
- **Déploiement** : Streamlit Cloud

## 📖 Documentation

- [Guide de démarrage rapide](GUIDE_DEMARRAGE.md)
- [Options de déploiement](OPTIONS_PARTAGE_EQUIPE.md)
- [Déploiement Streamlit Cloud](deploy_streamlit_cloud.md)

## 🤝 Contribution

Les contributions sont bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez votre branche feature (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## ⭐ Support

Si ce projet vous aide, n'hésitez pas à lui donner une étoile !

## 📞 Contact

Pour toute question ou suggestion, [créez une issue](https://github.com/VOTRE-USERNAME/text-to-teamwork-converter/issues).

---

**🚀 Développé pour simplifier la gestion de projet et l'intégration Teamwork.** 