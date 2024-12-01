import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Absoluten Pfad zur Datenbank verwenden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')
conn = sqlite3.connect(DB_PATH)

# Prognosedaten laden
def load_prognoses():
    query = """
    SELECT prognose_datum, prognose_brueche, prognose_textaufgaben,
           prognose_raumvorstellung, prognose_gleichungen,
           prognose_grundrechenarten, prognose_zahlenraum, prognose_gesamt
    FROM prognosen
    """
    return pd.read_sql(query, conn)

# Hauptfunktion für die Visualisierung der Prognosen
def main():
    st.header("Prognosen")

    # Prognosedaten laden
    prognoses = load_prognoses()
    if prognoses.empty:
        st.warning("Keine Prognosedaten verfügbar.")
        return

    # Diagramm erstellen
    fig = px.line(
        prognoses.melt(id_vars=["prognose_datum"], var_name="Kategorie", value_name="Prozent"),
        x="prognose_datum", y="Prozent", color="Kategorie",
        title="Prognosen für die mathematischen Kategorien",
        labels={"prognose_datum": "Datum", "Prozent": "Prognose (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
