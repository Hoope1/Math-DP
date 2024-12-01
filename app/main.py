import streamlit as st

from modules.database_setup import initialize_database

from app.participant_filter_module import main as manage_participants

from app.test_input_feature import main as test_input

from app.visualization_prognoses import main as visualize_prognoses

from app.reports_module import main as generate_reports

from app.warning_system_module import main as warning_system

from app.design_layout_module import main as layout_dashboard



# Initialize database

def setup_database():

    try:

        initialize_database()

        st.success("Database initialized successfully.")

    except Exception as e:

        st.error("Failed to initialize the database.")

        st.error(f"Error details: {e}")



# Main function for Streamlit App

def main():

    st.set_page_config(page_title="Math Course Management", layout="wide")



    # Sidebar navigation

    st.sidebar.title("Navigation")

    options = {

        "Dashboard": layout_dashboard,

        "Manage Participants": manage_participants,

        "Test Input": test_input,

        "Visualization": visualize_prognoses,

        "Generate Reports": generate_reports,

        "Warning System": warning_system,

    }

    choice = st.sidebar.radio("Go to", list(options.keys()))



    # Execute the chosen module

    if choice in options:

        options[choice]()

    else:

        st.error("Invalid selection.")



# Execute the app

if __name__ == "__main__":

    setup_database()

    main()

"""



# Save the optimized main.py file

with open(main_py_path, 'w') as file:

    file.write(optimized_main_py)
