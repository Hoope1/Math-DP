import pandas as pd
from flaml import AutoML
import sqlite3
import os

# Datenbankpfad im temporären Streamlit-Verzeichnis
BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")
DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')

# Funktion zur Vorbereitung der Daten für AutoML
def lade_daten_fuer_automl():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                brueche_erreichte_punkte AS Brüche, 
                textaufgaben_erreichte_punkte AS Textaufgaben, 
                raumvorstellung_erreichte_punkte AS Raumvorstellung, 
                gleichungen_erreichte_punkte AS Gleichungen, 
                grundrechenarten_erreichte_punkte AS Grundrechenarten, 
                zahlenraum_erreichte_punkte AS Zahlenraum, 
                gesamt_prozent AS Gesamtprozent
            FROM tests
            """
            daten = pd.read_sql(query, conn)
            return daten
    except sqlite3.Error as e:
        print(f"Fehler beim Laden der Daten: {e}")
        return pd.DataFrame()

# Funktion zur Durchführung von AutoML
def durchfuehren_automl(daten):
    if daten.empty:
        print("Keine Daten für das Training verfügbar.")
        return None

    # Merkmale (X) und Zielwert (y) definieren
    X = daten.drop(columns=["Gesamtprozent"])
    y = daten["Gesamtprozent"]

    # AutoML-Instanz erstellen
    automl = AutoML()
    automl.fit(X_train=X, y_train=y, task="regression", time_budget=60)  # Zeitbudget: 60 Sekunden

    return automl

# Prognosen mit dem trainierten Modell erstellen
def erstelle_prognose(automl_model, neue_daten):
    try:
        prognosen = automl_model.predict(neue_daten)
        return prognosen
    except Exception as e:
        print(f"Fehler bei der Prognoseerstellung: {e}")
        return None
