import sqlite3

DB_PATH = "mira.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT    NOT NULL,
            dob         TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            glucose     REAL    NOT NULL,
            haemoglobin REAL    NOT NULL,
            cholesterol REAL    NOT NULL,
            remarks     TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = _conn()
    conn.execute(
        "INSERT INTO patients (full_name,dob,email,glucose,haemoglobin,cholesterol,remarks) VALUES (?,?,?,?,?,?,?)",
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    )
    conn.commit(); conn.close()

def get_all_patients():
    conn = _conn()
    rows = conn.execute("SELECT * FROM patients ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

def get_patient_by_id(pid):
    conn = _conn()
    row = conn.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    conn.close()
    return row

def update_patient(pid, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = _conn()
    conn.execute(
        "UPDATE patients SET full_name=?,dob=?,email=?,glucose=?,haemoglobin=?,cholesterol=?,remarks=? WHERE id=?",
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, pid)
    )
    conn.commit(); conn.close()

def delete_patient(pid):
    conn = _conn()
    conn.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit(); conn.close()
