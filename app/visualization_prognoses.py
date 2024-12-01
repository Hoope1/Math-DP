import streamlit as st

import sqlite3

import pandas as pd

import plotly.express as px

import os

from modules.flaml_module import lade_daten_fuer_automl, durchfuehren_automl, erstelle_prognose



# Datenbankpfad im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um Prognosedaten aus der Datenbank zu laden

def lade_prognosedaten():

    try:

        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "SELECT "

                "teilnehmer_id, test_datum, brueche_err, gleichungen_err, textbeispiele_err, "

                "raumvorstellung_err, grundrechnungsarten_err, zahlenraum_err "

                "FROM testdaten "

                "ORDER BY test_datum"

            )

            df = pd.read_sql_query(query, conn)

            return df

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Prognosedaten: {e}")

        return pd.DataFrame()



# Funktion, um die Prognoseergebnisse zu visualisieren

def visualisiere_prognosen(prognose_df, original_df):

    try:

        merged_df = pd.concat([original_df, prognose_df], ignore_index=True)

        fig = px.line(

            merged_df,

            x="Datum",

            y="Wert",

            color="Kategorie",

            title="Prognose der Testergebnisse",

            labels={"Wert": "Leistung (%)", "Datum": "Datum"}

        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:

        st.error(f"Fehler bei der Visualisierung: {e}")



# Hauptfunktion für die Streamlit-Seite

def prognose_visualisierung():

    st.title("Prognosevisualisierung")

    st.markdown("Erstellen und visualisieren Sie Prognosen basierend auf den bisherigen Testergebnissen.")



    # Laden der ursprünglichen Daten

    original_df = lade_prognosedaten()

    if original_df.empty:

        st.warning("Keine Daten zum Visualisieren verfügbar.")

        return



    st.markdown("### Bisherige Testergebnisse")

    st.dataframe(original_df, use_container_width=True)



    # AutoML-Prognose durchführen

    if st.button("Prognose erstellen"):

        try:

            train_df, test_df = lade_daten_fuer_automl(original_df)

            model = durchfuehren_automl(train_df)

            prognose_df = erstelle_prognose(model, test_df)



            st.markdown("### Prognoseergebnisse")

            st.dataframe(prognose_df, use_container_width=True)



            # Visualisierung der Prognose

            visualisiere_prognosen(prognose_df, original_df)

        except Exception as e:

            st.error(f"Fehler bei der Prognoseerstellung: {e}")



if __name__ == "__main__":

    prognose_visualisierung()
