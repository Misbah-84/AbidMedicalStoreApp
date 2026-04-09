import sqlite3

# This connects to our database file. It will be created if it doesn't exist.
conn = sqlite3.connect('medical_store.db')

# This object lets us execute commands on the database.
cursor = conn.cursor()

# --- Create the 'bills' table ---
# This table stores the main information for each bill.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY,
        patient_id TEXT,
        admission_date TEXT,
        discharge_date TEXT,
        total_amount REAL,
        bill_date TEXT
    )
''')

# --- Create the 'bill_items' table ---
# This table stores every single medicine item for each bill.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bill_items (
        item_id INTEGER PRIMARY KEY,
        bill_id INTEGER,
        medicine_name TEXT,
        quantity INTEGER,
        rate REAL,
        amount REAL,
        FOREIGN KEY (bill_id) REFERENCES bills (bill_id)
    )
''')

# Save the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Database 'medical_store.db' and its tables have been created successfully!")