import sqlite3
import pandas as pd
import streamlit as st
import os
from datetime import datetime

# Absoluter Pfad zur Datenbank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')

# Funktion, um Teilnehmerdaten zu laden und deren Status zu berechnen
def lade_teilnehmer():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                name AS Name, 
                sv_nummer AS Sozialversicherungsnummer, 
                geschlecht AS Geschlecht, 
                eintrittsdatum AS Eintrittsdatum, 
                austrittsdatum AS Austrittsdatum,
                CASE
                    WHEN julianday(austrittsdatum) >= julianday('now') THEN 'Aktiv'
                    ELSE 'Inaktiv'
                END AS Status
            FROM teilnehmer
            """
            teilnehmer = pd.read_sql(query, conn)
            return teilnehmer
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")
        return pd.DataFrame()

# Funktion, um neue Teilnehmer hinzuzufügen
def neuer_teilnehmer_hinzufuegen(name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            INSERT INTO teilnehmer (name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum)
            VALUES (?, ?, ?, ?, ?)
            """
            conn.execute(query, (name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum))
            conn.commit()
            st.success(f"Teilnehmer {name} wurde erfolgreich hinzugefügt!")
    except sqlite3.Error as e:
        st.error(f"Fehler beim Hinzufügen eines Teilnehmers: {e}")

# Streamlit-App-Layout
def main():
    st.header("Teilnehmerverwaltung")

    # Teilnehmerdaten anzeigen
    teilnehmer = lade_teilnehmer()
    if teilnehmer.empty:
        st.warning("Es wurden keine Teilnehmer gefunden.")
    else:
        st.dataframe(teilnehmer)

    # Formular für neue Teilnehmer
    st.subheader("Neuen Teilnehmer hinzufügen")
    with st.form("neuer_teilnehmer_formular"):
        name = st.text_input("Name")
        sv_nummer = st.text_input("Sozialversicherungsnummer")
        geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
        eintrittsdatum = st.date_input("Eintrittsdatum", min_value=datetime.today())
        austrittsdatum = st.date_input("Austrittsdatum", min_value=eintrittsdatum)
        speichern = st.form_submit_button("Hinzufügen")
        if speichern:
            neuer_teilnehmer_hinzufuegen(
                name, 
                sv_nummer, 
                geschlecht, 
                eintrittsdatum.strftime("%Y-%m-%d"), 
                austrittsdatum.strftime("%Y-%m-%d")
            )

if __name__ == "__main__":
    main()
