# In search_window.py (Updated to display new item fields)

import sys
import os
import subprocess
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt

import database

class SearchWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search, View, and Delete Bills")
        self.resize(1000, 700)

        main_layout = QVBoxLayout()

        # Search Filters
        filter_layout = QHBoxLayout()
        self.search_label = QLabel("Search by Patient ID/Name:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Patient ID or Name")
        self.search_input.textChanged.connect(self.filter_bills)
        filter_layout.addWidget(self.search_label)
        filter_layout.addWidget(self.search_input)

        self.search_bill_id_label = QLabel("Search by Bill ID:")
        self.search_bill_id_input = QLineEdit()
        self.search_bill_id_input.setPlaceholderText("Enter Bill ID")
        self.search_bill_id_input.textChanged.connect(self.filter_bills)
        self.search_bill_id_input.setMaximumWidth(150)
        filter_layout.addWidget(self.search_bill_id_label)
        filter_layout.addWidget(self.search_bill_id_input)
        main_layout.addLayout(filter_layout)

        # All Bills Table (top)
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(6) # ID, Patient ID, Name, Admitted, Discharged, Total
        self.bills_table.setHorizontalHeaderLabels(["Bill ID", "Patient ID", "Patient Name", "Admission Date", "Discharge Date", "Total Amount"])
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bills_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bills_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.bills_table.itemSelectionChanged.connect(self.display_selected_bill_items)
        main_layout.addWidget(self.bills_table)
        
        # Selected Bill Items Table (bottom)
        self.items_label = QLabel("Items for Selected Bill:")
        main_layout.addWidget(self.items_label)
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7) # S.No, Date, Name, Qty, Rate, Amount, Type
        self.items_table.setHorizontalHeaderLabels(["S.No", "Date", "Item Name", "Quantity", "Rate", "Amount", "Type"])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.items_table)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.print_btn = QPushButton("Print Selected Bill")
        self.print_btn.clicked.connect(self.print_selected_bill)
        button_layout.addWidget(self.print_btn)
        
        self.delete_btn = QPushButton("Delete Selected Bill")
        self.delete_btn.clicked.connect(self.delete_selected_bill)
        button_layout.addWidget(self.delete_btn)
        
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
        patient_search_text = self.search_input.text().strip().lower()
        bill_id_search_text = self.search_bill_id_input.text().strip()

        filtered_bills = []
        for bill in self.all_bills:
            match_patient = (not patient_search_text or 
                             patient_search_text in bill["patient_id"].lower() or 
                             patient_search_text in bill["patient_name"].lower())
            match_bill_id = (not bill_id_search_text or 
                             bill_id_search_text == str(bill["id"]))
            
            if match_patient and match_bill_id:
                filtered_bills.append(bill)
        
        self.populate_bills_table(filtered_bills)
        self.items_table.setRowCount(0) # Clear items when bills table filters

    def display_selected_bill_items(self):
        selected_rows = self.bills_table.selectionModel().selectedRows()
        self.items_table.setRowCount(0) # Clear previous items

        if not selected_rows:
            return

        row_index = selected_rows[0].row()
        bill_id = int(self.bills_table.item(row_index, 0).text())
        bill_data = database.get_bill_by_id(bill_id)

        if bill_data and bill_data["items"]:
            self.items_table.setRowCount(len(bill_data["items"]))
            for row, item in enumerate(bill_data["items"]):
                self.items_table.setItem(row, 0, QTableWidgetItem(item.get("s_no", "")))
                self.items_table.setItem(row, 1, QTableWidgetItem(item.get("date", "")))
                self.items_table.setItem(row, 2, QTableWidgetItem(item.get("name", "")))
                self.items_table.setItem(row, 3, QTableWidgetItem(str(item.get("quantity", ""))))
                self.items_table.setItem(row, 4, QTableWidgetItem(f"{item.get('rate', 0):.2f}"))
                self.items_table.setItem(row, 5, QTableWidgetItem(f"{item.get('amount', 0):.2f}"))
                self.items_table.setItem(row, 6, QTableWidgetItem(item.get("type", "")))

    def print_selected_bill(self):
        selected_rows = self.bills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a bill to print.")
            return
        
        row_index = selected_rows[0].row()
        bill_id = int(self.bills_table.item(row_index, 0).text())
        bill_data = database.get_bill_by_id(bill_id)

        if bill_data:
            # Re-use the generate_pdf logic from BillWindow
            from bill_window import BillWindow # Import here to avoid circular dependency issues
            temp_bill_window = BillWindow() # Create a temporary instance
            temp_bill_window.generate_pdf(bill_id, bill_data)
        else:
            QMessageBox.critical(self, "Error", "Selected bill not found in database.")

    def delete_selected_bill(self):
        selected_rows = self.bills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a bill to delete.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this bill? This action cannot be undone.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            row_index = selected_rows[0].row()
            bill_id = int(self.bills_table.item(row_index, 0).text())
            database.delete_bill(bill_id)
            QMessageBox.information(self, "Success", f"Bill ID {bill_id} deleted successfully.")
            self.load_all_bills() # Reload bills after deletion
            self.items_table.setRowCount(0) # Clear items table