import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Test Final")

url = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # On teste la lecture la plus simple possible
    data = conn.read(spreadsheet=url, worksheet="Synthese_Fiscale")
    st.success("Connexion réussie !")
    st.table(data)
except Exception as e:
    st.error(f"Erreur : {e}")
