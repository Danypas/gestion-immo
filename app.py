import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")

# IDENTIFIANTS (GID)
SHEET_ID = "10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"
GID_SYNTHESE = "933600165"
GID_LOCATIONS = "452672058"
GID_CHARGES = "1888426177"

# BARRE LATÉRALE (MENU)
st.sidebar.header("🧭 Navigation")
page = st.sidebar.radio("Aller vers :", [
    "📊 Synthèse Fiscale", 
    "🏠 Suivi des Locations",
    "💸 Charges de Structure"
])

def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# --- PAGE SYNTHÈSE ---
if page == "📊 Synthèse Fiscale":
    st.title("📊 Synthèse Fiscale Globale")
    try:
        df = load_data(GID_SYNTHESE)
        col1, col2, col3, col4 = st.columns(4)
        def get_m(label):
            try: return f"{df[df.iloc[:, 0].str.strip() == label].iloc[0, 1]} €"
            except: return "0 €"
        col1.metric("CA Total", get_m('CA Total'))
        col2.metric("Marge Opé.", get_m('Marge Opérationnelle'))
        col3.metric("Charges", get_m('Total Charges Structure'))
        col4.metric("Résultat Final", get_m('Résultat Final'))
        st.divider()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- PAGE LOCATIONS ---
elif page == "🏠 Suivi des Locations":
    st.title("🏠 Détail des Locations")
    try:
        df_loc = load_data(GID_LOCATIONS)
        st.dataframe(df_loc, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- PAGE CHARGES ---
elif page == "💸 Charges de Structure":
    st.title("💸 Charges de Structure")
    try:
        df_charges = load_data(GID_CHARGES)
        
        # Calcul du total des charges
        # On suppose que la colonne 1 contient les montants
        total_ch = df_charges.iloc[:, 1].sum()
        st.metric("Total Charges Annuelles", f"{total_ch} €")
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("Liste des dépenses")
            st.dataframe(df_charges, use_container_width=True)
            
        with col_right:
            st.subheader("Répartition")
            # Création d'un graphique camembert si les données le permettent
            fig = px.pie(df_charges, names=df_charges.columns[0], values=df_charges.columns[1], hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur : {e}")

st.sidebar.divider()
st.sidebar.caption("Données synchronisées en temps réel")
