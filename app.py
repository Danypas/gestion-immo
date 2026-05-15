import streamlit as st
import pandas as pd

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")
st.title("📊 Mon Tableau de Bord Immobilier")

# L'URL DE PARTAGE (Format CSV direct pour éviter l'erreur 400)
# On transforme l'URL pour demander directement le format CSV de l'onglet voulu
SHEET_ID = "10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"
TAB_NAME = "Synthese_Fiscale"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_NAME}"

try:
    # Lecture directe avec Pandas (plus fiable que le connecteur gsheets dans ce cas précis)
    with st.spinner('Chargement des données...'):
        df = pd.read_csv(URL_CSV)
    
    st.success("✅ Données récupérées !")

    # Affichage des métriques
    col1, col2, col3, col4 = st.columns(4)
    
    # On récupère les valeurs dynamiquement
    def get_metric(label):
        try:
            return df[df.iloc[:, 0] == label].iloc[0, 1]
        except:
            return "N/A"

    col1.metric("CA Total", f"{get_metric('CA Total')} €")
    col2.metric("Marge Opé.", f"{get_metric('Marge Opérationnelle')} €")
    col3.metric("Charges", f"{get_metric('Total Charges Structure')} €")
    col4.metric("Résultat Final", f"{get_metric('Résultat Final')} €")

    st.divider()
    st.subheader("Détail des calculs")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.info("Vérifiez que l'onglet s'appelle exactement 'Synthese_Fiscale' (sans accent) dans Google Sheets.")
