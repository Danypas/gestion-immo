import streamlit as st
import pandas as pd

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")

# IDENTIFIANTS DES ONGLETS (GID)
SHEET_ID = "10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"
GID_SYNTHESE = "933600165"
GID_LOCATIONS = "452672058"

# BARRE LATÉRALE (MENU)
st.sidebar.header("🧭 Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Synthèse Fiscale", "🏠 Suivi des Locations"])

# FONCTION POUR LIRE LES DONNÉES
def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# --- PAGE SYNTHÈSE ---
if page == "📊 Synthèse Fiscale":
    st.title("📊 Synthèse Fiscale Globale")
    
    try:
        df = load_data(GID_SYNTHESE)
        
        # Métriques
        col1, col2, col3, col4 = st.columns(4)
        def get_m(label):
            try:
                return f"{df[df.iloc[:, 0].str.strip() == label].iloc[0, 1]} €"
            except: return "0 €"

        col1.metric("CA Total", get_m('CA Total'))
        col2.metric("Marge Opé.", get_m('Marge Opérationnelle'))
        col3.metric("Charges", get_m('Total Charges Structure'))
        col4.metric("Résultat Final", get_m('Résultat Final'))

        st.divider()
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur chargement Synthèse : {e}")

# --- PAGE LOCATIONS ---
elif page == "🏠 Suivi des Locations":
    st.title("🏠 Détail des Locations")
    
    try:
        df_loc = load_data(GID_LOCATIONS)
        
        # Petit résumé rapide pour cette page
        total_encaisse = df_loc.iloc[:, 5].sum() if len(df_loc.columns) > 5 else 0
        st.info(f"Montant total des loyers affichés dans ce tableau : **{total_encaisse} €**")
        
        st.divider()
        # Affichage du tableau complet
        st.dataframe(df_loc, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur chargement Locations : {e}")

st.sidebar.divider()
st.sidebar.caption("Données synchronisées avec Google Sheets")
