import random
import datetime
from database import cursor, db
from models import Patient, VitalSigns

def simulate_vital_signs(patient):
    temperature = random.uniform(36.0, 39.0)
    blood_pressure = random.uniform(80.0, 120.0)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Delete the previous vital sign for this patient
    cursor.execute("DELETE FROM vital_signs WHERE patient_id = %s ORDER BY timestamp DESC LIMIT 1", (patient.id,))

    vital_sign = VitalSigns(patient, temperature, blood_pressure, timestamp)

    cursor.execute("INSERT INTO vital_signs (patient_id, temperature, blood_pressure, timestamp) VALUES (%s, %s, %s, %s)",
                   (patient.id, vital_sign.temperature, vital_sign.blood_pressure, vital_sign.timestamp))

    db.commit()

    if vital_sign.temperature > 38.5 or vital_sign.blood_pressure > 140:
        print(f"Alert: Abnormal vital signs for patient {patient.name}")
