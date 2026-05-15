import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Test Connexion")

# Votre URL directe
url = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"

st.title("🔌 Test de Connexion")

conn = st.connection("gsheets", type=GSheetsConnection)

tabs = ['Parametrage_Biens', 'Suivi_Locations', 'Charges_Structure', 'Listes', 'Synthese_Fiscale']

for t in tabs:
    try:
        data = conn.read(spreadsheet=url, worksheet=t, ttl=0)
        st.success(f"✅ Onglet '{t}' trouvé !")
    except Exception as e:
        st.error(f"❌ Impossible de lire l'onglet '{t}'. Vérifiez l'orthographe dans Google Sheets.")
