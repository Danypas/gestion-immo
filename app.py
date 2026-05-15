import streamlit as st
import pandas as pd

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")
st.title("📊 Mon Tableau de Bord Immobilier")

# L'ID de votre document
SHEET_ID = "10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8"

# URL qui force l'onglet "Synthese_Fiscale" via son GID
# GID 933600165 trouvé sur vos captures précédentes
URL_SYNTHESE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=933600165"

try:
    with st.spinner('Chargement de la synthèse fiscale...'):
        # On utilise storage_options pour éviter les problèmes de droits
        df = pd.read_csv(URL_SYNTHESE)
    
    st.success("✅ Synthèse fiscale chargée !")

    # Affichage des métriques
    col1, col2, col3, col4 = st.columns(4)
    
    def get_metric(label):
        try:
            # On cherche dans la colonne 'Indicateur' (colonne 0)
            # Et on prend la 'Valeur' (colonne 1)
            val = df[df.iloc[:, 0].str.strip() == label].iloc[0, 1]
            return f"{val} €"
        except:
            return "Non trouvé"

    col1.metric("CA Total", get_metric('CA Total'))
    col2.metric("Marge Opé.", get_metric('Marge Opérationnelle'))
    col3.metric("Charges", get_metric('Total Charges Structure'))
    col4.metric("Résultat Final", get_metric('Résultat Final'))

    st.divider()
    st.subheader("Vérification des données lues :")
    st.dataframe(df)

except Exception as e:
    st.error(f"Erreur de lecture : {e}")
