import streamlit as st
import sqlite3
from datetime import datetime

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Validierung der Sozialversicherungsnummer
def validate_sv_number(sv_number):
    if len(sv_number) != 10 or not sv_number.isdigit():
        return False, "Die Sozialversicherungsnummer muss genau 10 Ziffern enthalten (Format: XXXXDDMMYY)."
    return True, ""

# Validierung von Datumseingaben
def validate_date(input_date):
    try:
        datetime.strptime(input_date, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Das Datum muss im Format YYYY-MM-DD eingegeben werden."

# Validierung der Punktwerte
def validate_points(points, max_points):
    if not (0 <= points <= max_points):
        return False, f"Punkte ({points}) müssen zwischen 0 und {max_points} liegen."
    return True, ""

# Teilnehmerdaten sicher in die Datenbank einfügen
def insert_participant(name, sv_number, gender, start_date, end_date):
    is_valid_sv, sv_error = validate_sv_number(sv_number)
    if not is_valid_sv:
        return False, sv_error

    is_valid_start, start_error = validate_date(start_date)
    if not is_valid_start:
        return False, start_error

    is_valid_end, end_error = validate_date(end_date)
    if not is_valid_end:
        return False, end_error

    try:
        conn.execute(
            """
            INSERT INTO teilnehmer (name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, sv_number, gender, start_date, end_date)
        )
        conn.commit()
        return True, "Teilnehmer erfolgreich hinzugefügt."
    except Exception as e:
        return False, f"Datenbankfehler: {str(e)}"

# Hauptfunktion für die Validierung in Streamlit
def main():
    st.header("Teilnehmer hinzufügen mit Validierung")

    with st.form("new_participant_form"):
        name = st.text_input("Name")
        sv_number = st.text_input("Sozialversicherungsnummer (Format: XXXXDDMMYY)")
        gender = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
        start_date = st.text_input("Eintrittsdatum (YYYY-MM-DD)")
        end_date = st.text_input("Austrittsdatum (YYYY-MM-DD)")
        submit = st.form_submit_button("Hinzufügen")

        if submit:
            success, message = insert_participant(name, sv_number, gender, start_date, end_date)
            if success:
                st.success(message)
            else:
                st.error(message)

if __name__ == "__main__":
    main()
