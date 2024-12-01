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

            # Tabelle für Teilnehmer erstellen
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS teilnehmer (
                teilnehmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sv_nummer TEXT NOT NULL UNIQUE,
                geschlecht TEXT NOT NULL,
                eintrittsdatum DATE NOT NULL,
                austrittsdatum DATE NOT NULL
            )
            """)

            # Tabelle für Tests erstellen
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                teilnehmer_id INTEGER NOT NULL,
                test_datum DATE NOT NULL,
                brueche_erreichte_punkte INTEGER NOT NULL,
                brueche_max_punkte INTEGER NOT NULL,
                textaufgaben_erreichte_punkte INTEGER NOT NULL,
                textaufgaben_max_punkte INTEGER NOT NULL,
                raumvorstellung_erreichte_punkte INTEGER NOT NULL,
                raumvorstellung_max_punkte INTEGER NOT NULL,
                gleichungen_erreichte_punkte INTEGER NOT NULL,
                gleichungen_max_punkte INTEGER NOT NULL,
                grundrechenarten_erreichte_punkte INTEGER NOT NULL,
                grundrechenarten_max_punkte INTEGER NOT NULL,
                zahlenraum_erreichte_punkte INTEGER NOT NULL,
                zahlenraum_max_punkte INTEGER NOT NULL,
                gesamt_erreichte_punkte INTEGER NOT NULL,
                gesamt_max_punkte INTEGER DEFAULT 100 NOT NULL,
                gesamt_prozent FLOAT NOT NULL,
                FOREIGN KEY (teilnehmer_id) REFERENCES teilnehmer (teilnehmer_id)
            )
            """)

            # Tabelle für Prognosen erstellen
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS prognosen (
                prognose_id INTEGER PRIMARY KEY AUTOINCREMENT,
                teilnehmer_id INTEGER NOT NULL,
                prognose_datum DATE NOT NULL,
                prognose_brueche FLOAT,
                prognose_textaufgaben FLOAT,
                prognose_raumvorstellung FLOAT,
                prognose_gleichungen FLOAT,
                prognose_grundrechenarten FLOAT,
                prognose_zahlenraum FLOAT,
                prognose_gesamt FLOAT,
                FOREIGN KEY (teilnehmer_id) REFERENCES teilnehmer (teilnehmer_id)
            )
            """)

            conn.commit()
            print(f"Datenbank initialisiert unter: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"Fehler beim Initialisieren der Datenbank: {e}")

# Datenbank initialisieren
initialize_database()
