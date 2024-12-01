import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

# Datenbankpfad im temporären Streamlit-Verzeichnis
BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")
DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')

# Funktion, um Teilnehmer mit nahendem Austrittsdatum zu laden
def lade_warnungen():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                name AS Name, 
                austrittsdatum AS Austrittsdatum
            FROM teilnehmer
            WHERE julianday(austrittsdatum) - julianday('now') <= 21
            AND julianday(austrittsdatum) - julianday('now') > 0
            """
            warnungen = pd.read_sql(query, conn)
            warnungen["Austrittsdatum"] = pd.to_datetime(warnungen["Austrittsdatum"]).dt.strftime("%d.%m.%Y")
            return warnungen
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Warnungen: {e}")
        return pd.DataFrame()

# Funktion, um inaktive Teilnehmer zu laden
def lade_inaktive_teilnehmer():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                name AS Name, 
                austrittsdatum AS Austrittsdatum
            FROM teilnehmer
            WHERE julianday(austrittsdatum) < julianday('now')
            """
            inaktive = pd.read_sql(query, conn)
            inaktive["Austrittsdatum"] = pd.to_datetime(inaktive["Austrittsdatum"]).dt.strftime("%d.%m.%Y")
            return inaktive
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der inaktiven Teilnehmer: {e}")
        return pd.DataFrame()

# Hauptfunktion für das Warnsystem
def main():
    st.header("Warnsystem")

    # Teilnehmer mit nahendem Austrittsdatum laden
    warnungen = lade_warnungen()

    if warnungen.empty:
        st.info("Keine Teilnehmer mit baldigen Austrittsdaten gefunden.")
    else:
        st.warning("Folgende Teilnehmer haben ein nahendes Austrittsdatum:")
        st.dataframe(warnungen)

    # Option zur Anzeige inaktiver Teilnehmer
    if st.checkbox("Inaktive Teilnehmer anzeigen"):
        inaktive_teilnehmer = lade_inaktive_teilnehmer()
        if inaktive_teilnehmer.empty:
            st.info("Es gibt keine inaktiven Teilnehmer.")
        else:
            st.subheader("Inaktive Teilnehmer")
            st.dataframe(inaktive_teilnehmer)

if __name__ == "__main__":
    main()
