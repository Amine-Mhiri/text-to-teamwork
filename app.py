import streamlit as st
import pandas as pd
import io
from text_to_teamwork import TextToTeamworkConverter

# Configuration de la page
st.set_page_config(
    page_title="Text to Teamwork Converter",
    page_icon="📋",
    layout="wide"
)

# CSS personnalisé pour une interface moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>📋 Text to Teamwork Converter</h1>
    <p>Transformez vos textes de tâches structurées en fichiers Excel compatibles avec Teamwork Projects</p>
</div>
""", unsafe_allow_html=True)

# Initialiser le convertisseur avec configuration IA
@st.cache_resource
def get_converter(api_key=None, use_ai=True):
    return TextToTeamworkConverter(openai_api_key=api_key, use_ai=use_ai)

# Sidebar avec configuration et instructions
with st.sidebar:
    st.header("🤖 Configuration IA")
    
    # Configuration OpenAI
    api_key = st.text_input(
        "Clé OpenAI API (optionnel)",
        type="password",
        help="Pour un parsing ultra-précis avec GPT-4. Laissez vide pour le parser classique.",
        placeholder="sk-..."
    )
    
    use_ai = st.checkbox(
        "Utiliser l'IA (GPT-4)",
        value=True,
        help="Parser intelligent vs parser classique"
    )
    
    if api_key:
        st.success("🧠 Mode IA activé")
        st.info("Précision maximale avec GPT-4")
    else:
        st.warning("🔧 Mode classique")
        st.info("Parser basé sur des règles")
    
    st.markdown("---")
    st.header("📝 Instructions")
    st.markdown("""
    **Format attendu :**
    - Titre du projet en début
    - Tâches numérotées (1., 2., etc.)
    - Sous-éléments avec descriptions
    - Priorités, dépendances, critères
    
    **Exemple :**
    ```
    Mon Projet
    
    1. Première tâche
       Description : Détails de la tâche
       Priorité : High
    
    2. Deuxième tâche
       Dépendance : 1
       Critère : Validation requise
    ```
    """)
    
    st.header("🎯 Colonnes Excel")
    st.markdown("""
    - **TASKLIST** : Nom du projet
    - **TASK** : Nom de la tâche (sans numérotation)
    - **DESCRIPTION** : Détails, critères, dépendances
    - **PRIORITY** : Priorité si mentionnée
    - **Autres** : Laissées vides pour saisie manuelle
    """)

# Initialiser le convertisseur avec la configuration (gestion d'erreur pour le cloud)
try:
    converter = get_converter(api_key=api_key if api_key else None, use_ai=use_ai)
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    # Fallback vers mode classique
    converter = get_converter(api_key=None, use_ai=False)
    st.warning("🔧 Mode classique activé suite à une erreur")

# Interface principale
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Texte d'entrée")
    
    # Zone de texte pour l'input
    input_text = st.text_area(
        "Collez votre texte structuré ici :",
        value=st.session_state.get('example_text', ''),
        height=400,
        placeholder="""Exemple :

Campagne Réseaux Sociaux

1. Définir le concept
   Description : Créer le thème visuel
   Priorité : High
   Critère : Validation équipe

2. Créer calendrier éditorial
   Description : Planning 4 semaines
   Dépendance : 1""",
        help="Collez votre texte avec tâches hiérarchisées"
    )
    
    # Exemple prédéfini
    if st.button("📄 Charger l'exemple", type="secondary"):
        st.session_state.example_text = """Campagne Réseaux Sociaux – Liste de Tâches

📌 Objectif général :
Planifier et lancer une campagne de visibilité sur Instagram et LinkedIn.

Jalon Principal : Lancement du premier post sponsorisé

✅ Liste des Tâches :
1. Définir le concept de la campagne  
   Description : Trouver un message central et un thème visuel  
   Priorité : High
   Critère d'acceptation : Concept validé par l'équipe

2. Créer le calendrier éditorial  
   Description : Planifier les publications sur 4 semaines  
   Dépendance : 1  
   Priorité : Medium
   Critère d'acceptation : Calendrier complet avec visuels et dates

3. Rédiger les textes des publications  
   Description : Écrire les textes adaptés à chaque plateforme  
   Dépendance : 2  
   Priorité : High
   Critère d'acceptation : Textes sans fautes et optimisés SEO"""
        st.rerun()

with col2:
    st.header("📊 Prévisualisation")
    
    if input_text:
        try:
            # Prévisualisation avec indication du mode
            if api_key and use_ai:
                st.info("🧠 **Parsing avec IA** - Précision maximale activée")
            else:
                st.info("🔧 **Parsing classique** - Ajoutez une clé OpenAI pour une précision optimale")
            
            preview_df = converter.preview_conversion(input_text)
            
            if not preview_df.empty:
                st.markdown('<div class="success-box">✅ Conversion réussie ! Prévisualisation ci-dessous :</div>', unsafe_allow_html=True)
                
                # Afficher le tableau avec un style amélioré
                st.dataframe(
                    preview_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Statistiques rapides
                st.markdown("**📊 Statistiques :**")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("Tâches", len(preview_df))
                
                with col_stat2:
                    priority_count = len(preview_df[preview_df['PRIORITY'] != ''])
                    st.metric("Avec priorité", priority_count)
                
                with col_stat3:
                    project_name = preview_df.iloc[0]['TASKLIST'] if not preview_df.empty else "N/A"
                    st.metric("Projet", project_name[:15] + "..." if len(project_name) > 15 else project_name)
                
            else:
                st.markdown('<div class="warning-box">⚠️ Aucune tâche détectée. Vérifiez le format de votre texte.</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Erreur lors de la prévisualisation : {str(e)}")
    else:
        st.info("👆 Entrez votre texte à gauche pour voir la prévisualisation")

# Section de téléchargement
if input_text:
    st.header("💾 Téléchargement")
    
    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
    
    with col_dl2:
        if st.button("📥 Générer et télécharger Excel", type="primary", use_container_width=True):
            try:
                # Créer le fichier Excel en mémoire
                output = io.BytesIO()
                
                # Convertir en DataFrame
                tasks_df = converter.preview_conversion(input_text)
                
                if not tasks_df.empty:
                    # Sauvegarder en Excel dans le buffer
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        tasks_df.to_excel(writer, index=False, sheet_name='Teamwork Import')
                        
                        # Ajuster les colonnes
                        worksheet = writer.sheets['Teamwork Import']
                        for idx, col in enumerate(tasks_df.columns):
                            max_length = max(
                                tasks_df[col].astype(str).map(len).max(),
                                len(col)
                            )
                            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
                    
                    # Préparer le téléchargement
                    output.seek(0)
                    
                    # Nom du projet pour le fichier
                    project_name = tasks_df.iloc[0]['TASKLIST'] if not tasks_df.empty else "Projet"
                    filename = f"{project_name.replace(' ', '_')}_Teamwork.xlsx"
                    
                    st.download_button(
                        label="📥 Télécharger le fichier Excel",
                        data=output.getvalue(),
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.success("✅ Fichier Excel généré avec succès !")
                    
                else:
                    st.error("❌ Impossible de générer le fichier : aucune tâche détectée")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {str(e)}")

# Section d'aide avancée
with st.expander("🔧 Aide avancée et nouveautés IA"):
    st.markdown("""
    ### 🧠 **NOUVEAU : Parser IA avec GPT-4**
    
    **🚀 Avantages du mode IA :**
    - **100% fiable** : Comprend n'importe quel format de texte
    - **Ultra-flexible** : Emails, documents Word, notes désorganisées
    - **Intelligence contextuelle** : Comprend l'intention, pas juste la forme
    - **Mapping parfait** : Tâches principales vs sous-tâches automatique
    - **Extraction intelligente** : Priorités, dépendances, risques
    
    **⚙️ Comment activer :**
    1. Obtenir une clé OpenAI sur [platform.openai.com](https://platform.openai.com)
    2. L'entrer dans la sidebar 
    3. Cocher "Utiliser l'IA"
    4. **Résultat : 100% fiable peu importe le format !**
    
    ---
    
    ### 📋 Format supporté (les deux modes)
    
    **Mode IA (Recommandé) :**
    - ✅ **Tout format** : emails, notes, documents désorganisés
    - ✅ **Numérotation flexible** : 1., 2.5.1, •, -, emojis, ou aucune
    - ✅ **Langue naturelle** : "urgent", "important", "doit être fait avant"
    - ✅ **Structure libre** : peu importe l'organisation
    
    **Mode classique (Fallback) :**
    - **Numérotation** : `1.`, `2.5.1`, `a)`, `•`, `-`, `✅`
    - **Priorités** : élevée, haute, moyenne, faible (français/anglais)
    - **Sections** : Description:, Dépendance:, Critère:, etc.
    
    ### 🎯 Conseils selon le mode
    
    **🧠 Avec IA activée :**
    - Collez n'importe quel texte de projet
    - L'IA comprend le contexte et l'intention
    - Formats libres acceptés
    
    **🔧 Mode classique :**
    - Structurez clairement avec numérotation
    - Utilisez les mots-clés : "Description :", "Priorité :"
    - Hiérarchie : 2.5 (principale) → 2.5.1 (sous-tâche)
    
    ### 🔄 Workflow optimisé
    
    1. **[NOUVEAU]** Ajoutez votre clé OpenAI pour 100% de fiabilité
    2. Collez votre texte (n'importe quel format)
    3. L'IA analyse et mappe automatiquement
    4. Vérifiez la prévisualisation
    5. Téléchargez et importez dans Teamwork
    
    ### 💡 Exemples de formats supportés en mode IA
    
    **Email de projet :**
    ```
    Objet: Nouveau site web
    
    Salut, voici les tâches pour le site :
    - Design des maquettes (urgent)
    - Développement front-end 
    - Tests utilisateurs
    ```
    
    **Notes de réunion :**
    ```
    Réunion projet mobile app
    
    TODO:
    * Interface utilisateur → Marie (priorité haute)
    * Backend API → Jean 
    * Tests → équipe QA (après backend)
    ```
    
    **✨ L'IA comprend tout et mappe parfaitement !**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 <strong>Text to Teamwork Converter</strong> - Simplifiez votre gestion de projet</p>
    <p>Compatible avec Teamwork Projects | Format Excel optimisé | Conversion automatique</p>
</div>
""", unsafe_allow_html=True) 