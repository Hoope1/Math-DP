import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Durchschnittswerte für das Dashboard berechnen
def calculate_averages():
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
    return pd.read_sql(query, conn)

# Hauptfunktion für das Layout und Dashboard
def main():
    st.header("Dashboard")

    # Durchschnittswerte berechnen
    averages = calculate_averages()
    if averages.empty or averages.isna().all().all():
        st.warning("Keine Testdaten verfügbar.")
        return

    # Balkendiagramm für Durchschnittswerte
    avg_df = averages.melt(var_name="Kategorie", value_name="Durchschnittliche Leistung (%)")
    fig = px.bar(
        avg_df,
        x="Kategorie",
        y="Durchschnittliche Leistung (%)",
        title="Durchschnittliche Leistung nach Kategorien",
        labels={"Durchschnittliche Leistung (%)": "Leistung (%)", "Kategorie": "Kategorie"}
    )
    fig.update_layout(xaxis_title="Kategorie", yaxis_title="Leistung (%)")
    st.plotly_chart(fig, use_container_width=True)

    # Placeholder für zukünftige Diagramme
    st.subheader("Leistungstrends")
    st.info("Trendanalysen werden später hinzugefügt.")

if __name__ == "__main__":
    main()
  
