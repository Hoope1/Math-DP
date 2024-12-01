import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Absoluter Pfad zur Datenbank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')

# Funktion, um Durchschnittswerte für die Kategorien zu berechnen
def berechne_durchschnittswerte():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                AVG(brueche_erreichte_punkte) AS Brüche, 
                AVG(textaufgaben_erreichte_punkte) AS Textaufgaben, 
                AVG(raumvorstellung_erreichte_punkte) AS Raumvorstellung, 
                AVG(gleichungen_erreichte_punkte) AS Gleichungen, 
                AVG(grundrechenarten_erreichte_punkte) AS Grundrechenarten, 
                AVG(zahlenraum_erreichte_punkte) AS Zahlenraum
            FROM tests
            """
            durchschnitt = pd.read_sql(query, conn)
            return durchschnitt
    except sqlite3.Error as e:
        st.error(f"Fehler beim Berechnen der Durchschnittswerte: {e}")
        return pd.DataFrame()

# Hauptfunktion für das Dashboard und Layout
def main():
    st.header("Dashboard: Übersicht der Durchschnittswerte")

    # Durchschnittswerte berechnen
    durchschnittswerte = berechne_durchschnittswerte()
    if durchschnittswerte.empty or durchschnittswerte.isna().all().all():
        st.warning("Keine Daten für Durchschnittswerte verfügbar.")
        return

    # Balkendiagramm erstellen
    df_durchschnitt = durchschnittswerte.melt(var_name="Kategorie", value_name="Durchschnittliche Punkte")
    fig = px.bar(
        df_durchschnitt,
        x="Kategorie",
        y="Durchschnittliche Punkte",
        title="Durchschnittliche Leistung nach Kategorien",
        labels={"Durchschnittliche Punkte": "Punkte", "Kategorie": "Kategorie"},
        text="Durchschnittliche Punkte"
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Kategorie",
        yaxis_title="Durchschnittliche Punkte",
        template="simple_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Option zur Datenanzeige
    if st.checkbox("Rohdaten anzeigen"):
        st.subheader("Durchschnittswerte der Kategorien")
        st.dataframe(durchschnittswerte)

if __name__ == "__main__":
    main()
