import pandas as pd
import sqlite3
from flaml import AutoML

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('data/math_course_management.db')

# Historische Testdaten laden
def load_test_data():
    query = """
    SELECT 
        test_datum, brueche_erreichte_punkte, textaufgaben_erreichte_punkte, 
        raumvorstellung_erreichte_punkte, gleichungen_erreichte_punkte, 
        grundrechenarten_erreichte_punkte, zahlenraum_erreichte_punkte,
        gesamt_prozent
    FROM tests
    """
    return pd.read_sql(query, conn)

# FLAML-Modelle für jede Kategorie trainieren
def train_flaml(data):
    data['test_datum'] = pd.to_datetime(data['test_datum'])
    data['days_since_start'] = (data['test_datum'] - data['test_datum'].min()).dt.days
    features = data[['days_since_start']]
    targets = data[['brueche_erreichte_punkte', 'textaufgaben_erreichte_punkte',
                    'raumvorstellung_erreichte_punkte', 'gleichungen_erreichte_punkte',
                    'grundrechenarten_erreichte_punkte', 'zahlenraum_erreichte_punkte']]
    
    models = {}
    for category in targets.columns:
        automl = AutoML()
        automl.fit(X_train=features, y_train=targets[category], task="regression")
        models[category] = automl
    return models

# Prognosen für zukünftige Werte erstellen
def predict_future(models, days_ahead=30):
    future_days = pd.DataFrame({'days_since_start': range(1, days_ahead + 1)})
    predictions = {}
    for category, model in models.items():
        predictions[category] = model.predict(future_days)
    predictions['days_since_start'] = future_days['days_since_start']
    return pd.DataFrame(predictions)

# Prognosen in die Datenbank speichern
def save_predictions(predictions, participant_id):
    for _, row in predictions.iterrows():
        conn.execute(
            """
            INSERT INTO prognosen (
                teilnehmer_id, prognose_datum, prognose_brueche, prognose_textaufgaben,
                prognose_raumvorstellung, prognose_gleichungen, prognose_grundrechenarten, 
                prognose_zahlenraum, prognose_gesamt
            )
            VALUES (?, DATE('now', ? || ' days'), ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                participant_id, int(row['days_since_start']),
                row.get('brueche_erreichte_punkte', 0), row.get('textaufgaben_erreichte_punkte', 0),
                row.get('raumvorstellung_erreichte_punkte', 0), row.get('gleichungen_erreichte_punkte', 0),
                row.get('grundrechenarten_erreichte_punkte', 0), row.get('zahlenraum_erreichte_punkte', 0),
                row.mean()
            )
        )
    conn.commit()

# Hauptfunktion für FLAML-Prozesse
def main():
    data = load_test_data()
    if data.empty:
        print("Keine Testdaten verfügbar für das Training.")
        return
    models = train_flaml(data)
    future_predictions = predict_future(models)
    save_predictions(future_predictions, participant_id=1)  # Beispiel-ID
    print("Prognosen erfolgreich erstellt und gespeichert.")

if __name__ == "__main__":
    main()
  
