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

            query = (

                "SELECT "

                "brueche_err AS Brüche, "

                "gleichungen_err AS Gleichungen, "

                "textbeispiele_err AS Textbeispiele, "

                "raumvorstellung_err AS Raumvorstellung, "

                "grundrechnungsarten_err AS Grundrechnungsarten, "

                "zahlenraum_err AS Zahlenraum, "

                "test_datum AS Datum "

                "FROM testdaten"

            )

            df = pd.read_sql_query(query, conn)

            df["Datum"] = pd.to_datetime(df["Datum"])

            df = df.sort_values(by="Datum")

            return df

    except sqlite3.Error as e:

        raise Exception(f"Fehler beim Laden der Daten: {e}")



# Funktion zur Durchführung von AutoML

def durchfuehren_automl(train_df):

    try:

        automl = AutoML()

        x_train = train_df.drop(columns=["Datum"])

        y_train = train_df["Datum"]  # Placeholder: Replace with actual target variable

        automl.fit(x_train, y_train, task="regression", time_budget=600)

        return automl

    except Exception as e:

        raise Exception(f"Fehler bei AutoML: {e}")



# Funktion zur Erstellung von Prognosen

def erstelle_prognose(automl_model, test_df):

    try:

        x_test = test_df.drop(columns=["Datum"])

        test_df["Prognose"] = automl_model.predict(x_test)

        return test_df

    except Exception as e:

        raise Exception(f"Fehler bei der Prognoseerstellung: {e}")



if __name__ == "__main__":

    try:

        data = lade_daten_fuer_automl()

        print("Daten geladen:")

        print(data.head())



        model = durchfuehren_automl(data)

        print("AutoML abgeschlossen.")



        prognose = erstelle_prognose(model, data)

        print("Prognosen erstellt:")

        print(prognose.head())

    except Exception as e:

        print(e)
