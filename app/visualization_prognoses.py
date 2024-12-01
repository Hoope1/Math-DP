import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Prognosedaten für einen bestimmten Teilnehmer laden
def load_prognoses(participant_id):
    query = """
    SELECT prognose_datum, prognose_brueche, prognose_textaufgaben, 
           prognose_raumvorstellung, prognose_gleichungen, prognose_grundrechenarten, 
           prognose_zahlenraum
    FROM prognosen
    WHERE teilnehmer_id = ?
    """
    return pd.read_sql(query, conn, params=(participant_id,))

# Hauptfunktion zur Visualisierung von Prognosen
def main():
    st.header("Prognosen Visualisieren")

    # Teilnehmerdaten laden
    participants = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    if participants.empty:
        st.warning("Keine Teilnehmer vorhanden. Bitte zuerst Teilnehmer hinzufügen.")
        return

    # Teilnehmerauswahl
    participant_name = st.selectbox("Wähle einen Teilnehmer", participants["name"].tolist())
    selected_participant = participants[participants["name"] == participant_name].iloc[0]

    # Prognosedaten laden
    prognoses = load_prognoses(selected_participant["teilnehmer_id"])
    if prognoses.empty:
        st.warning(f"Keine Prognosedaten für {participant_name} verfügbar.")
        return

    # Daten für die Visualisierung vorbereiten
    prognoses["prognose_datum"] = pd.to_datetime(prognoses["prognose_datum"])
    categories = ["prognose_brueche", "prognose_textaufgaben", "prognose_raumvorstellung", 
                  "prognose_gleichungen", "prognose_grundrechenarten", "prognose_zahlenraum"]
    prognoses_melted = prognoses.melt(id_vars=["prognose_datum"], value_vars=categories, 
                                      var_name="Kategorie", value_name="Prozent")
    prognoses_melted["Kategorie"] = prognoses_melted["Kategorie"].str.replace("prognose_", "")

    # Liniendiagramm erstellen
    fig = px.line(
        prognoses_melted,
        x="prognose_datum",
        y="Prozent",
        color="Kategorie",
        title=f"Prognosen der nächsten 30 Tage für {participant_name}",
        labels={"prognose_datum": "Datum", "Prozent": "Leistung (%)"}
    )
    fig.update_layout(legend_title_text="Kategorie", xaxis_title="Datum", yaxis_title="Prozent (%)")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
