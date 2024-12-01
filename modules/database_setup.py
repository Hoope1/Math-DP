import os
import sqlite3

# Fallback für Umgebungen ohne __file__
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()  # Aktuelles Arbeitsverzeichnis verwenden

# Setup the database path and create the directory if it doesn't exist
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the 'data' directory exists
DB_PATH = os.path.join(DATA_DIR, 'math_course_management.db')

# Function to initialize the database and create tables if they don't exist
def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create table for participants
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

        # Create table for tests
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

        # Create table for prognoses
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

# Initialize the database
initialize_database()
print(f"Database initialized at: {DB_PATH}")
