from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
import database

class BillWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Billing - Abid Medical Store")
        self.resize(1200, 800)
        
        layout = QVBoxLayout(self)

        # --- Patient Header (Restored Discharge Date) ---
        pat_box = QGroupBox("Patient Data")
        grid = QGridLayout(pat_box)
        self.pat_id = QLineEdit(); self.pat_name = QLineEdit()
        self.adm_date = QLineEdit(QDate.currentDate().toString("dd-MM-yyyy"))
        self.dis_date = QLineEdit(); self.dis_date.setPlaceholderText("DD-MM-YYYY (Discharge)")
        grid.addWidget(QLabel("ID:"), 0, 0); grid.addWidget(self.pat_id, 0, 1)
        grid.addWidget(QLabel("Name:"), 0, 2); grid.addWidget(self.pat_name, 0, 3)
        grid.addWidget(QLabel("Adm Date:"), 1, 0); grid.addWidget(self.adm_date, 1, 1)
        grid.addWidget(QLabel("Dis Date:"), 1, 2); grid.addWidget(self.dis_date, 1, 3)
        layout.addWidget(pat_box)

        # --- Smart Entry Row (Search Across All Lists) ---
        entry_lay = QHBoxLayout()
        self.name_in = QLineEdit(); self.name_in.setPlaceholderText("Search Medicine...")
        self.completer = QCompleter(database.get_all_medicine_names())
        self.name_in.setCompleter(self.completer)
        self.name_in.editingFinished.connect(self.auto_pitch)
        
        self.qty_in = QLineEdit(); self.rate_in = QLineEdit()
        self.type_sel = QComboBox(); self.type_sel.addItems(["Medicine", "Disposable"])
        self.add_btn = QPushButton("Add to Bill")
        self.add_btn.setStyleSheet("background: #28a745; color: white; padding: 10px;")
        self.add_btn.clicked.connect(self.add_item)

        entry_lay.addWidget(self.name_in); entry_lay.addWidget(self.qty_in)
        entry_lay.addWidget(self.rate_in); entry_lay.addWidget(self.type_sel); entry_lay.addWidget(self.add_btn)
        layout.addLayout(entry_lay)

        # --- Side-by-Side Columns ---
        tables_lay = QHBoxLayout()
        self.med_table = self.create_table("Pharmacy Items")
        self.disp_table = self.create_table("Disposable Items")
        tables_lay.addWidget(self.med_table); tables_lay.addWidget(self.disp_table)
        layout.addLayout(tables_lay)

        # --- Row Controls (Update/Delete Current Items) ---
        ctrl_lay = QHBoxLayout()
        self.btn_rem = QPushButton("Remove Selected Item")
        self.btn_rem.clicked.connect(self.remove_item)
        ctrl_lay.addWidget(self.btn_rem); ctrl_lay.addStretch()
        layout.addLayout(ctrl_lay)

        # --- Footer ---
        self.total_lab = QLabel("Grand Total: Rs. 0.00")
        self.total_lab.setStyleSheet("font-size: 20px; font-weight: bold; color: #1A5276;")
        layout.addWidget(self.total_lab, alignment=Qt.AlignRight)

        self.print_btn = QPushButton("🖨️ Save & Print Official Bill")
        self.print_btn.setStyleSheet("background: #1A5276; color: white; height: 45px;")
        layout.addWidget(self.print_btn)

    def create_table(self, title):
        t = QTableWidget(0, 4)
        t.setHorizontalHeaderLabels(["Name", "Qty", "Rate", "Total"])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return t

    def auto_pitch(self):
        p = database.get_medicine_price(self.name_in.text())
        if p: self.rate_in.setText(f"{p:.2f}")

    def add_item(self):
        try:
            name, qty, rate = self.name_in.text(), float(self.qty_in.text()), float(self.rate_in.text())
            table = self.med_table if self.type_sel.currentText() == "Medicine" else self.disp_table
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(str(qty)))
            table.setItem(row, 2, QTableWidgetItem(f"{rate:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"{qty*rate:.2f}"))
            self.update_total()
        except: pass

    def remove_item(self):
        for t in [self.med_table, self.disp_table]:
            if t.currentRow() >= 0:
                t.removeRow(t.currentRow())
        self.update_total()

    def update_total(self):
        grand = 0.0
        for t in [self.med_table, self.disp_table]:
            for r in range(t.rowCount()):
                grand += float(t.item(r, 3).text())
        self.total_lab.setText(f"Grand Total: Rs. {grand:,.2f}")