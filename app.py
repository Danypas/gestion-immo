import streamlit as st
import pandas as pd

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")
st.title("📊 Mon Tableau de Bord Immobilier")

# L'identifiant de votre fichier Google Sheets
SHEET_ID = "10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"

# On définit l'URL spécifique pour l'onglet "Synthese_Fiscale"
URL_SYNTHESE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Synthese_Fiscale"

try:
    # Lecture forcée de l'onglet Synthese_Fiscale
    with st.spinner('Chargement de la synthèse...'):
        df = pd.read_csv(URL_SYNTHESE)
    
    st.success("✅ Synthèse fiscale chargée !")

    # Affichage des métriques en haut de page
    col1, col2, col3, col4 = st.columns(4)
    
    def get_metric(label):
        try:
            # On cherche la ligne où la première colonne correspond exactement au texte
            # On récupère la valeur juste à côté (colonne 1)
            val = df[df.iloc[:, 0] == label].iloc[0, 1]
            return f"{val} €"
        except:
            return "0 €"

    # Ces noms doivent être IDENTIQUES à ceux écrits dans votre colonne "Indicateur"
    col1.metric("CA Total", get_metric('CA Total'))
    col2.metric("Marge Opé.", get_metric('Marge Opérationnelle'))
    col3.metric("Charges", get_metric('Total Charges Structure'))
    col4.metric("Résultat Final", get_metric('Résultat Final'))

    st.divider()
    
    # Affichage du tableau complet pour vérifier les données
    st.subheader("Détail de la Synthèse (Onglet Google Sheet)")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.info("Vérifiez bien que l'onglet s'appelle 'Synthese_Fiscale' dans votre Google Sheet.")
