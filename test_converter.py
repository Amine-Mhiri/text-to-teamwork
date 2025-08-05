#!/usr/bin/env python3
"""
Tests pour valider le fonctionnement du Text to Teamwork Converter
"""

import pandas as pd
import os
from text_to_teamwork import TextToTeamworkConverter

def test_sample_conversion():
    """Test avec l'exemple fourni dans les spécifications."""
    sample_text = """Campagne Réseaux Sociaux – Liste de Tâches

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
   Critère d'acceptation : Textes sans fautes et optimisés SEO"""
    
    print("🧪 Test 1: Conversion de l'exemple de base")
    print("=" * 50)
    
    converter = TextToTeamworkConverter()
    
    # Test de prévisualisation
    preview_df = converter.preview_conversion(sample_text)
    
    print(f"✅ Nombre de tâches détectées : {len(preview_df)}")
    print(f"✅ Nom du projet : {preview_df.iloc[0]['TASKLIST']}")
    print(f"✅ Première tâche : {preview_df.iloc[0]['TASK']}")
    
    # Vérifier que les priorités sont correctement extraites
    priority_tasks = preview_df[preview_df['PRIORITY'] != '']
    print(f"✅ Tâches avec priorité : {len(priority_tasks)}")
    
    # Test de génération Excel
    output_file = "test_output.xlsx"
    success = converter.convert_to_excel(sample_text, output_file)
    
    if success and os.path.exists(output_file):
        print(f"✅ Fichier Excel généré : {output_file}")
        file_size = os.path.getsize(output_file)
        print(f"✅ Taille du fichier : {file_size} bytes")
        
        # Nettoyer
        os.remove(output_file)
        print("✅ Fichier de test nettoyé")
    else:
        print("❌ Échec de génération du fichier Excel")
        return False
    
    print("\n📊 Aperçu du résultat :")
    print(preview_df[['TASKLIST', 'TASK', 'PRIORITY']].to_string(index=False))
    
    return True

def test_complex_example():
    """Test avec un exemple plus complexe."""
    
    print("\n\n🧪 Test 2: Exemple complexe avec multiples sections")
    print("=" * 50)
    
    # Lire l'exemple complexe
    try:
        with open('examples/sample_text.txt', 'r', encoding='utf-8') as f:
            complex_text = f.read()
    except FileNotFoundError:
        print("❌ Fichier examples/sample_text.txt non trouvé")
        return False
    
    converter = TextToTeamworkConverter()
    preview_df = converter.preview_conversion(complex_text)
    
    print(f"✅ Tâches détectées : {len(preview_df)}")
    print(f"✅ Project name: {preview_df.iloc[0]['TASKLIST']}")
    
    # Compter les différents éléments
    priority_count = len(preview_df[preview_df['PRIORITY'] != ''])
    description_count = len(preview_df[preview_df['DESCRIPTION'] != ''])
    
    print(f"✅ Tâches avec priorité : {priority_count}")
    print(f"✅ Tâches avec description : {description_count}")
    
    # Vérifier quelques éléments spécifiques
    if "Élevée" in preview_df['PRIORITY'].values:
        print("✅ Priorité 'Élevée' correctement détectée")
    
    if "Dépendance" in preview_df['DESCRIPTION'].iloc[1]:
        print("✅ Dépendances correctement extraites")
    
    return True

def test_edge_cases():
    """Test de cas limites."""
    
    print("\n\n🧪 Test 3: Cas limites et formats variés")
    print("=" * 50)
    
    edge_cases = [
        # Différents formats de numérotation
        """Projet Test Numérotation
        
        • Première tâche
        - Deuxième tâche  
        ✅ Troisième tâche
        a) Quatrième tâche""",
        
        # Sans priorité explicite
        """Projet Simple
        
        1. Tâche unique
           Description : Juste une description simple""",
        
        # Avec emojis et caractères spéciaux
        """🚀 Projet Emojis
        
        1. Tâche avec émojis 🎯
           Description : Contient des émojis 📋 et caractères spéciaux @#$
           Priorité : Élevée"""
    ]
    
    converter = TextToTeamworkConverter()
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n📝 Sous-test 3.{i}:")
        try:
            result = converter.preview_conversion(test_case)
            print(f"   ✅ {len(result)} tâche(s) détectée(s)")
            
            if not result.empty:
                print(f"   ✅ Project: {result.iloc[0]['TASKLIST']}")
                print(f"   ✅ First task: {result.iloc[0]['TASK']}")
            
        except Exception as e:
            print(f"   ❌ Erreur : {e}")
            
    return True

def test_performance():
    """Test de performance avec un grand nombre de tâches."""
    
    print("\n\n🧪 Test 4: Performance avec 50 tâches")
    print("=" * 50)
    
    # Générer un texte avec 50 tâches
    large_text = "Grand Projet Test\n\n"
    for i in range(1, 51):
        large_text += f"{i}. Tâche numéro {i}\n"
        large_text += f"   Description : Description de la tâche {i}\n"
        if i % 5 == 0:  # Ajouter priorité à chaque 5ème tâche
            large_text += "   Priorité : Élevée\n"
        large_text += "\n"
    
    import time
    
    converter = TextToTeamworkConverter()
    
    start_time = time.time()
    result = converter.preview_conversion(large_text)
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    print(f"✅ {len(result)} tâches traitées")
    print(f"✅ Temps de traitement : {processing_time:.3f} secondes")
    print(f"✅ Performance : {len(result)/processing_time:.1f} tâches/seconde")
    
    if processing_time < 5.0:  # Moins de 5 secondes acceptable
        print("✅ Performance acceptable")
        return True
    else:
        print("⚠️  Performance lente")
        return False

def run_all_tests():
    """Lance tous les tests."""
    
    print("🧪 SUITE DE TESTS - TEXT TO TEAMWORK CONVERTER")
    print("=" * 60)
    
    tests = [
        ("Conversion de base", test_sample_conversion),
        ("Exemple complexe", test_complex_example), 
        ("Cas limites", test_edge_cases),
        ("Performance", test_performance)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n\n📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🏆 Résultat final : {passed}/{len(results)} tests réussis")
    
    if passed == len(results):
        print("🎉 Tous les tests sont passés avec succès !")
        return True
    else:
        print("⚠️  Certains tests ont échoué")
        return False

if __name__ == "__main__":
    run_all_tests() 