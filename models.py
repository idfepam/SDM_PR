class Patient:
    def __init__(self, name, age, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.clinical_file = None

class ClinicalFile:
    def __init__(self, patient, diagnoses=None, treatments=None):
        self.patient = patient
        self.diagnoses = diagnoses or []
        self.treatments = treatments or []

class VitalSigns:
    def __init__(self, patient, temperature, blood_pressure, timestamp):
        self.patient = patient
        self.temperature = temperature
        self.blood_pressure = blood_pressure
        self.timestamp = timestamp

class Bed:
    def __init__(self, room_number, bed_number, patient=None, sensor_data=None):
        self.room_number = room_number
        self.bed_number = bed_number
        self.patient = patient
        self.sensor_data = sensor_data or []