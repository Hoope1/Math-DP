import streamlit as st
import sqlite3
import pandas as pd
import os
from reportlab.pdfgen import canvas

# Absoluten Pfad zur Datenbank verwenden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')
conn = sqlite3.connect(DB_PATH)

# Teilnehmerberichte erstellen
def generate_report(participant_id):
    query = f"""
    SELECT * FROM tests WHERE teilnehmer_id = {participant_id}
    """
    tests = pd.read_sql(query, conn)

    if tests.empty:
        return "Keine Daten verfügbar."

    report_file = f"Bericht_Teilnehmer_{participant_id}.pdf"
    pdf = canvas.Canvas(report_file)

    # PDF-Erstellung
    pdf.drawString(100, 800, f"Bericht für Teilnehmer-ID: {participant_id}")
    pdf.drawString(100, 780, "Testergebnisse:")
    y = 760
    for index, row in tests.iterrows():
        pdf.drawString(100, y, f"Testdatum: {row['test_datum']}, Punkte: {row['gesamt_erreichte_punkte']}/{row['gesamt_max_punkte']}")
        y -= 20

    pdf.save()
    return report_file

# Hauptfunktion für Berichte
def main():
    st.header("Berichte")

    participants = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    if participants.empty:
        st.warning("Keine Teilnehmer verfügbar.")
        return

    participant_name = st.selectbox("Wähle einen Teilnehmer", participants["name"].tolist())
    selected_participant = participants[participants["name"] == participant_name].iloc[0]

    if st.button("Bericht erstellen"):
        report_path = generate_report(selected_participant["teilnehmer_id"])
        st.success(f"Bericht erstellt: {report_path}")

if __name__ == "__main__":
    main()
