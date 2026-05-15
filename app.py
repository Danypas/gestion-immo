import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Test de Connexion Ultime")

# URL SANS le /edit à la fin
url = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # On essaie de lire SANS préciser l'onglet d'abord (ça lira le premier par défaut)
    data = conn.read(spreadsheet=url)
    st.success("Bravo ! Le fichier est enfin lu.")
    st.write(data)
except Exception as e:
    st.error(f"Erreur persistante : {e}")
    st.info("Vérification : Allez dans 'Partager' sur Google Sheets -> 'Modifier l'accès' -> Vérifiez que c'est bien 'Tous les utilisateurs disposant du lien'.")
