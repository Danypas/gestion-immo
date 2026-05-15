import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Gestion Immo Nomade", layout="wide")

# URL de votre Google Sheet (vérifiée)
URL_SHEET = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name):
    # On force la lecture via l'URL directe pour éviter les erreurs de configuration
    return conn.read(spreadsheet=URL_SHEET, worksheet=sheet_name, ttl=0)

# Chargement initial des données (Vérifiez bien l'orthographe ici)
try:
    biens = load_data('Parametrage_Biens')
    locs = load_data('Suivi_Locations')
    charges = load_data('Charges_Structure')
    listes = load_data('Listes')
    fiscale = load_data('Synthese_Fiscale') # L'onglet qui posait problème
except Exception as e:
    st.error(f"Erreur : Impossible de trouver un onglet. Vérifiez l'orthographe. Détail : {e}")
    st.stop()

st.sidebar.title("🏠 Menu Nomade")
page = st.sidebar.radio("Aller vers", ["Tableau de Bord", "Nouvelle Location", "Nouvelle Charge"])

# --- PAGE 1 : TABLEAU DE BORD ---
if page == "Tableau de Bord":
    st.title("📊 Synthèse Immobilière")
    
    # Calculs (en s'assurant que les colonnes sont bien lues comme des nombres)
    ca = pd.to_numeric(locs['CA Perçu (€)'], errors='coerce').sum()
    frais = pd.to_numeric(locs['Frais de Gestion (€)'], errors='coerce').sum()
    struct = pd.to_numeric(charges['Montant (€)'], errors='coerce').sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Chiffre d'Affaire", f"{ca:.2f} €")
    col2.metric("Frais Opérationnels", f"{frais:.2f} €")
    col3.metric("Bénéfice Net", f"{(ca - frais - struct):.2f} €")
    
    st.subheader("Répartition des revenus par bien")
    if not locs.empty:
        st.bar_chart(locs.groupby('Bien')['CA Perçu (€)'].sum())

# --- PAGE 2 : NOUVELLE LOCATION ---
elif page == "Nouvelle Location":
    st.title("📝 Enregistrer une location")
    with st.form("loc_form", clear_on_submit=True):
        b = st.selectbox("Bien concerné", biens['Nom du Bien'].unique())
        l = st.text_input("Nom du locataire")
        d1 = st.date_input("Début", date.today())
        d2 = st.date_input("Fin", date.today())
        val = st.number_input("Montant perçu (€)", min_value=0.0)
        gest = st.number_input("Frais de gestion associés (€)", min_value=0.0)
        
        if st.form_submit_button("Valider l'enregistrement"):
            new_row = pd.DataFrame([{
                "Bien": b, "Locataire": l, "Date Début": str(d1),
                "Date Fin": str(d2), "CA Perçu (€)": val, "Frais de Gestion (€)": gest
            }])
            updated_df = pd.concat([locs, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, worksheet="Suivi_Locations", data=updated_df)
            st.cache_data.clear()
            st.success("Enregistré dans Google Sheets !")
            st.balloons()

# --- PAGE 3 : NOUVELLE CHARGE ---
elif page == "Nouvelle Charge":
    st.title("💸 Enregistrer une charge")
    with st.form("charge_form", clear_on_submit=True):
        b_c = st.selectbox("Bien concerné", biens['Nom du Bien'].unique())
        cat = st.selectbox("Catégorie", listes.iloc[:, 0].unique())
        mont = st.number_input("Montant (€)", min_value=0.0)
        
        if st.form_submit_button("Enregistrer la charge"):
            new_charge = pd.DataFrame([{
                "Bien": b_c, "Catégorie": cat, "Montant (€)": mont, "Date": str(date.today())
            }])
            updated_charges = pd.concat([charges, new_charge], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, worksheet="Charges_Structure", data=updated_charges)
            st.cache_data.clear()
            st.success("Charge enregistrée avec succès !")
