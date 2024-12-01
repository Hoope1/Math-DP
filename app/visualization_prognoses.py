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
            query = """
            SELECT 
                prognose_datum AS Datum, 
                prognose_brueche AS Brüche, 
                prognose_textaufgaben AS Textaufgaben, 
                prognose_raumvorstellung AS Raumvorstellung, 
                prognose_gleichungen AS Gleichungen, 
                prognose_grundrechenarten AS Grundrechenarten, 
                prognose_zahlenraum AS Zahlenraum, 
                prognose_gesamt AS Gesamt
            FROM prognosen
            """
            prognosen = pd.read_sql(query, conn)
            return prognosen
    except sqlite3.Error as e:
        st.error(f"Fehler beim Laden der Prognosedaten: {e}")
        return pd.DataFrame()

# Hauptfunktion für die Prognose-Visualisierung
def main():
    st.header("Prognose-Visualisierung")

    # Prognosedaten laden
    prognosen = lade_prognosedaten()
    if prognosen.empty:
        st.warning("Keine Prognosedaten verfügbar.")
        return

    # Benutzer wählt, welche Kategorie visualisiert werden soll
    kategorie = st.selectbox(
        "Wähle eine Kategorie für die Prognosevisualisierung",
        ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum", "Gesamt"]
    )

    # Liniendiagramm für die ausgewählte Kategorie
    fig = px.line(
        prognosen,
        x="Datum",
        y=kategorie,
        title=f"Prognoseverlauf für {kategorie}",
        labels={"Datum": "Datum", kategorie: "Prozent"},
        markers=True
    )
    fig.update_layout(
        xaxis_title="Datum",
        yaxis_title="Prognose (%)",
        template="simple_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Alle Kategorien in einem Diagramm anzeigen
    if st.checkbox("Alle Kategorien anzeigen"):
        fig_all = px.line(
            prognosen.melt(id_vars=["Datum"], var_name="Kategorie", value_name="Prozent"),
            x="Datum",
            y="Prozent",
            color="Kategorie",
            title="Prognosen für alle Kategorien",
            labels={"Datum": "Datum", "Prozent": "Prognose (%)"},
            markers=True
        )
        fig_all.update_layout(
            xaxis_title="Datum",
            yaxis_title="Prognose (%)",
            template="simple_white"
        )
        st.plotly_chart(fig_all, use_container_width=True)

    # AutoML-Modelltraining und Prognose
    st.subheader("Prognosen mit AutoML")
    if st.button("Trainiere AutoML-Modell"):
        daten = lade_daten_fuer_automl()
        automl_model = durchfuehren_automl(daten)
        if automl_model:
            st.success("Das AutoML-Modell wurde erfolgreich trainiert!")
            
            # Neue Daten für Prognose simulieren
            neue_daten = daten.drop(columns=["Gesamtprozent"]).head(1)  # Beispiel: Erste Zeile für Prognose
            prognosen = erstelle_prognose(automl_model, neue_daten)
            if prognosen is not None:
                st.write("Erstellte Prognosen:")
                st.write(prognosen)
            else:
                st.error("Fehler bei der Erstellung der Prognosen.")

if __name__ == "__main__":
    main()
