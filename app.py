import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Gestion Immo Nomade", layout="wide")

# Connexion au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet="https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8")

def load_data(sheet_name):
    # On force le rafraîchissement à chaque chargement pour voir les nouvelles lignes
    return conn.read(worksheet=sheet_name, ttl=0)

# Chargement des données
try:
    biens = load_data('Parametrage_Biens')
    locs = load_data('Suivi_Locations')
    charges = load_data('Charges_Structure')
    listes = load_data('Listes')
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

st.sidebar.title("🏠 Menu Nomade")
page = st.sidebar.radio("Aller vers", ["Tableau de Bord", "Nouvelle Location", "Nouvelle Charge"])

if page == "Tableau de Bord":
    st.title("📊 Synthèse Immobilière")
    # Utilisation des noms exacts de votre capture d'écran
    ca = pd.to_numeric(locs['CA Perçu (€)'], errors='coerce').sum()
    frais = pd.to_numeric(locs['Frais de Gestion (€)'], errors='coerce').sum()
    struct = pd.to_numeric(charges['Montant (€)'], errors='coerce').sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Chiffre d'Affaire", f"{ca:.2f} €")
    c2.metric("Frais Opérationnels", f"{frais:.2f} €")
    c3.metric("Bénéfice Net", f"{(ca - frais - struct):.2f} €")
    
    st.subheader("Revenus par bien")
    if not locs.empty:
        st.bar_chart(locs.groupby('Bien')['CA Perçu (€)'].sum())

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
            # Création de la ligne avec les noms EXACTS de votre capture
            new_row = pd.DataFrame([{
                "Bien": b, 
                "Locataire": l, 
                "Date Début": str(d1),
                "Date Fin": str(d2), 
                "CA Perçu (€)": val, 
                "Frais de Gestion (€)": gest
            }])
            updated_df = pd.concat([locs, new_row], ignore_index=True)
            conn.update(worksheet="Suivi_Locations", data=updated_df)
            st.cache_data.clear()
            st.success("C'est enregistré dans Google Sheets !")
            st.balloons()

elif page == "Nouvelle Charge":
    st.title("💸 Enregistrer une charge")
    with st.form("charge_form", clear_on_submit=True):
        b_c = st.selectbox("Bien concerné", biens['Nom du Bien'].unique())
        cat = st.selectbox("Catégorie", listes.iloc[:, 0].unique())
        mont = st.number_input("Montant (€)", min_value=0.0)
        
        if st.form_submit_button("Enregistrer la charge"):
            new_charge = pd.DataFrame([{
                "Bien": b_c, 
                "Catégorie": cat, 
                "Montant (€)": mont, 
                "Date": str(date.today())
            }])
            updated_charges = pd.concat([charges, new_charge], ignore_index=True)
            conn.update(worksheet="Charges_Structure", data=updated_charges)
            st.cache_data.clear()
            st.success("Charge enregistrée !")
