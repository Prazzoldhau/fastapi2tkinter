import tkinter as tk
from tkinter import ttk
import requests

# FastAPI endpoint
# API_URL = "http://127.0.0.1:8000"
API_URL = "https://fastapi2tkinter-1.onrender.com"


# Function to send data to FastAPI
def send_data():
    name = name_entry.get()
    age = age_entry.get()
    diagnosis = diagnosis_entry.get()

    if name and age and diagnosis:
        data = {
            "name": name,
            "age": int(age),
            "diagnosis": diagnosis
        }
        try:
            response = requests.post(f"{API_URL}/add_patient", json=data)
            if response.status_code == 200:
                result_label.config(text="Patient added successfully!")
                fetch_data()  # Refresh the table after adding
            else:
                result_label.config(text="Error adding patient.")
        except Exception as e:
            result_label.config(text=f"Error: {e}")
    else:
        result_label.config(text="Please fill all fields.")

# Function to fetch data from FastAPI and update the Treeview
def fetch_data():
    try:
        response = requests.get(f"{API_URL}/patients")
        if response.status_code == 200:
            data = response.json()["patients"]
            update_treeview(data)
        else:
            result_label.config(text="Error fetching data.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Function to update the Treeview with fetched data
def update_treeview(data):
    for row in tree.get_children():
        tree.delete(row)

    for row in data:
        tree.insert("", "end", values=row)

# Tkinter window setup
root = tk.Tk()
root.title("Patient Database")

# Entry fields for patient details
name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

age_label = tk.Label(root, text="Age:")
age_label.grid(row=1, column=0, padx=5, pady=5)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=5, pady=5)

diagnosis_label = tk.Label(root, text="Diagnosis:")
diagnosis_label.grid(row=2, column=0, padx=5, pady=5)
diagnosis_entry = tk.Entry(root)
diagnosis_entry.grid(row=2, column=1, padx=5, pady=5)

# Button to send data to FastAPI
submit_button = tk.Button(root, text="Add Patient", command=send_data)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Label to show result
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Treeview to display patient data
columns = ("ID", "Name", "Age", "Diagnosis")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Define headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Fetch data button
fetch_button = tk.Button(root, text="Fetch Patients", command=fetch_data)
fetch_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

# Run the Tkinter app
root.mainloop()
