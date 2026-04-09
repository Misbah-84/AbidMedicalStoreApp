# In returning_patient_window.py (Add Update Bill button)

import sys
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt, QDate

import database
from bill_window import BillWindow # Import BillWindow

class ReturningPatientWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Returning Patient Hub")
        self.resize(800, 600)

        main_layout = QVBoxLayout()

        # Search Section
        search_layout = QHBoxLayout()
        self.search_label = QLabel("Search by Patient ID:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Patient ID")
        self.search_input.textChanged.connect(self.filter_bills)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Bills Table
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(6) # ID, Patient ID, Name, Admitted, Discharged, Total
        self.bills_table.setHorizontalHeaderLabels(["Bill ID", "Patient ID", "Patient Name", "Admission Date", "Discharge Date", "Total Amount"])
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bills_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bills_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        main_layout.addWidget(self.bills_table)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.update_bill_btn = QPushButton("Update Selected Bill")
        self.update_bill_btn.clicked.connect(self.open_update_bill_window)
        button_layout.addWidget(self.update_bill_btn)
        
        self.create_new_bill_btn = QPushButton("Create New Bill for This Patient")
        self.create_new_bill_btn.clicked.connect(self.create_new_bill_for_patient)
        button_layout.addWidget(self.create_new_bill_btn)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.close_btn)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_all_bills()

    def load_all_bills(self):
        self.all_bills = database.get_all_bills()
        self.populate_bills_table(self.all_bills)

    def populate_bills_table(self, bills):
        self.bills_table.setRowCount(0)
        for row, bill in enumerate(bills):
            self.bills_table.insertRow(row)
            self.bills_table.setItem(row, 0, QTableWidgetItem(str(bill["id"])))
            self.bills_table.setItem(row, 1, QTableWidgetItem(bill["patient_id"]))
            self.bills_table.setItem(row, 2, QTableWidgetItem(bill["patient_name"]))
            self.bills_table.setItem(row, 3, QTableWidgetItem(bill["admission_date"]))
            self.bills_table.setItem(row, 4, QTableWidgetItem(bill["discharge_date"]))
            self.bills_table.setItem(row, 5, QTableWidgetItem(f"{bill['total_amount']:.2f}"))

    def filter_bills(self):
        search_text = self.search_input.text().strip().lower()
        if not search_text:
            self.populate_bills_table(self.all_bills)
            return

        filtered_bills = [
            bill for bill in self.all_bills 
            if search_text in bill["patient_id"].lower() or 
               search_text in bill["patient_name"].lower()
        ]
        self.populate_bills_table(filtered_bills)

    def open_update_bill_window(self):
        selected_rows = self.bills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a bill to update.")
            return
        
        row_index = selected_rows[0].row()
        bill_id_item = self.bills_table.item(row_index, 0)
        if bill_id_item:
            bill_id = int(bill_id_item.text())
            bill_to_update = database.get_bill_by_id(bill_id)
            if bill_to_update:
                update_bill_win = BillWindow(existing_bill_data=bill_to_update)
                if update_bill_win.exec() == QDialog.DialogCode.Accepted:
                    self.load_all_bills() # Reload data after update
            else:
                QMessageBox.critical(self, "Error", "Selected bill not found in database.")

    def create_new_bill_for_patient(self):
        selected_rows = self.bills_table.selectionModel().selectedRows()
        patient_id = ""
        patient_name = ""
        admission_date = QDate.currentDate().toString("dd-MM-yyyy") # Default to current date

        if selected_rows:
            row_index = selected_rows[0].row()
            patient_id = self.bills_table.item(row_index, 1).text()
            patient_name = self.bills_table.item(row_index, 2).text()
            # If creating a *new* bill, we don't carry over the old admission_date directly, 
            # unless the intent is to create a new *admission* for the same patient.
            # For simplicity, we'll let the user fill a new admission date for a new bill.
            # However, we can pre-fill patient ID and name.
        
        # Open a new BillWindow with pre-filled patient info
        new_bill_win = BillWindow()
        new_bill_win.patient_id_input.setText(patient_id)
        new_bill_win.patient_name_input.setText(patient_name)
        new_bill_win.admission_date_input.setText(admission_date) # Can be changed by user
        
        if new_bill_win.exec() == QDialog.DialogCode.Accepted:
            self.load_all_bills() # Reload data after new bill created