import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv
import os
import time
import pandas as pd
from abc import ABC, abstractmethod
import copy
import random

# Abstract class for inheritance and OOP principles
class Person(ABC):
    def __init__(self, full_name, age, height, gender):
        self.full_name = full_name
        self.age = age
        self.height = height
        self.gender = gender

    @abstractmethod
    def to_list(self):
        pass

class Patient(Person):
    def __init__(self, full_name, severity_score, logical_expression, age, height, gender, reason):
        super().__init__(full_name, age, height, gender)
        self.severity_score = severity_score
        self.logical_expression = logical_expression
        self.reason = reason

    def evaluate_logical_expression(self):
        self.logical_expression = self.logical_expression.replace('true', 'True').replace('false', 'False')
        try:
            return eval(self.logical_expression)
        except Exception as e:
            print(f"Error evaluating logical expression: {e}")
            return False

    def __repr__(self):
        return f"Patient(full_name={self.full_name}, severity_score={self.severity_score}, logical_expression={self.logical_expression})"

    def to_list(self):
        return [self.full_name, self.severity_score, self.logical_expression, self.age, self.height, self.gender, self.reason]

patients = []

# Sorting algorithms

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j].severity_score > key.severity_score:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0].severity_score < right[0].severity_score:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

# Search algorithm

def search_patient(name):
    for patient in patients:
        if patient.full_name.lower() == name.lower():
            return patient
    return None

# Performance analysis

def analyze_performance():
    copy_data = copy.deepcopy(patients)

    start = time.perf_counter()
    insertion_sort(copy_data[:])
    insertion_time = time.perf_counter() - start

    start = time.perf_counter()
    merge_sort(copy_data[:])
    merge_time = time.perf_counter() - start

    messagebox.showinfo("Performance Analysis", f"Insertion Sort Time: {insertion_time:.5f}s\nMerge Sort Time: {merge_time:.5f}s")

def generate_dummy_patients(n):
    for i in range(n):
        name = f"TestPatient{i}"
        severity = random.uniform(1, 10)
        expr = random.choice(["True", "False", "True and False", "not False"])
        age = random.randint(1, 100)
        height = random.randint(100, 200)
        gender = random.choice(["M", "F"])
        reason = "Testing"
        patients.append(Patient(name, severity, expr, age, height, gender, reason))
    show_patients()

def show_patients(silent=False):
    for row in treeview.get_children():
        treeview.delete(row)

    if not patients:
        if not silent:
            messagebox.showinfo("No Patients", "No patients to show.")
    else:
        for patient in patients:
            treeview.insert('', 'end', values=(patient.full_name, patient.severity_score, patient.age, patient.height, patient.gender, patient.reason))


def add_patient():
    if not full_name_entry.get() or not severity_score_entry.get() or not logical_expression_entry.get() or not age_entry.get() or not height_entry.get() or not gender_entry.get() or not reason_entry.get():
        messagebox.showerror("Input Error", "All fields must be filled!")
        return

    full_name = full_name_entry.get()

    if len(full_name) > 60:
        messagebox.showerror("Invalid Input", "Full Name must not be more than 60 characters.")
        return

    try:
        severity_score = float(severity_score_entry.get())
        if not (1 <= severity_score <= 10):
            messagebox.showerror("Invalid Input", "Severity score must be between 1 and 10.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Severity score must be a number.")
        return

    logical_expression = logical_expression_entry.get()
    if len(logical_expression) > 60:
        messagebox.showerror("Invalid Input", "Logical expression must not be more than 60 characters.")
        return

    if logical_expression.strip().isdigit():
        messagebox.showerror("Invalid Input", "Logical expression must not be a pure integer.")
        return

    allowed_keywords = {"True", "False", "and", "or", "not", "(", ")"}
    tokens = logical_expression.replace('(', ' ( ').replace(')', ' ) ').split()
    for token in tokens:
        if not (token in allowed_keywords or token.isalpha()):
            messagebox.showerror("Invalid Input", f"Invalid token in logical expression: '{token}'")
            return

    try:
        evaluated_result = eval(logical_expression.replace('true', 'True').replace('false', 'False'))
        if not isinstance(evaluated_result, bool):
            raise ValueError("Logical expression must evaluate to a boolean result.")
    except Exception as e:
        messagebox.showerror("Invalid Input", f"Logical expression error: {e}")
        return

    try:
        age = int(age_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be an integer.")
        return

    try:
        height = int(height_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Height must be an integer.")
        return

    gender = gender_entry.get().upper()
    if gender not in ['M', 'F']:
        messagebox.showerror("Invalid Input", "Gender must be 'M' or 'F' (capital letters only).")
        return

    reason = reason_entry.get()

    new_patient = Patient(full_name, severity_score, logical_expression, age, height, gender, reason)
    patients.append(new_patient)

    full_name_entry.delete(0, tk.END)
    severity_score_entry.delete(0, tk.END)
    logical_expression_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    reason_entry.delete(0, tk.END)

    messagebox.showinfo("Patient Added", f"Patient {full_name} has been added successfully.")

def save_patients():
    try:
        with open("patients_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Full Name", "Severity Score", "Logical Expression", "Age", "Height", "Gender", "Reason"])
            for patient in patients:
                writer.writerow(patient.to_list())
        messagebox.showinfo("Data Saved", "Patient data has been successfully saved to 'patients_data.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving data: {e}")

def load_patients():
    if os.path.exists("patients_data.csv"):
        try:
            with open("patients_data.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) == 7:
                        full_name, severity_score, logical_expression, age, height, gender, reason = row
                        patient = Patient(full_name, float(severity_score), logical_expression, int(age), int(height), gender, reason)
                        patients.append(patient)
            show_patients(silent=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading data: {e}")

def delete_patient():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("No Selection", "Please select a patient to delete.")
        return

    selected_patient_name = treeview.item(selected_item)["values"][0]
    patient_to_delete = None
    for patient in patients:
        if patient.full_name == selected_patient_name:
            patient_to_delete = patient
            break

    if patient_to_delete:
        patients.remove(patient_to_delete)
        treeview.delete(selected_item)
        save_patients()
        messagebox.showinfo("Patient Deleted", f"Patient {selected_patient_name} has been deleted successfully.")
    else:
        messagebox.showerror("Error", "Patient not found.")
def delete_all_patients():
    confirm = messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete ALL patients?")
    if confirm:
        patients.clear()
        treeview.delete(*treeview.get_children())
        try:
            with open("patients_data.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Full Name", "Severity Score", "Logical Expression", "Age", "Height", "Gender", "Reason"])
            messagebox.showinfo("Deleted", "All patient records have been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear patient file: {e}")

def upload_csv():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                patient = Patient(row["Full Name"], float(row["Severity Score"]), row["Logical Expression"], int(row["Age"]), int(row["Height"]), row["Gender"], row["Reason"])
                patients.append(patient)
            show_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load CSV: {e}")

def search_patient_ui():
    name = search_entry.get()
    patient = search_patient(name)
    if patient:
        messagebox.showinfo("Found", f"Patient found: {patient.full_name}, Severity: {patient.severity_score}")
        for row in treeview.get_children():
            if treeview.item(row)["values"][0].lower() == name.lower():
                treeview.selection_set(row)
                treeview.focus(row)
                treeview.see(row)
                break
    else:
        messagebox.showinfo("Not Found", "Patient not found.")

root = tk.Tk()
root.title("Hospital Patient Management")

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

tk.Label(input_frame, text="Full Name:").grid(row=0, column=0, pady=5, padx=5)
full_name_entry = tk.Entry(input_frame)
full_name_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Severity Score (1-10):").grid(row=1, column=0, pady=5, padx=5)
severity_score_entry = tk.Entry(input_frame)
severity_score_entry.grid(row=1, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Logical Expression (e.g., 'True and False'):").grid(row=2, column=0, pady=5, padx=5)
logical_expression_entry = tk.Entry(input_frame)
logical_expression_entry.grid(row=2, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Age:").grid(row=3, column=0, pady=5, padx=5)
age_entry = tk.Entry(input_frame)
age_entry.grid(row=3, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Height (in cm):").grid(row=4, column=0, pady=5, padx=5)
height_entry = tk.Entry(input_frame)
height_entry.grid(row=4, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Gender (M/F):").grid(row=5, column=0, pady=5, padx=5)
gender_entry = tk.Entry(input_frame)
gender_entry.grid(row=5, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Reason for Visit:").grid(row=6, column=0, pady=5, padx=5)
reason_entry = tk.Entry(input_frame)
reason_entry.grid(row=6, column=1, pady=5, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Patient", command=add_patient).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Show Patients", command=show_patients).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Save Patients", command=save_patients).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Delete Patient", command=delete_patient).grid(row=0, column=3, padx=10)
tk.Button(button_frame, text="Delete All Patients", command=delete_all_patients).grid(row=1, column=0, columnspan=2, pady=10)
tk.Button(button_frame, text="Upload CSV", command=upload_csv).grid(row=0, column=4, padx=10)
tk.Button(button_frame, text="Analyze Performance", command=analyze_performance).grid(row=0, column=5, padx=10)
tk.Button(button_frame, text="Generate 10 Patients", command=lambda: generate_dummy_patients(10)).grid(row=0, column=6, padx=10)

search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root, text="Search by Name", command=search_patient_ui).pack(pady=5)

treeview_frame = tk.Frame(root)
treeview_frame.pack(pady=20)

treeview = ttk.Treeview(treeview_frame, columns=("Full Name", "Severity", "Age", "Height", "Gender", "Reason"), show="headings")
treeview.pack()

treeview.heading("Full Name", text="Full Name")
treeview.heading("Severity", text="Severity")
treeview.heading("Age", text="Age")
treeview.heading("Height", text="Height")
treeview.heading("Gender", text="Gender")
treeview.heading("Reason", text="Reason")

treeview.column("Full Name", width=150)
treeview.column("Severity", width=80)
treeview.column("Age", width=60)
treeview.column("Height", width=100)
treeview.column("Gender", width=60)
treeview.column("Reason", width=150)

load_patients()
root.mainloop()
