import streamlit as st
from streamlit_gsheets import GSheetsConnection

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gestion Immo", layout="wide")
st.title("📊 Mon Tableau de Bord Immobilier")

# L'URL STANDARD (Celle qui correspond à votre partage)
URL = "https://docs.google.com/spreadsheets/d/10BCCMOjBFSN93w4xwUmlIfc_ejR6m6Cib7JVsQOY1n8/edit?usp=sharing"

# CONNEXION
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Chargement des données
    with st.spinner('Chargement des données...'):
        df_synthese = conn.read(spreadsheet=URL, worksheet="Synthese_Fiscale")
        # On pourra ajouter les autres onglets ici une fois que celui-ci s'affiche
    
    st.success("✅ Connexion établie avec succès !")

    # 2. Affichage des indicateurs (Design "Tableau de bord")
    st.subheader("Synthèse Fiscale")
    
    # On transforme le tableau pour l'afficher joliment
    col1, col2, col3, col4 = st.columns(4)
    
    # Extraction des valeurs (basé sur votre image)
    # On suppose que l'indicateur est en colonne A et la valeur en colonne B
    def get_val(label):
        try:
            return df_synthese[df_synthese.iloc[:, 0] == label].iloc[0, 1]
        except:
            return 0

    col1.metric("CA Total", f"{get_val('CA Total')} €")
    col2.metric("Marge Opé.", f"{get_val('Marge Opérationnelle')} €")
    col3.metric("Charges", f"{get_val('Total Charges Structure')} €")
    col4.metric("Résultat Final", f"{get_val('Résultat Final')} €", delta_color="normal")

    st.divider()
    st.write("### Détail des données")
    st.table(df_synthese)

except Exception as e:
    st.error(f"Oups ! Petit souci technique : {e}")
    st.info("Vérifiez que le nom de l'onglet est bien 'Synthese_Fiscale' sans accent ni espace.")
