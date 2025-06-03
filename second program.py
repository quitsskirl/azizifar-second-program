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

class Hospital:
    def __init__(self, name):
        self.name = name
        self.patient_list = []

    def add_patient(self, patient):
        self.patient_list.append(patient)

    def clear_patients(self):
        self.patient_list.clear()

    def get_all_patients(self):
        return self.patient_list

    def remove_patient_by_name(self, name):
        self.patient_list = [p for p in self.patient_list if p.full_name != name]

class Admin:
    def __init__(self, username):
        self.username = username

    def authenticate(self, input_username, input_password):
        return input_username == self.username and input_password == VALID_PASSWORD

hospital = Hospital("General Hospital")
admin = Admin("admin")

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

def search_patient(name):
    for patient in hospital.get_all_patients():
        if patient.full_name.lower() == name.lower():
            return patient
    return None

def analyze_performance():
    copy_data = copy.deepcopy(hospital.get_all_patients())

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
        hospital.add_patient(Patient(name, severity, expr, age, height, gender, reason))
    show_patients()

def show_patients(silent=False):
    for row in treeview.get_children():
        treeview.delete(row)
    if not hospital.get_all_patients():
        if not silent:
            messagebox.showinfo("No Patients", "No patients to show.")
    else:
        for patient in hospital.get_all_patients():
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
    if len(logical_expression) > 60 or logical_expression.strip().isdigit():
        messagebox.showerror("Invalid Input", "Logical expression invalid.")
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
            raise ValueError("Must be boolean")
    except Exception as e:
        messagebox.showerror("Invalid Input", f"Logical expression error: {e}")
        return

    try:
        age = int(age_entry.get())
        height = int(height_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Age and Height must be integers.")
        return

    gender = gender_entry.get().upper()
    if gender not in ['M', 'F']:
        messagebox.showerror("Invalid Input", "Gender must be 'M' or 'F'")
        return

    reason = reason_entry.get()
    new_patient = Patient(full_name, severity_score, logical_expression, age, height, gender, reason)
    hospital.add_patient(new_patient)

    full_name_entry.delete(0, tk.END)
    severity_score_entry.delete(0, tk.END)
    logical_expression_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    reason_entry.delete(0, tk.END)
    messagebox.showinfo("Patient Added", f"Patient {full_name} added successfully.")

def save_patients():
    try:
        with open("patients_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Full Name", "Severity Score", "Logical Expression", "Age", "Height", "Gender", "Reason"])
            for patient in hospital.get_all_patients():
                writer.writerow(patient.to_list())
        messagebox.showinfo("Saved", "Patient data saved to 'patients_data.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"Save error: {e}")

def load_patients():
    if os.path.exists("patients_data.csv"):
        try:
            with open("patients_data.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) == 7:
                        patient = Patient(row[0], float(row[1]), row[2], int(row[3]), int(row[4]), row[5], row[6])
                        hospital.add_patient(patient)
            show_patients(silent=True)
        except Exception as e:
            messagebox.showerror("Error", f"Load error: {e}")

def delete_patient():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("No Selection", "Select a patient to delete.")
        return
    selected_name = treeview.item(selected_item)["values"][0]
    hospital.remove_patient_by_name(selected_name)
    treeview.delete(selected_item)
    save_patients()
    messagebox.showinfo("Deleted", f"Patient {selected_name} deleted.")

def delete_all_patients():
    if messagebox.askyesno("Confirm", "Delete ALL patients?"):
        hospital.clear_patients()
        treeview.delete(*treeview.get_children())
        with open("patients_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Full Name", "Severity Score", "Logical Expression", "Age", "Height", "Gender", "Reason"])
        messagebox.showinfo("Deleted", "All patients deleted.")

def upload_csv():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                patient = Patient(row["Full Name"], float(row["Severity Score"]), row["Logical Expression"], int(row["Age"]), int(row["Height"]), row["Gender"], row["Reason"])
                hospital.add_patient(patient)
            show_patients()
        except Exception as e:
            messagebox.showerror("Error", f"CSV load error: {e}")

def search_patient_ui():
    name = search_entry.get()
    patient = search_patient(name)
    if patient:
        messagebox.showinfo("Found", f"Found: {patient.full_name}, Severity: {patient.severity_score}")
        for row in treeview.get_children():
            if treeview.item(row)["values"][0].lower() == name.lower():
                treeview.selection_set(row)
                treeview.focus(row)
                treeview.see(row)
                break
    else:
        messagebox.showinfo("Not Found", "Patient not found.")

def open_login():
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x180")
    login_window.grab_set()

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10)

    def check_login():
        if admin.authenticate(username_entry.get(), password_entry.get()):
            login_window.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Button(login_window, text="Login", command=check_login).grid(row=2, column=0, columnspan=2, pady=15)

VALID_PASSWORD = "1234"

root = tk.Tk()
root.withdraw()
open_login()

root.title("Hospital Patient Management")
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

entries = {}
labels = ["Full Name", "Severity Score (1-10)", "Logical Expression", "Age", "Height (in cm)", "Gender (M/F)", "Reason for Visit"]
for i, label in enumerate(labels):
    tk.Label(input_frame, text=label + ":").grid(row=i, column=0, pady=5, padx=5)
    entry = tk.Entry(input_frame)
    entry.grid(row=i, column=1, pady=5, padx=5)
    entries[label] = entry

full_name_entry = entries["Full Name"]
severity_score_entry = entries["Severity Score (1-10)"]
logical_expression_entry = entries["Logical Expression"]
age_entry = entries["Age"]
height_entry = entries["Height (in cm)"]
gender_entry = entries["Gender (M/F)"]
reason_entry = entries["Reason for Visit"]

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

buttons = [
    ("Add Patient", add_patient),
    ("Show Patients", show_patients),
    ("Save Patients", save_patients),
    ("Delete Patient", delete_patient),
    ("Delete All Patients", delete_all_patients),
    ("Upload CSV", upload_csv),
    ("Analyze Performance", analyze_performance),
    ("Generate 10 Patients", lambda: generate_dummy_patients(10))
]

for idx, (text, cmd) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=cmd).grid(row=idx // 4, column=idx % 4, padx=10, pady=5)

search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root, text="Search by Name", command=search_patient_ui).pack(pady=5)

treeview_frame = tk.Frame(root)
treeview_frame.pack(pady=20)

treeview = ttk.Treeview(treeview_frame, columns=("Full Name", "Severity", "Age", "Height", "Gender", "Reason"), show="headings")
treeview.pack()

for col in ("Full Name", "Severity", "Age", "Height", "Gender", "Reason"):
    treeview.heading(col, text=col)
    treeview.column(col, width=120)

load_patients()
root.mainloop()