from database import cursor, db
from models import Patient, ClinicalFile

def update_clinical_file(patient, diagnosis=None, treatment=None):
    cursor.execute("SELECT diagnoses, treatments FROM clinicalfiles WHERE patient_id = %s", (patient.id,))
    result = cursor.fetchone()

    if result:
        clinical_file = ClinicalFile(patient, result[0].split(';'), result[1].split(';'))
    else:
        clinical_file = ClinicalFile(patient)

    if diagnosis:
        clinical_file.diagnoses.append(diagnosis)
    if treatment:
        clinical_file.treatments.append(treatment)

    diagnoses_str = ';'.join(clinical_file.diagnoses)
    treatments_str = ';'.join(clinical_file.treatments)
    if result:
        cursor.execute("UPDATE clinicalfiles SET diagnoses = %s, treatments = %s WHERE patient_id = %s",
                       (diagnoses_str, treatments_str, patient.id))
    else:
        cursor.execute("INSERT INTO clinicalfiles (patient_id, diagnoses, treatments) VALUES (%s, %s, %s)",
                       (patient.id, diagnoses_str, treatments_str))
    db.commit()

    return clinical_file
