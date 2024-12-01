import streamlit as st
from participant_filter_module import main as participant_filter
from test_input_feature import main as test_input
from visualization_prognoses import main as visualization_prognoses
from reports_module import main as reports
from warning_system_module import main as warnings
from design_layout_module import main as design_layout

# Hauptfunktion für die Streamlit-Anwendung
def main():
    st.set_page_config(layout="wide")
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
  
