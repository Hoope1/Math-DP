import sqlite3

import pandas as pd

import streamlit as st

import os

from datetime import datetime



# Datenbankpfad im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um Teilnehmerdaten zu laden und den Status zu berechnen

def lade_teilnehmer():

    try:

        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "SELECT "

                "name AS Name, "

                "sv_nummer AS Sozialversicherungsnummer, "

                "geschlecht AS Geschlecht, "

                "eintrittsdatum AS Eintrittsdatum, "

                "austrittsdatum AS Austrittsdatum, "

                "CASE "

                "WHEN austrittsdatum >= DATE('now') THEN 'Aktiv' "

                "ELSE 'Inaktiv' "

                "END AS Status "

                "FROM teilnehmer"

            )

            df = pd.read_sql_query(query, conn)

            return df

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")

        return pd.DataFrame()



# Streamlit-Funktion zur Anzeige und Filterung der Teilnehmerdaten

def teilnehmer_ansicht():

    st.title("Teilnehmerverwaltung")

    st.markdown("Hier können Sie die Teilnehmerdaten anzeigen und filtern.")



    # Teilnehmerdaten laden

    df = lade_teilnehmer()



    if not df.empty:

        # Filteroptionen

        status_filter = st.selectbox("Status filtern", ["Alle", "Aktiv", "Inaktiv"])

        if status_filter != "Alle":

            df = df[df["Status"] == status_filter]



        # Anzeige der Daten

        st.dataframe(df, use_container_width=True)

    else:

        st.warning("Keine Teilnehmerdaten verfügbar.")



if __name__ == "__main__":

    teilnehmer_ansicht()

"""



# Save the corrected file

with open(participant_filter_module_path, 'w') as file:

    file.write(optimized_participant_filter_module)
