from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            diagnosis TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Pydantic model for request validation
class Patient(BaseModel):
    name: str
    age: int
    diagnosis: str

# API to receive data from `server.py`
@app.post("/add_patient")
def add_patient(patient: Patient):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, diagnosis) VALUES (?, ?, ?)", 
                   (patient.name, patient.age, patient.diagnosis))
    conn.commit()
    conn.close()
    return {"message": "Patient added successfully"}

# API to fetch all patients
@app.get("/patients")
def get_patients():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    conn.close()
    return {"patients": data}
