import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.participant_filter_module import main as participant_filter
from app.test_input_feature import main as test_input
from app.visualization_prognoses import main as visualization_prognoses
from app.reports_module import main as reports
from app.warning_system_module import main as warnings
from app.design_layout_module import main as design_layout

import streamlit as st

def main():
    st.set_page_config(layout="wide", page_title="Mathematik-Kursverwaltung")
    st.title("Mathematik-Kursverwaltung")

    # Tabs für verschiedene Bereiche
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Übersicht", "Teilnehmer", "Tests", "Prognosen", "Berichte"])

    # Übersicht
    with tab1:
        design_layout()

    # Teilnehmerverwaltung
    with tab2:
        participant_filter()

    # Tests
    with tab3:
        test_input()

    # Prognosen
    with tab4:
        visualization_prognoses()

    # Berichte
    with tab5:
        reports()

    # Warnsystem
    with st.sidebar:
        st.header("Warnungen")
        warnings()

if __name__ == "__main__":
    main()
