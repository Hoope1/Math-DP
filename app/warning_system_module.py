import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Teilnehmer mit bevorstehendem Austrittsdatum laden
def load_warnings():
    query = """
    SELECT name, austrittsdatum
    FROM teilnehmer
    WHERE austrittsdatum BETWEEN ? AND ?
    """
    today = datetime.today()
    warning_date = today + timedelta(weeks=3)
    warnings = pd.read_sql(query, conn, params=(today.strftime("%Y-%m-%d"), warning_date.strftime("%Y-%m-%d")))
    warnings["austrittsdatum"] = pd.to_datetime(warnings["austrittsdatum"])
    return warnings

# Hauptfunktion für das Warnsystem
def main():
    st.header("Warnsystem")

    # Teilnehmer mit bevorstehendem Austrittsdatum prüfen
    warnings = load_warnings()

    if warnings.empty:
        st.success("Keine Teilnehmer verlassen den Kurs in den nächsten drei Wochen.")
    else:
        st.warning("Die folgenden Teilnehmer verlassen den Kurs bald:")
        st.table(warnings)

if __name__ == "__main__":
    main()
