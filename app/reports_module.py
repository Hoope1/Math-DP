import streamlit as st
import pandas as pd
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from io import BytesIO

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Daten für einen Teilnehmer laden
def load_data(participant_id):
    tests_query = """
    SELECT test_datum, brueche_erreichte_punkte, textaufgaben_erreichte_punkte,
           raumvorstellung_erreichte_punkte, gleichungen_erreichte_punkte,
           grundrechenarten_erreichte_punkte, zahlenraum_erreichte_punkte, gesamt_prozent
    FROM tests
    WHERE teilnehmer_id = ?
    """
    prognoses_query = """
    SELECT prognose_datum, prognose_brueche, prognose_textaufgaben,
           prognose_raumvorstellung, prognose_gleichungen, prognose_grundrechenarten,
           prognose_zahlenraum, prognose_gesamt
    FROM prognosen
    WHERE teilnehmer_id = ?
    """
    tests = pd.read_sql(tests_query, conn, params=(participant_id,))
    prognoses = pd.read_sql(prognoses_query, conn, params=(participant_id,))
    return tests, prognoses

# PDF-Bericht erstellen
def generate_pdf(participant_name, tests, prognoses):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Bericht für {participant_name}")

    # Header
    pdf.drawString(100, 750, f"Bericht für {participant_name}")

    # Testdaten hinzufügen
    pdf.drawString(100, 730, "Testergebnisse:")
    y = 710
    for index, row in tests.iterrows():
        pdf.drawString(100, y, f"{row['test_datum']}: {row['gesamt_prozent']}%")
        y -= 20

    # Prognosedaten hinzufügen
    pdf.drawString(100, y, "Prognosen:")
    y -= 20
    for index, row in prognoses.iterrows():
        pdf.drawString(100, y, f"{row['prognose_datum']}: {row['prognose_gesamt']}%")
        y -= 20

    pdf.save()
    buffer.seek(0)
    return buffer

# Excel-Bericht erstellen
def generate_excel(participant_name, tests, prognoses):
    wb = Workbook()
    ws_tests = wb.active
    ws_tests.title = "Testergebnisse"

    # Testdaten schreiben
    ws_tests.append(tests.columns.tolist())
    for row in tests.itertuples(index=False):
        ws_tests.append(row)

    # Neue Tabelle für Prognosen
    ws_prognoses = wb.create_sheet("Prognosen")
    ws_prognoses.append(prognoses.columns.tolist())
    for row in prognoses.itertuples(index=False):
        ws_prognoses.append(row)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

# Hauptfunktion für Berichte in Streamlit
def main():
    st.header("Berichtserstellung")

    # Teilnehmerdaten laden
    participants = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    if participants.empty:
        st.warning("Keine Teilnehmer verfügbar. Bitte zuerst Teilnehmer hinzufügen.")
        return

    # Teilnehmerauswahl
    participant_name = st.selectbox("Wähle einen Teilnehmer", participants["name"].tolist())
    selected_participant = participants[participants["name"] == participant_name].iloc[0]

    # Daten laden
    tests, prognoses = load_data(selected_participant["teilnehmer_id"])

    if st.button("PDF-Bericht erstellen"):
        pdf_buffer = generate_pdf(participant_name, tests, prognoses)
        st.download_button(
            label="PDF herunterladen",
            data=pdf_buffer,
            file_name=f"{participant_name}_Bericht.pdf",
            mime="application/pdf"
        )

    if st.button("Excel-Bericht erstellen"):
        excel_buffer = generate_excel(participant_name, tests, prognoses)
        st.download_button(
            label="Excel herunterladen",
            data=excel_buffer,
            file_name=f"{participant_name}_Bericht.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
