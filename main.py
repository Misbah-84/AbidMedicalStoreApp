import sys, os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from bill_window import BillWindow
import database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        database.init_db()
        self.setWindowTitle("Abid Medical Store - Pro v5.0")
        self.resize(1100, 750)
        
        central = QWidget(); self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # --- Professional Sidebar ---
        sidebar = QFrame(); sidebar.setFixedWidth(250); sidebar.setStyleSheet("background: #1A5276; color: white;")
        side_lay = QVBoxLayout(sidebar)
        
        self.btn_new = self.nav_btn("➕ Create New Bill")
        self.btn_search = self.nav_btn("🔍 Search & Update")
        self.btn_admin = self.nav_btn("🔒 Sales Analytics")
        
        for b in [self.btn_new, self.btn_search, self.btn_admin]:
            side_lay.addWidget(b)
        side_lay.addStretch()
        layout.addWidget(sidebar)

        # --- Main Content Area ---
        self.stack = QStackedWidget()
        self.setup_home()
        self.setup_search_view()
        layout.addWidget(self.stack)

        # Button Logic
        self.btn_new.clicked.connect(lambda: BillWindow().exec())
        self.btn_search.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_admin.clicked.connect(self.admin_auth)

    def nav_btn(self, text):
        return QPushButton(text)

    def setup_home(self):
        """Main Branded Landing Page."""
        home = QWidget(); lay = QVBoxLayout(home); lay.setAlignment(Qt.AlignCenter)
        
        logo = QLabel(); logo.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.KeepAspectRatio))
        title = QLabel("ABID MEDICAL STORE")
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #1A5276;")
        
        slogan = QLabel("Care You Can Trust | Quality You Can Afford")
        slogan.setStyleSheet("font-size: 18px; color: #555; font-style: italic;")
        
        lay.addWidget(logo, alignment=Qt.AlignCenter)
        lay.addWidget(title, alignment=Qt.AlignCenter)
        lay.addWidget(slogan, alignment=Qt.AlignCenter)
        self.stack.addWidget(home)

    def setup_search_view(self):
        """Dedicated page for Searching, Updating, and Deleting old bills."""
        search = QWidget(); lay = QVBoxLayout(search)
        lay.addWidget(QLabel("<h1>Search Records</h1>"))
        self.search_bar = QLineEdit(); self.search_bar.setPlaceholderText("Type Name or ID...")
        self.search_table = QTableWidget(0, 4)
        self.search_table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Total"])
        self.search_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lay.addWidget(self.search_bar); lay.addWidget(self.search_table)
        self.stack.addWidget(search)

    def admin_auth(self):
        """Protected Sales Analytics logic."""
        pwd, ok = QInputDialog.getText(self, "Admin", "Access Pin:", QLineEdit.Password)
        if ok and pwd == "admin123":
            # FIX: Pulling from the restored database function
            rev, count = database.get_total_sales()
            QMessageBox.information(self, "Business Stats", f"Total Revenue: Rs. {rev:,.2f}\nTotal Bills: {count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())