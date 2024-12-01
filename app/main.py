import streamlit as st

from modules.database_setup import initialize_database

from app.participant_filter_module import teilnehmer_ansicht as manage_participants

from app.test_input_feature import testeingabe as test_input

from app.visualization_prognoses import prognose_visualisierung as visualize_prognoses

from app.reports_module import berichte as generate_reports

from app.warning_system_module import warnsystem as warning_system

from app.design_layout_module import main as layout_dashboard



# Initialize database

def setup_database():

    initialize_database()



# Streamlit navigation setup

def main():

    st.sidebar.title("Navigation")

    options = {

        "Dashboard": layout_dashboard,

        "Teilnehmer verwalten": manage_participants,

        "Testergebnisse eingeben": test_input,

        "Prognosen visualisieren": visualize_prognoses,

        "Berichte generieren": generate_reports,

        "Warnsystem": warning_system

    }



    choice = st.sidebar.radio("Wähle eine Seite:", list(options.keys()))

    setup_database()  # Ensure the database is initialized before loading any page

    st.sidebar.markdown("---")

    options[choice]()  # Load the selected module



if __name__ == "__main__":

    main()
