import streamlit as st

import sqlite3

import pandas as pd

import plotly.express as px

import os



# Datenbankpfad im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um Durchschnittswerte für die Kategorien zu berechnen

def berechne_durchschnittswerte():

    try:

        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "SELECT "

                "AVG(brueche_err) AS Brueche, "

                "AVG(gleichungen_err) AS Gleichungen, "

                "AVG(textbeispiele_err) AS Textbeispiele, "

                "AVG(raumvorstellung_err) AS Raumvorstellung, "

                "AVG(grundrechnungsarten_err) AS Grundrechnungsarten, "

                "AVG(zahlenraum_err) AS Zahlenraum "

                "FROM testdaten"

            )

            df = pd.read_sql_query(query, conn)

            return df

    except sqlite3.Error as e:

        st.error(f"Fehler beim Abrufen der Durchschnittswerte: {e}")

        return None



# Visualisierung der Durchschnittswerte

def visualisiere_durchschnittswerte(df):

    if df is not None and not df.empty:

        df_melted = df.melt(var_name="Kategorie", value_name="Durchschnitt")

        fig = px.bar(

            df_melted, 

            x="Kategorie", 

            y="Durchschnitt", 

            title="Durchschnittswerte der Kategorien",

            labels={"Durchschnitt": "Durchschnitt (%)", "Kategorie": "Kategorien"}

        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("Keine Daten zum Visualisieren vorhanden.")



# Hauptlayout für das Dashboard

def main():

    st.title("Dashboard für Durchschnittswerte")

    st.markdown("Hier sehen Sie die Durchschnittswerte aller Kategorien basierend auf den vorhandenen Testergebnissen.")

    

    # Durchschnittswerte berechnen

    df = berechne_durchschnittswerte()

    

    # Visualisierung der Durchschnittswerte

    visualisiere_durchschnittswerte(df)



if __name__ == "__main__":

    main()
