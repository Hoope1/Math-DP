import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Tabellen erstellen
def create_tables():
    # Tabelle für Teilnehmer
    conn.execute("""
    CREATE TABLE IF NOT EXISTS teilnehmer (
        teilnehmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sv_nummer TEXT NOT NULL UNIQUE,
        geschlecht TEXT NOT NULL,
        eintrittsdatum DATE NOT NULL,
        austrittsdatum DATE NOT NULL
    )
    """)
    
    # Tabelle für Tests
    conn.execute("""
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
    
    # Tabelle für Prognosen
    conn.execute("""
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
    print("Datenbanktabellen erfolgreich erstellt.")

if __name__ == "__main__":
    create_tables()
