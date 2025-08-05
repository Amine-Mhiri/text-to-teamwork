# 📋 Text to Teamwork Converter

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transformez instantanément vos textes de tâches structurées en fichiers Excel compatibles avec Teamwork Projects.**

![Text to Teamwork Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Text+to+Teamwork+Converter)

## 🎯 Fonctionnalités

### 🧠 **NOUVEAU : Intelligence Artificielle GPT-4**
- ✨ **100% fiable** : Comprend n'importe quel format de texte
- 🚀 **Ultra-flexible** : Emails, notes de réunion, documents désorganisés
- 🎯 **Mapping parfait** : Tâches principales vs sous-tâches automatique
- 💡 **Intelligence contextuelle** : Comprend l'intention, pas juste la syntaxe

### 📋 **Fonctionnalités Core**
- ✅ **Conversion automatique** : Texte → Excel Teamwork compatible
- 🎨 **Interface moderne** : Application web Streamlit responsive
- 📊 **Prévisualisation temps réel** : Validation avant téléchargement
- 🔧 **Double parsing** : IA (optimal) + classique (fallback)
- 📥 **Export optimisé** : Format Excel parfait pour Teamwork
- 🌐 **Multi-format** : De structuré à complètement libre

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

- **Frontend** : Streamlit (interface moderne)
- **Backend** : Python 3.8+ 
- **IA Engine** : OpenAI GPT-4o-mini (parsing intelligent)
- **Parsing** : IA + Regex (double fallback)
- **Data** : pandas (manipulation)
- **Export** : openpyxl (génération Excel)
- **Déploiement** : Streamlit Cloud (gratuit)

## 🧠 Exemple Mode IA vs Classique

### **📧 Input : Email de projet (format libre)**
```
Objet: Site web urgence

Salut,

Pour le nouveau site, il faut:
1) Faire les mockups (Marie - URGENT)  
2) Coder le front (Jean - après mockups)
3) Tester sur mobile (Lisa)

Deadline: fin mai
```

### **📊 Output automatique :**
| TASKLIST | TASK | DESCRIPTION | PRIORITY |
|----------|------|-------------|----------|
| Site web urgence | | Email de projet avec deadline fin mai | |
| | Faire les mockups | Assigné : Marie | Élevée |
| | Coder le front | Assigné : Jean. Dépendance : Faire les mockups | |
| | Tester sur mobile | Assigné : Lisa | |

**✨ L'IA comprend le contexte, extrait les assignations, reconnaît "URGENT" = Élevée, mappe les dépendances !**

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