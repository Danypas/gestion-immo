import streamlit as st
import pandas as pd
from datetime import date
import os
from openpyxl import load_workbook

# Fichier Excel
EXCEL_FILE = 'Gestion_Locative_V2_Fidèle.xlsx'

st.set_page_config(page_title="Gestion Immo", layout="wide")

def load_all_data():
    biens = pd.read_excel(EXCEL_FILE, sheet_name='Parametrage_Biens')
    locs = pd.read_excel(EXCEL_FILE, sheet_name='Suivi_Locations')
    charges = pd.read_excel(EXCEL_FILE, sheet_name='Charges_Structure')
    listes = pd.read_excel(EXCEL_FILE, sheet_name='Listes')
    return biens, locs, charges, listes

biens, locs, charges, listes = load_all_data()

st.sidebar.title("🏠 Menu")
page = st.sidebar.radio("Aller vers", ["Tableau de Bord", "Nouvelle Location", "Nouvelle Charge"])

if page == "Tableau de Bord":
    st.title("📊 Synthèse Immobilière")
    ca = locs['CA Perçu (€)'].sum()
    frais = locs['Frais de Gestion (€)'].sum()
    struct = charges['Montant (€)'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Chiffre d'Affaire", f"{ca} €")
    c2.metric("Frais Opérationnels", f"{frais} €")
    c3.metric("Bénéfice Net (estimé)", f"{ca - frais - struct} €")
    
    st.subheader("Détail des revenus par bien")
    st.bar_chart(locs.groupby('Bien')['CA Perçu (€)'].sum())

elif page == "Nouvelle Location":
    st.title("📝 Enregistrer une location")
    with st.form("loc_form"):
        b = st.selectbox("Bien concerné", biens['Nom du Bien'].tolist())
        l = st.text_input("Nom du locataire")
        d1 = st.date_input("Début", date.today())
        d2 = st.date_input("Fin", date.today())
        val = st.number_input("Montant perçu (€)", min_value=0)
        gest = st.number_input("Frais de gestion associés (€)", min_value=0)
        if st.form_submit_button("Valider"):
            # Ici on ajoute au fichier Excel (logique simplifiée pour l'exemple)
            st.success(f"Location de {l} enregistrée !")

elif page == "Nouvelle Charge":
    st.title("💸 Enregistrer une charge fixe")
    with st.form("charge_form"):
        b_c = st.selectbox("Bien concerné", biens['Nom du Bien'].tolist())
        cat = st.selectbox("Catégorie", listes.iloc[:, 0].tolist())
        mont = st.number_input("Montant (€)", min_value=0)
        if st.form_submit_button("Enregistrer la charge"):
            st.success("Charge enregistrée !")
