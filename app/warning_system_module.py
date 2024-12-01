import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

# Absoluter Pfad zur Datenbank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')

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

    # Zusätzliche Optionen
    if st.checkbox("Alle Teilnehmer anzeigen, die bereits inaktiv sind"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                query = """
                SELECT 
                    name AS Name, 
                    austrittsdatum AS Austrittsdatum
                FROM teilnehmer
                WHERE julianday(austrittsdatum) < julianday('now')
                """
                inaktive_teilnehmer = pd.read_sql(query, conn)
                inaktive_teilnehmer["Austrittsdatum"] = pd.to_datetime(inaktive_teilnehmer["Austrittsdatum"]).dt.strftime("%d.%m.%Y")
                if inaktive_teilnehmer.empty:
                    st.info("Es gibt keine inaktiven Teilnehmer.")
                else:
                    st.dataframe(inaktive_teilnehmer)
        except sqlite3.Error as e:
            st.error(f"Fehler beim Laden der inaktiven Teilnehmer: {e}")

if __name__ == "__main__":
    main()
