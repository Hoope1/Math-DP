import streamlit as st
import pandas as pd
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Prozentwerte berechnen
def calculate_percentages(points, max_points):
    if max_points > 0:
        return round((points / max_points) * 100, 2)
    return 0

# Tests in die Datenbank einfügen
def insert_test(participant_id, test_date, points_categories, max_points_categories):
    total_points = sum(points_categories.values())
    total_max_points = sum(max_points_categories.values())
    total_percent = calculate_percentages(total_points, total_max_points)

    conn.execute(
        """
        INSERT INTO tests (
            teilnehmer_id, test_datum, brueche_erreichte_punkte, brueche_max_punkte,
            textaufgaben_erreichte_punkte, textaufgaben_max_punkte, 
            raumvorstellung_erreichte_punkte, raumvorstellung_max_punkte,
            gleichungen_erreichte_punkte, gleichungen_max_punkte,
            grundrechenarten_erreichte_punkte, grundrechenarten_max_punkte,
            zahlenraum_erreichte_punkte, zahlenraum_max_punkte,
            gesamt_erreichte_punkte, gesamt_max_punkte, gesamt_prozent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            participant_id, test_date,
            points_categories["Brüche"], max_points_categories["Brüche"],
            points_categories["Textaufgaben"], max_points_categories["Textaufgaben"],
            points_categories["Raumvorstellung"], max_points_categories["Raumvorstellung"],
            points_categories["Gleichungen"], max_points_categories["Gleichungen"],
            points_categories["Grundrechenarten"], max_points_categories["Grundrechenarten"],
            points_categories["Zahlenraum"], max_points_categories["Zahlenraum"],
            total_points, total_max_points, total_percent
        )
    )
    conn.commit()

# Hauptfunktion für die Testeingabe
def main():
    st.header("Testdaten eingeben")

    # Teilnehmerdaten laden
    participants = pd.read_sql("SELECT teilnehmer_id, name FROM teilnehmer", conn)
    if participants.empty:
        st.warning("Keine Teilnehmer vorhanden. Bitte zuerst Teilnehmer hinzufügen.")
        return

    # Teilnehmerauswahl
    participant_name = st.selectbox("Wähle einen Teilnehmer", participants["name"].tolist())
    selected_participant = participants[participants["name"] == participant_name].iloc[0]

    # Formular für Testdaten
    with st.form("test_input_form"):
        st.subheader(f"Testdaten für {participant_name} eingeben")
        test_date = st.date_input("Testdatum")
        points_categories = {}
        max_points_categories = {}

        # Kategorien
        categories = ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]
        for category in categories:
            points_categories[category] = st.number_input(f"Erreichte Punkte in {category}", min_value=0, max_value=100)
            max_points_categories[category] = st.number_input(f"Maximale Punkte in {category}", min_value=0, max_value=100)
        
        submit_test = st.form_submit_button("Speichern")
        
        if submit_test:
            insert_test(
                selected_participant["teilnehmer_id"], str(test_date),
                points_categories, max_points_categories
            )
            st.success(f"Testdaten für {participant_name} wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    main()
