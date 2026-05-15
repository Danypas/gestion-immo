import streamlit as st
import pandas as pd
from datetime import date
import os
from openpyxl import load_workbook

# Configuration du fichier
EXCEL_FILE = 'Gestion_Locative_V2_Fidèle.xlsx'

st.set_page_config(page_title="Gestion Immo", layout="wide")

# Fonction pour charger les données
def load_all_data():
    biens = pd.read_excel(EXCEL_FILE, sheet_name='Parametrage_Biens')
    locs = pd.read_excel(EXCEL_FILE, sheet_name='Suivi_Locations')
    charges = pd.read_excel(EXCEL_FILE, sheet_name='Charges_Structure')
    listes = pd.read_excel(EXCEL_FILE, sheet_name='Listes')
    return biens, locs, charges, listes

# Fonction pour sauvegarder dans Excel
def save_data(df_to_add, sheet_name):
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        # On charge la feuille existante
        existing_df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        # On ajoute la nouvelle ligne
        updated_df = pd.concat([existing_df, df_to_add], ignore_index=True)
        # On réécrit la feuille
        updated_df.to_excel(writer, sheet_name=sheet_name, index=False)

# Chargement initial
try:
    biens, locs, charges, listes = load_all_data()
except Exception as e:
    st.error(f"Erreur de lecture du fichier Excel : {e}")
    st.stop()

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
    if not locs.empty:
        st.bar_chart(locs.groupby('Bien')['CA Perçu (€)'].sum())
    else:
        st.info("Aucune donnée de location à afficher.")

elif page == "Nouvelle Location":
    st.title("📝 Enregistrer une location")
    with st.form("loc_form", clear_on_submit=True):
        b = st.selectbox("Bien concerné", biens['Nom du Bien'].tolist())
        l = st.text_input("Nom du locataire")
        d1 = st.date_input("Début", date.today())
        d2 = st.date_input("Fin", date.today())
        val = st.number_input("Montant perçu (€)", min_value=0.0, format="%.2f")
        gest = st.number_input("Frais de gestion associés (€)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Valider l'enregistrement"):
            new_row = pd.DataFrame({
                'Bien': [b], 'Locataire': [l], 'Date Début': [d1], 
                'Date Fin': [d2], 'CA Perçu (€)': [val], 'Frais de Gestion (€)': [gest]
            })
            save_data(new_row, 'Suivi_Locations')
            st.success(f"Location pour {b} enregistrée avec succès !")
            st.balloons()

elif page == "Nouvelle Charge":
    st.title("💸 Enregistrer une charge fixe")
    with st.form("charge_form", clear_on_submit=True):
        b_c = st.selectbox("Bien concerné", biens['Nom du Bien'].tolist())
        cat = st.selectbox("Catégorie", listes.iloc[:, 0].tolist())
        mont = st.number_input("Montant (€)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Enregistrer la charge"):
            new_charge = pd.DataFrame({
                'Bien': [b_c], 'Catégorie': [cat], 'Montant (€)': [mont], 'Date': [date.today()]
            })
            save_data(new_charge, 'Charges_Structure')
            st.success("Charge enregistrée !")
