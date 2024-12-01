import streamlit as st

import sqlite3

import pandas as pd

import os

from reportlab.pdfgen import canvas



# Datenbankpfad im temporären Streamlit-Verzeichnis

BASE_DIR = os.environ.get("STREAMLIT_DATA_DIR", "/tmp")

DB_PATH = os.path.join(BASE_DIR, 'math_course_management.db')



# Funktion, um die Testergebnisse eines Teilnehmers zu laden

def lade_testergebnisse(teilnehmer_id):

    try:

        with sqlite3.connect(DB_PATH) as conn:

            query = (

                "SELECT "

                "test_datum AS Testdatum, "

                "brueche_err AS Brüche, "

                "gleichungen_err AS Gleichungen, "

                "textbeispiele_err AS Textbeispiele, "

                "raumvorstellung_err AS Raumvorstellung, "

                "grundrechnungsarten_err AS Grundrechnungsarten, "

                "zahlenraum_err AS Zahlenraum "

                "FROM testdaten "

                "WHERE teilnehmer_id = ? "

                "ORDER BY test_datum"

            )

            df = pd.read_sql_query(query, conn, params=(teilnehmer_id,))

            return df

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Testergebnisse: {e}")

        return pd.DataFrame()



# Funktion, um einen PDF-Bericht zu erstellen

def erstelle_pdf(teilnehmer_name, testergebnisse):

    pdf_path = os.path.join(BASE_DIR, f"{teilnehmer_name}_Bericht.pdf")

    try:

        c = canvas.Canvas(pdf_path)

        c.setFont("Helvetica", 12)

        c.drawString(100, 800, f"Bericht für Teilnehmer: {teilnehmer_name}")

        c.drawString(100, 780, "Testergebnisse:")

        

        y = 760

        for index, row in testergebnisse.iterrows():

            text = f"{row['Testdatum']} - Brüche: {row['Brüche']}%, Gleichungen: {row['Gleichungen']}%, "

            text += f"Textbeispiele: {row['Textbeispiele']}%, Raumvorstellung: {row['Raumvorstellung']}%, "

            text += f"Grundrechnungsarten: {row['Grundrechnungsarten']}%, Zahlenraum: {row['Zahlenraum']}%"

            c.drawString(100, y, text)

            y -= 20

            if y < 50:

                c.showPage()

                y = 800



        c.save()

        st.success(f"PDF-Bericht wurde erstellt: {pdf_path}")

    except Exception as e:

        st.error(f"Fehler beim Erstellen des PDF-Berichts: {e}")



# Streamlit-Funktion zur Berichterstellung

def berichte():

    st.title("Berichterstellung")

    st.markdown("Erstellen Sie einen PDF-Bericht für die Testergebnisse eines Teilnehmers.")



    try:

        # Teilnehmerdaten laden

        with sqlite3.connect(DB_PATH) as conn:

            teilnehmer_query = "SELECT id, name FROM teilnehmer"

            teilnehmer_df = pd.read_sql_query(teilnehmer_query, conn)



        if not teilnehmer_df.empty:

            teilnehmer_name = st.selectbox(

                "Wählen Sie einen Teilnehmer aus", 

                teilnehmer_df["name"].tolist()

            )

            if teilnehmer_name:

                teilnehmer_id = teilnehmer_df.loc[teilnehmer_df["name"] == teilnehmer_name, "id"].values[0]

                testergebnisse = lade_testergebnisse(teilnehmer_id)



                if not testergebnisse.empty:

                    st.dataframe(testergebnisse)

                    if st.button("PDF-Bericht erstellen"):

                        erstelle_pdf(teilnehmer_name, testergebnisse)

                else:

                    st.warning("Keine Testergebnisse für den ausgewählten Teilnehmer verfügbar.")

        else:

            st.warning("Keine Teilnehmerdaten verfügbar.")

    except sqlite3.Error as e:

        st.error(f"Fehler beim Laden der Teilnehmerdaten: {e}")



if __name__ == "__main__":

    berichte()

"""



# Save the corrected file

with open(reports_module_path, 'w') as file:

    file.write(optimized_reports_module)
