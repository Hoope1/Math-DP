import streamlit as st
import sys
import os

# Fügen Sie den modules-Ordner zum Python-Pfad hinzu, falls nicht erkannt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_PATH = os.path.join(BASE_DIR, '../modules')
if MODULES_PATH not in sys.path:
    sys.path.append(MODULES_PATH)

from database_setup import initialize_database
from app.participant_filter_module import main as teilnehmerverwaltung
from app.test_input_feature import main as testeingabe
from app.visualization_prognoses import main as prognose_visualisierung
from app.reports_module import main as berichte
from app.warning_system_module import main as warnsystem
from app.design_layout_module import main as dashboard

# Initialisierung der Datenbank
initialize_database()

# Hauptfunktion der Streamlit-Anwendung
def main():
    st.set_page_config(
        layout="wide", 
        page_title="Mathematik-Kursverwaltung"
    )
    st.title("Mathematik-Kursverwaltung")

    # Tabs für die verschiedenen Bereiche
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dashboard", "Teilnehmerverwaltung", "Testergebniseingabe", 
        "Prognosen", "Berichte", "Warnsystem"
    ])

    # Dashboard
    with tab1:
        dashboard()

    # Teilnehmerverwaltung
    with tab2:
        teilnehmerverwaltung()

    # Testergebniseingabe
    with tab3:
        testeingabe()

    # Prognosen
    with tab4:
        prognose_visualisierung()

    # Berichte
    with tab5:
        berichte()

    # Warnsystem
    with tab6:
        warnsystem()

if __name__ == "__main__":
    main()
