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



        if gesamt_punkte > gesamt_max_punkte:

            return False, "Gesamtpunkte dürfen die maximalen Punkte nicht überschreiten."



        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "INSERT INTO testdaten ("

                "teilnehmer_id, test_datum, brueche_err, gleichungen_err, textbeispiele_err, "

                "raumvorstellung_err, grundrechnungsarten_err, zahlenraum_err"

                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            )

            conn.execute(query, (

                teilnehmer_id, test_datum, punkte_kategorien['Brüche'], punkte_kategorien['Gleichungen'],

                punkte_kategorien['Textbeispiele'], punkte_kategorien['Raumvorstellung'],

                punkte_kategorien['Grundrechnungsarten'], punkte_kategorien['Zahlenraum']

            ))

            conn.commit()

            return True, "Testergebnisse erfolgreich hinzugefügt."

    except sqlite3.Error as e:

        return False, f"Fehler beim Hinzufügen der Testergebnisse: {e}"



# Streamlit-Funktion zur Eingabe von Testergebnissen

def testeingabe():

    st.title("Testeingabe")

    st.markdown("Fügen Sie die Testergebnisse für einen Teilnehmer hinzu.")



    try:

        # Teilnehmerdaten laden

        with sqlite3.connect(DB_PATH) as conn:

            teilnehmer_query = "SELECT id, name FROM teilnehmer"

            teilnehmer_df = pd.read_sql_query(teilnehmer_query, conn)



        if not teilnehmer_df.empty:

            teilnehmer_name = st.selectbox(

                "Wählen Sie einen Teilnehmer aus", 

                teilnehmer_df["name"].tolist()

            )

            if teilnehmer_name:

                teilnehmer_id = teilnehmer_df.loc[teilnehmer_df["name"] == teilnehmer_name, "id"].values[0]

                test_datum = st.date_input("Testdatum", datetime.now()).strftime("%Y-%m-%d")



                punkte_kategorien = {}

                max_punkte_kategorien = {}



                for kategorie in ["Brüche", "Gleichungen", "Textbeispiele", "Raumvorstellung", "Grundrechnungsarten", "Zahlenraum"]:

                    punkte = st.number_input(f"Punkte in {kategorie}", min_value=0, step=1)

                    max_punkte = st.number_input(f"Maximale Punkte in {kategorie}", min_value=1, step=1)

                    punkte_kategorien[kategorie] = punkte

                    max_punkte_kategorien[kategorie] = max_punkte



                if st.button("Testergebnisse speichern"):

                    success, message = testeingabe_hinzufuegen(teilnehmer_id, test_datum, punkte_kategorien, max_punkte_kategorien)

                    if success:

                        st.success(message)

                    else:

                        st.error(message)

        else:

            st.warning("Keine Teilnehmerdaten verfügbar.")

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")



if __name__ == "__main__":

    testeingabe()

"""



# Save the corrected file

with open(test_input_feature_path, 'w') as file:

    file.write(optimized_test_input_feature)
