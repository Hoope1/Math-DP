import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

# Absoluten Pfad zur Datenbank verwenden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')
conn = sqlite3.connect(DB_PATH)

# Warnungen für Teilnehmer mit nahendem Austrittsdatum
def check_warnings():
    query = """
    SELECT name, austrittsdatum FROM teilnehmer
    WHERE julianday(austrittsdatum) - julianday('now') <= 21
    """
    return pd.read_sql(query, conn)

# Hauptfunktion für das Warnsystem
def main():
    st.header("Warnsystem")

    warnings = check_warnings()
    if warnings.empty:
        st.info("Keine Warnungen.")
    else:
        st.warning("Teilnehmer mit nahendem Austrittsdatum:")
        st.dataframe(warnings)

if __name__ == "__main__":
    main()
