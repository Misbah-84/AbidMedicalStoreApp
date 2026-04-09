# In patient_hub_window.py (UPDATED)

import sqlite3
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTableWidget, 
                               QPushButton, QHBoxLayout, QHeaderView, 
                               QTableWidgetItem, QMessageBox)
from bill_window import BillWindow

class PatientHubWindow(QDialog):
    def __init__(self, patient_id):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = "" # Variable to store patient name
        
        # --- First, get patient's name ---
        self.get_patient_name()
        
        self.setWindowTitle(f"Options for {self.patient_name} ({self.patient_id})")
        self.resize(700, 400)
        layout = QVBoxLayout()
        
        self.info_label = QLabel(f"Showing all bills for {self.patient_name} (I,D: {self.patient_id})")
        
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(4)
        self.bills_table.setHorizontalHeaderLabels(["Bill ID", "Bill Date", "Admission Date", "Total Amount"])
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bills_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        button_layout = QHBoxLayout()
        self.edit_bill_button = QPushButton("Edit Selected Bill")
        self.create_new_bill_button = QPushButton("Create New Bill for This Patient")
        button_layout.addWidget(self.edit_bill_button)
        button_layout.addWidget(self.create_new_bill_button)
        layout.addWidget(self.info_label)
        layout.addWidget(self.bills_table)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.create_new_bill_button.clicked.connect(self.create_new_bill)
        self.edit_bill_button.clicked.connect(self.edit_selected_bill)
        self.load_bills()
        
    def get_patient_name(self):
        # Function to get the most recent name for this patient ID
        conn = sqlite3.connect('medical_store.db')
        cursor = conn.cursor()
        query = "SELECT patient_name FROM bills WHERE patient_id = ? ORDER BY bill_id DESC LIMIT 1"
        cursor.execute(query, (self.patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.patient_name = result[0]

    def load_bills(self):
        # This function is unchanged
        conn = sqlite3.connect('medical_store.db')
        cursor = conn.cursor()
        query = "SELECT bill_id, bill_date, admission_date, total_amount FROM bills WHERE patient_id = ?"
        cursor.execute(query, (self.patient_id,))
        bills = cursor.fetchall()
        conn.close()
        self.bills_table.setRowCount(0)
        for row_data in bills:
            row_position = self.bills_table.rowCount()
            self.bills_table.insertRow(row_position)
            for col_num, data in enumerate(row_data):
                self.bills_table.setItem(row_position, col_num, QTableWidgetItem(str(data)))

    def create_new_bill(self):
        # This function is unchanged
        self.accept()
        self.bill_win = BillWindow(patient_id=self.patient_id)
        self.bill_win.exec()

    def edit_selected_bill(self):
        # This function is unchanged
        selected_row = self.bills_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a bill from the table to edit.")
            return
        bill_id_to_edit = self.bills_table.item(selected_row, 0).text()
        self.accept()
        self.bill_win = BillWindow(bill_id_to_edit=int(bill_id_to_edit))
        self.bill_win.exec()