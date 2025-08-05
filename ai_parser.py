import openai
import json
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import pandas as pd

# Charger les variables d'environnement
load_dotenv()

class AITaskParser:
    """
    Parser intelligent utilisant OpenAI pour mapper les tâches vers le format Teamwork.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le parser IA.
        
        Args:
            api_key: Clé API OpenAI (optionnel, peut être dans .env)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Erreur initialisation client OpenAI: {e}")
                self.client = None
        
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Construit le prompt système optimisé pour Teamwork."""
        return """Tu es un expert en gestion de projet et en parsing de données. Ton rôle est de convertir des textes de tâches en format Excel compatible avec Teamwork Projects.

RÈGLES STRICTES - HIÉRARCHIE TEAMWORK :

1. TÂCHE PRINCIPALE (TASKLIST) :
   - Va dans la colonne TASKLIST
   - Colonne TASK = VIDE (très important !)
   - Peut avoir une description
   - Exemple : TASKLIST="Publicité Digitale", TASK=""

2. SOUS-TÂCHES (TASK) :
   - Va dans la colonne TASK
   - Colonne TASKLIST = VIDE
   - Exemple : TASKLIST="", TASK="Définition du budget"

3. CRITÈRES, DÉPENDANCES, LIVRABLES :
   - NE SONT PAS des tâches séparées !
   - Doivent être intégrés dans la DESCRIPTION de la tâche concernée
   - Ne créent JAMAIS de ligne séparée

4. SUPPRESSION NUMÉROTATION :
   - "2.5 - Publicité" → "Publicité"
   - "2.5.1 - Budget" → "Budget"

EXEMPLE CORRECT :
Input: 
```
Campagne Marketing
1. Publicité Digitale
   Description: Gestion des campagnes
2. Définir budget
   Critère d'acceptation: Budget validé
   Priorité: Élevée
```

Output: [
  {"TASKLIST": "Publicité Digitale", "TASK": "", "DESCRIPTION": "Gestion des campagnes", "PRIORITY": ""},
  {"TASKLIST": "", "TASK": "Définir budget", "DESCRIPTION": "Critère d'acceptation : Budget validé", "PRIORITY": "High"}
]

ERREURS À ÉVITER :
❌ Créer des lignes pour "Critère d'acceptation"
❌ Mettre quelque chose dans TASK quand TASKLIST est rempli
❌ Créer des tâches pour les descriptions, dépendances, etc.

COLONNES TEAMWORK :
- TASKLIST : Tâche principale uniquement (TASK vide si rempli)
- TASK : Sous-tâches uniquement (TASKLIST vide si rempli)
- DESCRIPTION : Tout le contexte (critères, dépendances, détails)
- PRIORITY : High|Medium|Low
- Autres colonnes : toujours vides

RETOURNE UNIQUEMENT UN TABLEAU JSON VALIDE."""

    def parse_with_ai(self, text: str, project_title: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Parse le texte en utilisant OpenAI pour un mapping intelligent.
        
        Args:
            text: Texte contenant les tâches
            project_title: Titre du projet (optionnel)
            
        Returns:
            Liste de dictionnaires représentant les tâches
        """
        if not self.client:
            raise ValueError("Client OpenAI non initialisé. Vérifiez votre clé API.")
        
        try:
            # Prompt utilisateur avec contexte renforcé
            user_prompt = f"""Convertis ce texte au format Teamwork Excel en respectant STRICTEMENT les règles :

TEXTE À ANALYSER :
{text}

RÈGLES CRITIQUES :
1. Tâches principales → TASKLIST rempli, TASK = ""
2. Sous-tâches → TASKLIST = "", TASK rempli  
3. Critères/dépendances → dans DESCRIPTION, PAS en tâche séparée
4. Supprimer toute numérotation des noms
5. Une ligne = une vraie tâche, pas un élément descriptif

VALIDATION :
- Vérifier qu'aucune ligne n'a TASKLIST et TASK remplis simultanément
- Aucune ligne pour "Critère d'acceptation" seul
- Regrouper tous les détails dans DESCRIPTION

Retourne le JSON :"""

            # Appel à OpenAI GPT-4 avec le nouveau client
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Plus rapide et moins cher que gpt-4
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Faible pour consistance
                max_tokens=2000,
                response_format={"type": "json_object"}  # Force JSON
            )
            
            # Extraire et parser la réponse
            content = response.choices[0].message.content
            
            # Parser le JSON
            try:
                parsed_tasks = json.loads(content)
                
                # Si la réponse est dans un wrapper
                if isinstance(parsed_tasks, dict):
                    if 'tasks' in parsed_tasks:
                        parsed_tasks = parsed_tasks['tasks']
                    elif 'data' in parsed_tasks:
                        parsed_tasks = parsed_tasks['data']
                    else:
                        # Prendre la première liste trouvée
                        for value in parsed_tasks.values():
                            if isinstance(value, list):
                                parsed_tasks = value
                                break
                
                # Valider et nettoyer les résultats
                return self._validate_and_clean_tasks(parsed_tasks, project_title)
                
            except json.JSONDecodeError as e:
                print(f"Erreur parsing JSON: {e}")
                print(f"Contenu reçu: {content}")
                # Fallback vers parser manuel
                return []
                
        except Exception as e:
            print(f"Erreur OpenAI API: {e}")
            # Fallback vers parser manuel
            return []
    
    def _validate_and_clean_tasks(self, tasks: List[Dict], project_title: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Valide et nettoie les tâches retournées par l'IA avec corrections automatiques.
        
        Args:
            tasks: Liste des tâches brutes de l'IA
            project_title: Titre du projet pour fallback
            
        Returns:
            Liste des tâches validées et corrigées
        """
        if not isinstance(tasks, list):
            return []
        
        validated_tasks = []
        required_columns = [
            'TASKLIST', 'TASK', 'DESCRIPTION', 'ASSIGN TO', 
            'START DATE', 'DUE DATE', 'PRIORITY', 'ESTIMATED TIME', 
            'TAGS', 'STATUS'
        ]
        
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                continue
            
            # Créer une tâche validée avec toutes les colonnes
            validated_task = {}
            
            for col in required_columns:
                # Récupérer la valeur ou vide
                value = task.get(col, '')
                
                # Nettoyer les valeurs
                if isinstance(value, str):
                    value = value.strip()
                elif value is None:
                    value = ''
                else:
                    value = str(value).strip()
                
                validated_task[col] = value
            
            # VALIDATION CRITÈRES D'ACCEPTATION - Filtrer les tâches qui ne sont que des critères
            task_name = validated_task['TASK'].lower() if validated_task['TASK'] else ''
            tasklist_name = validated_task['TASKLIST'].lower() if validated_task['TASKLIST'] else ''
            
            # Ignorer les lignes qui sont juste des critères/descriptions
            if any(keyword in task_name for keyword in ['critère', 'dépendance', 'livrable', 'risque']) and len(task_name) < 50:
                print(f"⚠️ Ligne ignorée (critère non-tâche) : {validated_task['TASK']}")
                continue
                
            if any(keyword in tasklist_name for keyword in ['critère', 'dépendance', 'livrable', 'risque']) and len(tasklist_name) < 50:
                print(f"⚠️ Ligne ignorée (critère non-tâche) : {validated_task['TASKLIST']}")
                continue
            
            # CORRECTION HIÉRARCHIE - Règle exclusive TASKLIST vs TASK
            if validated_task['TASKLIST'] and validated_task['TASK']:
                print(f"🔧 Correction hiérarchie : {validated_task['TASKLIST']} | {validated_task['TASK']}")
                # Si les deux sont remplis, priorité au TASKLIST (tâche principale)
                validated_task['TASK'] = ''
            
            # Si c'est la première tâche et pas de TASKLIST, utiliser project_title
            if i == 0 and not validated_task['TASKLIST'] and not validated_task['TASK'] and project_title:
                validated_task['TASKLIST'] = project_title
            
            # Ignorer les tâches complètement vides
            if not validated_task['TASKLIST'] and not validated_task['TASK']:
                continue
            
            # Valider les priorités
            priority = validated_task['PRIORITY'].lower()
            if priority in ['élevée', 'haute', 'high', 'elevee', 'urgent', 'urgente']:
                validated_task['PRIORITY'] = 'High'
            elif priority in ['moyenne', 'medium', 'moyen', 'normale', 'normal']:
                validated_task['PRIORITY'] = 'Medium'
            elif priority in ['faible', 'basse', 'low', 'bas']:
                validated_task['PRIORITY'] = 'Low'
            elif priority:
                # Garder tel quel si pas reconnu mais pas vide
                validated_task['PRIORITY'] = validated_task['PRIORITY']
            else:
                validated_task['PRIORITY'] = ''
            
            validated_tasks.append(validated_task)
        
        return validated_tasks

    def is_available(self) -> bool:
        """Vérifie si l'API OpenAI est disponible."""
        return bool(self.client)
    
    def test_connection(self) -> bool:
        """Teste la connexion à l'API OpenAI."""
        if not self.client:
            return False
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False

# Fonctions utilitaires pour l'interface
def create_ai_parser(api_key: str = None) -> AITaskParser:
    """Créer une instance du parser IA."""
    return AITaskParser(api_key=api_key)

def parse_text_with_ai(text: str, api_key: str = None, project_title: str = None) -> pd.DataFrame:
    """
    Parse un texte avec l'IA et retourne un DataFrame.
    
    Args:
        text: Texte à parser
        api_key: Clé API OpenAI
        project_title: Titre du projet
        
    Returns:
        DataFrame avec les tâches
    """
    try:
        parser = AITaskParser(api_key=api_key)
        tasks = parser.parse_with_ai(text, project_title)
        
        if tasks:
            return pd.DataFrame(tasks)
        else:
            # Retourner DataFrame vide avec bonnes colonnes
            columns = [
                'TASKLIST', 'TASK', 'DESCRIPTION', 'ASSIGN TO', 
                'START DATE', 'DUE DATE', 'PRIORITY', 'ESTIMATED TIME', 
                'TAGS', 'STATUS'
            ]
            return pd.DataFrame(columns=columns)
            
    except Exception as e:
        print(f"Erreur parsing IA: {e}")
        # Retourner DataFrame vide
        columns = [
            'TASKLIST', 'TASK', 'DESCRIPTION', 'ASSIGN TO', 
            'START DATE', 'DUE DATE', 'PRIORITY', 'ESTIMATED TIME', 
            'TAGS', 'STATUS'
        ]
        return pd.DataFrame(columns=columns) 