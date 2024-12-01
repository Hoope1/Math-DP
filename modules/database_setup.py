import os

import sqlite3



# Absoluter Pfad zur Datenbank im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um die Datenbank und Tabellen zu initialisieren

def initialize_database():

    # Sicherstellen, dass das Verzeichnis existiert

    os.makedirs(BASE_DIR, exist_ok=True)

    try:

        with sqlite3.connect(DB_PATH) as conn:

            cursor = conn.cursor()



            # Tabelle: Teilnehmer

            cursor.execute("CREATE TABLE IF NOT EXISTS teilnehmer (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, sv_nummer TEXT UNIQUE NOT NULL, geschlecht TEXT NOT NULL, eintrittsdatum DATE NOT NULL, austrittsdatum DATE NOT NULL)")



            # Tabelle: Testdaten

            cursor.execute("CREATE TABLE IF NOT EXISTS testdaten (id INTEGER PRIMARY KEY AUTOINCREMENT, teilnehmer_id INTEGER NOT NULL, test_datum DATE NOT NULL, brueche_err REAL, gleichungen_err REAL, textbeispiele_err REAL, raumvorstellung_err REAL, grundrechnungsarten_err REAL, zahlenraum_err REAL, FOREIGN KEY (teilnehmer_id) REFERENCES teilnehmer (id))")



            conn.commit()

            print("Datenbank und Tabellen erfolgreich initialisiert.")

    except sqlite3.Error as e:

        print(f"Fehler bei der Initialisierung der Datenbank: {e}")



if __name__ == "__main__":

    initialize_database()
