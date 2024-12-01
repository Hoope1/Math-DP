import streamlit as st

import sqlite3

import pandas as pd

import os

from datetime import datetime, timedelta



# Datenbankpfad im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um Teilnehmer mit nahendem Austrittsdatum zu laden

def lade_warnungen(tage_vor_austritt=21):

    try:

        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "SELECT "

                "name AS Name, "

                "sv_nummer AS Sozialversicherungsnummer, "

                "geschlecht AS Geschlecht, "

                "eintrittsdatum AS Eintrittsdatum, "

                "austrittsdatum AS Austrittsdatum "

                "FROM teilnehmer "

                "WHERE austrittsdatum BETWEEN DATE('now') AND DATE('now', ?)"

            )

            df = pd.read_sql_query(query, conn, params=(f"+{tage_vor_austritt} days",))

            return df

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Warnungsdaten: {e}")

        return pd.DataFrame()



# Streamlit-Funktion zur Anzeige der Warnungen

def warnsystem():

    st.title("Warnsystem")

    st.markdown("Zeigt Teilnehmer mit einem Austrittsdatum in den nächsten 21 Tagen an.")



    # Eingabe der Anzahl von Tagen bis zum Austritt

    tage_vor_austritt = st.slider("Tage bis zum Austritt", min_value=1, max_value=60, value=21, step=1)



    # Laden der Warnungsdaten

    warnungen_df = lade_warnungen(tage_vor_austritt)



    if not warnungen_df.empty:

        st.markdown("### Teilnehmer mit nahendem Austrittsdatum")

        st.dataframe(warnungen_df, use_container_width=True)

    else:

        st.success("Es gibt keine Teilnehmer mit einem nahenden Austrittsdatum.")



if __name__ == "__main__":

    warnsystem()
