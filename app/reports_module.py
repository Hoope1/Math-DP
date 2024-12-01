import streamlit as st
import sqlite3
import pandas as pd
import os
from reportlab.pdfgen import canvas

# Absoluter Pfad zur Datenbank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'math_course_management.db')

# Funktion, um die Testergebnisse eines Teilnehmers zu laden
def lade_testergebnisse(teilnehmer_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = f"""
            SELECT 
                test_datum AS Testdatum, 
                brueche_erreichte_punkte AS Brüche, 
                textaufgaben_erreichte_punkte AS Textaufgaben, 
                raumvorstellung_erreichte_punkte AS Raumvorstellung, 
                gleichungen_erreichte_punkte AS Gleichungen, 
                grundrechenarten_erreichte_punkte AS Grundrechenarten, 
                zahlenraum_erreichte_punkte AS Zahlenraum, 
                gesamt_erreichte_punkte AS Gesamtpunkte, 
                gesamt_prozent AS Gesamtprozent
            FROM tests
            WHERE teilnehmer_id = ?
            ORDER BY test_datum ASC
            """
            return pd.read_sql(query, conn, params=(teilnehmer_id,))
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Testergebnisse: {e}")
        return pd.DataFrame()

# Funktion, um einen Bericht im PDF-Format zu erstellen
def erstelle_bericht(teilnehmer_name, testergebnisse):
    try:
        report_file = f"{teilnehmer_name}_Bericht.pdf"
        pdf = canvas.Canvas(report_file)

        # Titel und Kopfzeilen
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 800, f"Bericht für Teilnehmer: {teilnehmer_name}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 780, "Testergebnisse:")
        
        # Testergebnisse einfügen
        y = 760
        for _, row in testergebnisse.iterrows():
            pdf.drawString(100, y, f"Datum: {row['Testdatum']}, Punkte: {row['Gesamtpunkte']}, Prozent: {row['Gesamtprozent']}%")
            y -= 20
            if y < 100:  # Neue Seite, falls Platz nicht ausreicht
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 800

        pdf.save()
        return report_file
    except Exception as e:
        st.error(f"Fehler beim Erstellen des Berichts: {e}")
        return None

# Hauptfunktion für das Berichtssystem
def main():
    st.header("Berichtserstellung")

    # Teilnehmerdaten laden
    try:
        with sqlite3.connect(DB_PATH) as conn:
            teilnehmer = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")
        return

    if teilnehmer.empty:
        st.warning("Keine Teilnehmer vorhanden.")
        return

    # Teilnehmerauswahl
    teilnehmer_name = st.selectbox("Wähle einen Teilnehmer", teilnehmer["name"].tolist())
    ausgewählter_teilnehmer = teilnehmer[teilnehmer["name"] == teilnehmer_name].iloc[0]

    # Testergebnisse laden
    testergebnisse = lade_testergebnisse(ausgewählter_teilnehmer["teilnehmer_id"])
    if testergebnisse.empty:
        st.warning("Keine Testergebnisse für diesen Teilnehmer vorhanden.")
        return

    # Testergebnisse anzeigen
    st.subheader(f"Testergebnisse für {teilnehmer_name}")
    st.dataframe(testergebnisse)

    # Bericht erstellen
    if st.button("Bericht erstellen"):
        report_file = erstelle_bericht(teilnehmer_name, testergebnisse)
        if report_file:
            st.success(f"Bericht wurde erfolgreich erstellt: {report_file}")
            with open(report_file, "rb") as file:
                st.download_button(
                    label="Bericht herunterladen",
                    data=file,
                    file_name=report_file,
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
