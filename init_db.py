import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ---------------- USERS ----------------
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT,
    profile_pic TEXT,
    course TEXT,
    year TEXT,
    reg_no TEXT
)
""")

# ---------------- LOST ITEMS ----------------
cur.execute("""
CREATE TABLE lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_name TEXT,
    description TEXT,
    location TEXT,
    image TEXT
)
""")

# ---------------- FOUND ITEMS ----------------
cur.execute("""
CREATE TABLE found_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_name TEXT,
    description TEXT,
    location TEXT,
    image TEXT
)
""")

# ---------------- CLAIMS ----------------
cur.execute("""
CREATE TABLE claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    claimer_id INTEGER,
    message TEXT,
    status TEXT DEFAULT 'pending'
)
""")

# ---------------- VOUCHERS ----------------
cur.execute("""
CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    voucher_name TEXT,
    voucher_value INTEGER
)
""")

# ---------------- SETTINGS ----------------
cur.execute("""
CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    voucher_name TEXT,
    voucher_value INTEGER
)
""")

cur.execute("""
INSERT INTO users (name, email, password, role)
VALUES ('Admin', 'admin@gmail.com', 'admin123', 'admin')
""")

# default setting
cur.execute("INSERT INTO settings VALUES (1, 'Amazon Gift Card', 100)")

conn.commit()
conn.close()

print("✅ Database created successfully!")