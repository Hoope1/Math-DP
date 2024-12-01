import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Datenbankpfad im temporären Streamlit-Verzeichnis
BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")
DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')

# Funktion, um Testergebnisse hinzuzufügen
def testeingabe_hinzufuegen(teilnehmer_id, test_datum, punkte_kategorien, max_punkte_kategorien):
    try:
        gesamt_punkte = sum(punkte_kategorien.values())
        gesamt_max_punkte = sum(max_punkte_kategorien.values())
        gesamt_prozent = round((gesamt_punkte / gesamt_max_punkte) * 100, 2) if gesamt_max_punkte > 0 else 0

        with sqlite3.connect(DB_PATH) as conn:
            query = """
            INSERT INTO tests (
                teilnehmer_id, test_datum, 
                brueche_erreichte_punkte, brueche_max_punkte,
                textaufgaben_erreichte_punkte, textaufgaben_max_punkte,
                raumvorstellung_erreichte_punkte, raumvorstellung_max_punkte,
                gleichungen_erreichte_punkte, gleichungen_max_punkte,
                grundrechenarten_erreichte_punkte, grundrechenarten_max_punkte,
                zahlenraum_erreichte_punkte, zahlenraum_max_punkte,
                gesamt_erreichte_punkte, gesamt_max_punkte, gesamt_prozent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            conn.execute(query, (
                teilnehmer_id, test_datum,
                punkte_kategorien["Brüche"], max_punkte_kategorien["Brüche"],
                punkte_kategorien["Textaufgaben"], max_punkte_kategorien["Textaufgaben"],
                punkte_kategorien["Raumvorstellung"], max_punkte_kategorien["Raumvorstellung"],
                punkte_kategorien["Gleichungen"], max_punkte_kategorien["Gleichungen"],
                punkte_kategorien["Grundrechenarten"], max_punkte_kategorien["Grundrechenarten"],
                punkte_kategorien["Zahlenraum"], max_punkte_kategorien["Zahlenraum"],
                gesamt_punkte, gesamt_max_punkte, gesamt_prozent
            ))
            conn.commit()
            st.success(f"Testergebnisse wurden erfolgreich gespeichert!")
    except sqlite3.Error as e:
        st.error(f"Fehler beim Speichern der Testergebnisse: {e}")

# Hauptfunktion für die Testergebniseingabe
def main():
    st.header("Testergebnisse eingeben")

    # Teilnehmerdaten laden
    try:
        with sqlite3.connect(DB_PATH) as conn:
            teilnehmer = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")
        return

    if teilnehmer.empty:
        st.warning("Es sind keine Teilnehmer vorhanden. Bitte zuerst Teilnehmer hinzufügen.")
        return

    # Teilnehmerauswahl
    teilnehmer_name = st.selectbox("Wähle einen Teilnehmer", teilnehmer["name"].tolist())
    ausgewählter_teilnehmer = teilnehmer[teilnehmer["name"] == teilnehmer_name].iloc[0]

    # Formular für Testergebnisse
    with st.form("testeingabe_formular"):
        st.subheader(f"Testergebnisse für {teilnehmer_name} eingeben")
        test_datum = st.date_input("Testdatum", max_value=datetime.today())
        
        punkte_kategorien = {}
        max_punkte_kategorien = {}
        kategorien = ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]

        for kategorie in kategorien:
            punkte_kategorien[kategorie] = st.number_input(f"Erreichte Punkte in {kategorie}", min_value=0, max_value=100, value=0)
            max_punkte_kategorien[kategorie] = st.number_input(f"Maximale Punkte in {kategorie}", min_value=1, max_value=100, value=100)

        speichern = st.form_submit_button("Speichern")
        if speichern:
            testeingabe_hinzufuegen(
                ausgewählter_teilnehmer["teilnehmer_id"], 
                test_datum.strftime("%Y-%m-%d"),
                punkte_kategorien, 
                max_punkte_kategorien
            )

if __name__ == "__main__":
    main()
