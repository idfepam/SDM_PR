import mysql.connector
# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hospital_db"
)

cursor = db.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        clinicalfile_id INT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinicalfiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        diagnoses TEXT,
        treatments TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vital_signs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        temperature FLOAT,
        blood_pressure FLOAT,
        timestamp DATETIME,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds (
        id INT AUTO_INCREMENT PRIMARY KEY,
        room_number INT,
        bed_number INT,
        patient_id INT,
        sensor_data TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
""")

# Commit the changes and close the connection
db.commit()
