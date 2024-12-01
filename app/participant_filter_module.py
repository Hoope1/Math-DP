import streamlit as st
import pandas as pd
import sqlite3
import os

# Absoluten Pfad zur Datenbank verwenden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')
conn = sqlite3.connect(DB_PATH)

# Teilnehmerdaten laden und den Status berechnen
def load_participants():
    query = (
        "SELECT teilnehmer_id, name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum "
        "FROM teilnehmer"
    )
    participants = pd.read_sql(query, conn)
    participants["eintrittsdatum"] = pd.to_datetime(participants["eintrittsdatum"])
    participants["austrittsdatum"] = pd.to_datetime(participants["austrittsdatum"])
    today = pd.Timestamp.today()
    participants["status"] = participants.apply(
        lambda row: "Aktiv" if row["eintrittsdatum"] <= today <= row["austrittsdatum"] else "Inaktiv", axis=1
    )
    return participants

# Hauptfunktion für die Teilnehmerverwaltung
def main():
    st.header("Teilnehmerverwaltung")

    # Teilnehmerdaten laden
    participants = load_participants()

    # Filteroptionen
    filter_option = st.radio("Filter:", ["Alle Teilnehmer", "Nur aktive Teilnehmer"])
    if filter_option == "Nur aktive Teilnehmer":
        participants = participants[participants["status"] == "Aktiv"]

    # Teilnehmerdaten anzeigen
    st.subheader("Teilnehmerliste")
    if participants.empty:
        st.warning("Keine Teilnehmerdaten verfügbar.")
    else:
        st.dataframe(participants)

if __name__ == "__main__":
    main()
