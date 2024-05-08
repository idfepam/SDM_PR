from datetime import time
import random
import threading
from flask import Flask, redirect, request, jsonify, render_template, url_for
import monitoring
import clinical_files
from models import Patient
from database import cursor, db

app = Flask(__name__)

def add_patient_to_db(name, age):
    cursor.execute("INSERT INTO patients (name, age) VALUES (%s, %s)", (name, age))
    db.commit()
    return Patient(name, age, id=cursor.lastrowid)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.get_json()
    patient = add_patient_to_db(data['name'], data['age'])
    return jsonify({'id': patient.id, 'name': patient.name, 'age': patient.age}), 201

@app.route('/update_clinical_file', methods=['POST'])
def update_file():
    data = request.get_json()
    patient = Patient(id=data['patient_id'])
    clinical_file = clinical_files.update_clinical_file(patient, data.get('diagnosis'), data.get('treatment'))
    return jsonify({'diagnoses': clinical_file.diagnoses, 'treatments': clinical_file.treatments}), 200

@app.route('/simulate_vitals', methods=['POST'])
def simulate_vitals():
    data = request.get_json()
    patient = Patient(id=data['patient_id'])
    monitoring.simulate_vital_signs(patient)
    return jsonify({'message': 'Vital signs simulated'}), 200

@app.route('/patients')
def list_patients():
    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    return render_template('patients_list.html', patients=patients)


@app.route('/clinical_file', methods=['GET'])
def clinical_file():
    patient_id = request.args.get('patient_id')
    
    print(f"Accessing clinical file for patient ID: {patient_id}")
    cursor.execute("SELECT * FROM patients WHERE id = %s", [patient_id])
    patient = cursor.fetchone()

    cursor.execute("SELECT * FROM clinicalfiles WHERE patient_id = %s", [patient_id])
    clinical_data = cursor.fetchone()

    cursor.execute("SELECT temperature, blood_pressure FROM vital_signs WHERE patient_id = %s ORDER BY timestamp DESC LIMIT 1", [patient_id])
    last_vitals = cursor.fetchone()

    return render_template('clinical_file.html', patient=patient, clinical_data=clinical_data, last_vitals=last_vitals)

@app.route('/update_patient_form', methods=['POST'])
def update_patient_form():
    patient_id = request.form.get('patient_id')

    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    cursor.execute("SELECT * FROM clinicalfiles WHERE patient_id = %s", (patient_id,))
    clinical_data = cursor.fetchone()

    if patient and clinical_data:
        return render_template('update_patient.html', patient=patient, clinical_data=clinical_data)
    else:
        return "Patient not found", 404
    
@app.route('/update_patient', methods=['POST'])
def update_patient():
    # Process the form submission to update the patient data
    patient_id = request.form.get('patient_id')
    updated_name = request.form.get('name')
    updated_age = request.form.get('age')
    updated_doctor = request.form.get('doctor')
    updated_diagnosis = request.form.get('diagnosis')
    updated_treatment = request.form.get('treatment')

    cursor.execute("""
        UPDATE patients SET name = %s, age = %s, doctor = %s WHERE id = %s;
    """, (updated_name, updated_age, updated_doctor, patient_id))

    cursor.execute("""
        UPDATE clinicalfiles SET diagnoses = %s, treatments = %s WHERE patient_id = %s;
    """, (updated_diagnosis, updated_treatment, patient_id))

    db.commit()

    return redirect(url_for('confirm_update'))

@app.route('/confirm_update')
def confirm_update():
    # Display the confirmation page
    return render_template('confirm.html')

def update_vital_signs():
    while True:
        cursor.execute("SELECT id, name FROM patients")
        patients = cursor.fetchall()

        for patient in patients:
            patient_id = patient[0]
            patient_name = patient[1]
            monitoring.simulate_vital_signs(Patient(id=patient_id, name=patient_name))
        time.sleep(60)  # Wait for 1 minute (60 seconds)


if __name__ == '__main__':
    update_thread = threading.Thread(target=update_vital_signs)
    update_thread.start()
    app.run(debug=True)
