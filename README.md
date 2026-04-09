# Abid Medical Store - Pro Management Suite
**Your Health, Our Priority | Serving with Integrity**

A professional, desktop-based Pharmacy Management System developed for **Abid Medical Store**. This suite is designed to streamline complex medical billing, automate inventory searching across multi-source rate lists, and provide secure, data-driven business analytics.

---

## 📂 Project Architecture
This application follows a modular architecture to ensure scalability and ease of maintenance:

* **`main.py`**: The application's entry point, featuring a branded landing page with the store's official logo and custom professional slogans.
* **`bill_window.py`**: The core billing engine, implementing an intuitive side-by-side table layout to distinguish between Pharmacy and Disposable products.
* **`database.py`**: The SQLite backend manager, handling complex multi-list medicine search logic and protected sales analytics.
* **`requirements.txt`**: A comprehensive list of environment dependencies including `PySide6` and `reportlab`.
* **`.gitignore`**: A strict security configuration to ensure local databases and private patient records are never pushed to the public repository.

---

## 🚀 Key Features
* **Intelligent Multi-List Search**: Real-time "auto-pitch" functionality that fetches medicine rates from integrated master lists (supporting 131+ pages of data) instantly as you type.
* **Side-by-Side Billing**: Automatically categorizes items into separate columns for **Pharmacy** and **Disposable** items, ensuring professional invoice clarity for patients.
* **In-Bill Item Management**: Fully integrated controls to **Update** or **Delete** specific items within the billing window, allowing for error correction before finalization.
* **Secure Admin Analytics**: A password-protected "Admin Vault" that provides critical business insights, including total revenue and historical transaction counts.
* **Professional Branding**: A modern landing page focused on UX, featuring custom store branding and a clean medical software interface.

---

## 🛠️ Installation & Setup
1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Misbah-84/AbidMedicalStoreApp.git](https://github.com/Misbah-84/AbidMedicalStoreApp.git)
    cd AbidMedicalStoreApp
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Application**:
    ```bash
    python main.py
    ```

---

## 🔒 Data Security & Privacy
This repository is configured to exclude the local `medical_store.db` file. This is a critical security measure to ensure that while the source code is public, all private patient data and sensitive store financial records remain locally stored and encrypted.

## 🤝 Developed By
**Misbah Ullah**
