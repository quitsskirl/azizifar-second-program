import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

class Patient:
    def __init__(self, full_name, severity_score, logical_expression, age, height, gender, reason):
        self.full_name = full_name
        self.severity_score = severity_score
        self.logical_expression = logical_expression
        self.age = age
        self.height = height
        self.gender = gender
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
    
    
def show_patients():
   
    for row in treeview.get_children():
        treeview.delete(row)
    
    if not patients:
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
            
            show_patients()  
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

add_patient_button = tk.Button(button_frame, text="Add Patient", command=add_patient)
add_patient_button.grid(row=0, column=0, padx=10)

show_button = tk.Button(button_frame, text="Show Patients", command=show_patients)
show_button.grid(row=0, column=1, padx=10)

save_button = tk.Button(button_frame, text="Save Patients", command=save_patients)
save_button.grid(row=0, column=2, padx=10)

delete_button = tk.Button(button_frame, text="Delete Patient", command=delete_patient)
delete_button.grid(row=0, column=3, padx=10)

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




