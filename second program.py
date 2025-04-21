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
            return False  # Default to False if there's an error
    
    def __repr__(self):
        return f"Patient(full_name={self.full_name}, severity_score={self.severity_score}, logical_expression={self.logical_expression})"

    def to_list(self):
        return [self.full_name, self.severity_score, self.logical_expression, self.age, self.height, self.gender, self.reason]
