import pandas as pd
import re
import openai
import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from ai_parser import AITaskParser

# Charger les variables d'environnement
load_dotenv()

class TextToTeamworkConverter:
    """
    Convertit du texte structuré en fichier Excel compatible avec Teamwork Projects.
    
    Structure Excel requise:
    TASKLIST | TASK | DESCRIPTION | ASSIGN TO | START DATE | DUE DATE | PRIORITY | ESTIMATED TIME | TAGS | STATUS
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, use_ai: bool = True):
        self.columns = [
            'TASKLIST', 'TASK', 'DESCRIPTION', 'ASSIGN TO', 
            'START DATE', 'DUE DATE', 'PRIORITY', 'ESTIMATED TIME', 
            'TAGS', 'STATUS'
        ]
        
        # Configuration IA
        self.use_ai = use_ai
        self.ai_parser = None
        
        if use_ai:
            try:
                self.ai_parser = AITaskParser(api_key=openai_api_key)
                # Tester la connexion
                if not self.ai_parser.is_available():
                    print("⚠️ Clé OpenAI manquante - Utilisation du parser classique")
                    self.use_ai = False
                    self.ai_parser = None
            except Exception as e:
                print(f"⚠️ Erreur initialisation IA - Utilisation du parser classique: {e}")
                self.use_ai = False
                self.ai_parser = None
        
        # Patterns pour identifier les éléments avec numérotation hiérarchique
        self.task_patterns = [
            r'^\d+(?:\.\d+)*\.?\s*[–-]?\s*(.+)',  # 1. ou 2.5.1 – Tâche (capture la numérotation hiérarchique)
            r'^[-•]\s*(.+)',    # - Tâche ou • Tâche
            r'^[✓✅]\s*(.+)',   # ✓ Tâche ou ✅ Tâche
            r'^[a-zA-Z]\)\s*(.+)', # a) Tâche
        ]
        
        # Patterns à ignorer (ne sont pas des tâches)
        self.ignore_patterns = [
            r'critère\s*d[\'\'""]acceptation',
            r'dépendance\s*:',
            r'livrable\s*:',
            r'risque\s*:',
            r'description\s*:',
        ]
        
        # Pattern pour détecter le niveau de hiérarchie
        self.hierarchy_pattern = r'^(\d+(?:\.\d+)*)'
        
        self.priority_keywords = {
            'élevée': 'Élevée',
            'haute': 'Élevée', 
            'high': 'Élevée',
            'moyenne': 'Moyenne',
            'medium': 'Moyenne',
            'faible': 'Faible',
            'basse': 'Faible',
            'low': 'Faible'
        }
        
    def get_task_hierarchy_level(self, task_text: str) -> Tuple[int, str]:
        """Retourne le niveau de hiérarchie et le numéro de la tâche."""
        match = re.match(self.hierarchy_pattern, task_text.strip())
        if match:
            number = match.group(1)
            level = len(number.split('.'))  # 2.5.1 = niveau 3, 2.5 = niveau 2, 2 = niveau 1
            return level, number
        return 1, ""
    
    def clean_task_name(self, task_text: str) -> str:
        """Nettoie le nom de la tâche en supprimant la numérotation."""
        for pattern in self.task_patterns:
            match = re.match(pattern, task_text.strip())
            if match:
                return match.group(1).strip()
        return task_text.strip()
    
    def is_main_task(self, task_text: str) -> bool:
        """Détermine si c'est une tâche principale (niveau 2 comme 2.5) vs sous-tâche (niveau 3+ comme 2.5.1)."""
        level, _ = self.get_task_hierarchy_level(task_text)
        return level == 2  # Niveau 2 = tâche principale (ex: 2.5), niveau 3+ = sous-tâche (ex: 2.5.1)
    
    def should_ignore_line(self, line: str) -> bool:
        """Vérifie si une ligne doit être ignorée car ce n'est pas une vraie tâche."""
        line_lower = line.lower().strip()
        
        # Ignorer les lignes vides ou très courtes
        if len(line_lower) < 3:
            return True
        
        # Vérifier les patterns à ignorer
        for pattern in self.ignore_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                return True
        
        # Ignorer les lignes qui commencent par des emojis de description
        if re.match(r'^\s*[🔗📋✅❗⚠️]\s*(critère|dépendance|livrable|risque)', line_lower):
            return True
            
        return False
    
    def extract_priority(self, text: str) -> Optional[str]:
        """Extrait la priorité du texte."""
        text_lower = text.lower()
        for keyword, priority in self.priority_keywords.items():
            if keyword in text_lower:
                return priority
        return None
    
    def extract_project_title(self, text: str) -> str:
        """Extrait le titre du projet du texte."""
        lines = text.strip().split('\n')
        
        # Chercher un titre en première ligne ou avec des marqueurs
        for line in lines[:5]:  # Chercher dans les 5 premières lignes
            line = line.strip()
            if not line:
                continue
                
            # Supprimer les marqueurs communs et emojis
            line = re.sub(r'^[#\*\-=✅✓•]+\s*', '', line)
            line = re.sub(r'\s*[#\*\-=]+$', '', line)
            line = re.sub(r'📌.*?:', '', line)
            line = re.sub(r'🎯.*?:', '', line)
            
            # Nettoyer "Liste des Tâches" qui est souvent un en-tête, pas le titre du projet
            if 'liste' in line.lower() and 'tâche' in line.lower():
                continue
            
            if line and len(line) > 5:  # Titre raisonnable
                return line.strip()
        
        return "Projet"
    
    def parse_task_details(self, task_lines: List[str]) -> Dict[str, str]:
        """Parse les détails d'une tâche à partir de plusieurs lignes."""
        details = {
            'description': [],
            'priority': None,
            'dependencies': [],
            'criteria': [],
            'deliverables': [],
            'risks': []
        }
        
        current_section = 'description'
        
        for line in task_lines[1:]:  # Skip la première ligne (nom de la tâche)
            line = line.strip()
            if not line:
                continue
                
            # Identifier le type d'information
            if re.search(r'description\s*:', line, re.IGNORECASE):
                current_section = 'description'
                content = re.sub(r'.*description\s*:\s*', '', line, flags=re.IGNORECASE)
                if content:
                    details['description'].append(content)
            elif re.search(r'priorité\s*:', line, re.IGNORECASE):
                priority_text = re.sub(r'.*priorité\s*:\s*', '', line, flags=re.IGNORECASE)
                details['priority'] = self.extract_priority(priority_text)
            elif re.search(r'dépendance', line, re.IGNORECASE):
                current_section = 'dependencies'
                content = re.sub(r'.*dépendance[s]?\s*:\s*', '', line, flags=re.IGNORECASE)
                if content:
                    details['dependencies'].append(content)
            elif re.search(r'critère', line, re.IGNORECASE):
                current_section = 'criteria'
                content = re.sub(r'.*critère.*?:\s*', '', line, flags=re.IGNORECASE)
                if content:
                    details['criteria'].append(content)
            elif re.search(r'livrable', line, re.IGNORECASE):
                current_section = 'deliverables'
                content = re.sub(r'.*livrable[s]?\s*:\s*', '', line, flags=re.IGNORECASE)
                if content:
                    details['deliverables'].append(content)
            elif re.search(r'risque', line, re.IGNORECASE):
                current_section = 'risks'
                content = re.sub(r'.*risque[s]?\s*:\s*', '', line, flags=re.IGNORECASE)
                if content:
                    details['risks'].append(content)
            else:
                # Ajouter à la section courante
                details[current_section].append(line)
        
        return details
    
    def build_description(self, details: Dict[str, str]) -> str:
        """Construit la description complète à partir des détails."""
        description_parts = []
        
        # Description principale
        if details['description']:
            description_parts.extend(details['description'])
        
        # Dépendances
        if details['dependencies']:
            dep_text = "Dépendance : " + ", ".join(details['dependencies'])
            description_parts.append(dep_text)
        
        # Critères d'acceptation
        if details['criteria']:
            criteria_text = "Critère d'acceptation : " + " ".join(details['criteria'])
            description_parts.append(criteria_text)
        
        # Livrables
        if details['deliverables']:
            deliverable_text = "Livrables : " + ", ".join(details['deliverables'])
            description_parts.append(deliverable_text)
        
        # Risques
        if details['risks']:
            risk_text = "Risques : " + ", ".join(details['risks'])
            description_parts.append(risk_text)
        
        return ". ".join(description_parts) + ("." if description_parts else "")
    
    def parse_text_to_tasks(self, text: str) -> List[Dict[str, str]]:
        """Parse le texte pour extraire les tâches avec gestion hiérarchique."""
        lines = text.split('\n')
        project_title = self.extract_project_title(text)
        
        tasks = []
        current_task_lines = []
        current_main_task = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Ignorer les lignes qui ne sont pas des vraies tâches
            if self.should_ignore_line(line):
                # Ajouter à la tâche courante comme description si on en a une
                if current_task_lines:
                    current_task_lines.append(line)
                continue
            
            # Vérifier si c'est une nouvelle tâche
            is_task = False
            for pattern in self.task_patterns:
                if re.match(pattern, line):
                    is_task = True
                    break
            
            if is_task:
                # Traiter la tâche précédente si elle existe
                if current_task_lines:
                    task_data = self.process_task_group(current_task_lines, project_title, current_main_task, len(tasks) == 0)
                    tasks.extend(task_data)
                
                # Déterminer si c'est une tâche principale
                if self.is_main_task(line):
                    current_main_task = self.clean_task_name(line)
                else:
                    current_main_task = None
                
                # Commencer une nouvelle tâche
                current_task_lines = [line]
            else:
                # Ajouter à la tâche courante
                if current_task_lines:
                    current_task_lines.append(line)
        
        # Traiter la dernière tâche
        if current_task_lines:
            task_data = self.process_task_group(current_task_lines, project_title, current_main_task, len(tasks) == 0)
            tasks.extend(task_data)
        
        return tasks
    
    def process_task_group(self, task_lines: List[str], project_title: str, current_main_task: Optional[str], is_first_task: bool) -> List[Dict[str, str]]:
        """Traite un groupe de lignes représentant une tâche avec gestion hiérarchique."""
        if not task_lines:
            return []
        
        first_line = task_lines[0]
        task_name = self.clean_task_name(first_line)
        
        # Extraire les détails
        details = self.parse_task_details(task_lines)
        description = self.build_description(details)
        
        # Si c'est une tâche principale (niveau 2, ex: 2.5)
        if self.is_main_task(first_line):
            # Créer une entrée pour la tâche principale (TASKLIST rempli, TASK vide)
            main_task_entry = {
                'TASKLIST': task_name,  # La tâche principale va dans TASKLIST
                'TASK': '',  # TASK reste vide pour les tâches principales
                'DESCRIPTION': description,
                'ASSIGN TO': '',
                'START DATE': '',
                'DUE DATE': '',
                'PRIORITY': details['priority'] or '',
                'ESTIMATED TIME': '',
                'TAGS': '',
                'STATUS': ''
            }
            return [main_task_entry]
        
        # Si c'est une sous-tâche (niveau 3+, ex: 2.5.1)
        else:
            # Créer l'entrée de sous-tâche
            subtask_entry = {
                'TASKLIST': '',  # TASKLIST vide pour les sous-tâches
                'TASK': task_name,  # Le nom de la sous-tâche va dans TASK
                'DESCRIPTION': description,
                'ASSIGN TO': '',
                'START DATE': '',
                'DUE DATE': '',
                'PRIORITY': details['priority'] or '',
                'ESTIMATED TIME': '',
                'TAGS': '',
                'STATUS': ''
            }
            
            # Si c'est la première tâche du projet et qu'il n'y a pas de tâche principale
            if is_first_task and not current_main_task:
                subtask_entry['TASKLIST'] = project_title
            
            return [subtask_entry]
    
    def convert_to_excel(self, text: str, output_path: str) -> bool:
        """Convertit le texte en fichier Excel."""
        try:
            # Parser le texte
            tasks = self.parse_text_to_tasks(text)
            
            if not tasks:
                return False
            
            # Créer le DataFrame
            df = pd.DataFrame(tasks, columns=self.columns)
            
            # Sauvegarder en Excel
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Teamwork Import')
                
                # Ajuster la largeur des colonnes
                worksheet = writer.sheets['Teamwork Import']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de la conversion : {e}")
            return False
    
    def preview_conversion(self, text: str) -> pd.DataFrame:
        """Prévisualise la conversion sans sauvegarder."""
        
        # Essayer d'abord avec l'IA si disponible
        if self.use_ai and self.ai_parser:
            try:
                project_title = self.extract_project_title(text)
                ai_tasks = self.ai_parser.parse_with_ai(text, project_title)
                
                if ai_tasks:
                    print("✨ Parsing avec IA réussi")
                    return pd.DataFrame(ai_tasks, columns=self.columns)
                else:
                    print("⚠️ IA n'a pas pu parser - Fallback vers parser classique")
                    
            except Exception as e:
                print(f"⚠️ Erreur IA - Fallback vers parser classique: {e}")
        
        # Fallback vers le parser classique
        print("🔧 Utilisation du parser classique")
        tasks = self.parse_text_to_tasks(text)
        return pd.DataFrame(tasks, columns=self.columns)

# Fonction utilitaire pour tester
def test_converter():
    """Teste le convertisseur avec l'exemple fourni."""
    sample_text = """
Campagne Réseaux Sociaux – Liste de Tâches

📌 Objectif général :
Planifier et lancer une campagne de visibilité sur Instagram et LinkedIn.

Jalon Principal : Lancement du premier post sponsorisé

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
"""
    
    converter = TextToTeamworkConverter()
    preview = converter.preview_conversion(sample_text)
    print("Prévisualisation de la conversion :")
    print(preview.to_string(index=False))
    
    return converter.convert_to_excel(sample_text, "example_output.xlsx")

if __name__ == "__main__":
    test_converter() 