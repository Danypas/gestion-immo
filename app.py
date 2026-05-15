import streamlit as st
from streamlit_gsheets import GSheetsConnection

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")
st.title("📊 Tableau de Bord Immobilier")

# L'URL DIRECTE (SANS PASSER PAR LES SECRETS)
URL_DIRECTE = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8/edit#gid=0"

# CONNEXION
conn = st.connection("gsheets", type=GSheetsConnection)

# FONCTION DE LECTURE FORCÉE
def load_sheet(name):
    return conn.read(spreadsheet=URL_DIRECTE, worksheet=name, ttl=0)

# TENTATIVE DE CHARGEMENT
try:
    with st.spinner('Connexion au Google Sheet en cours...'):
        # On charge les onglets un par un
        df_biens = load_sheet('Parametrage_Biens')
        df_locs = load_sheet('Suivi_Locations')
        df_charges = load_sheet('Charges_Structure')
        df_listes = load_sheet('Listes')
        df_synthese = load_sheet('Synthese_Fiscale')
    
    st.success("✅ Données chargées avec succès !")
    
    # AFFICHAGE DE TEST POUR VOIR SI ÇA MARCHE
    st.subheader("Aperçu de la Synthèse Fiscale")
    st.write(df_synthese)

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Vérifiez que l'onglet 'Synthese_Fiscale' existe bien et que le partage est sur 'Tous les utilisateurs disposant du lien'.")
