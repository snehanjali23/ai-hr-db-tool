import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("hr.db")
cursor = conn.cursor()

# Drop table if already exists
cursor.execute("DROP TABLE IF EXISTS employees")

# Create the employees table
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    designation TEXT,
    salary INTEGER,
    location TEXT,
    hire_date TEXT
)
""")

# Insert sample data with UNIQUE IDs
employees = [
    (1, "Alice Johnson", "HR", "HR Manager", 75000, "New York", "2018-03-12"),
    (2, "Bob Smith", "HR", "HR Executive", 60000, "New York", "2019-07-23"),
    (3, "Carla James", "HR", "HR Analyst", 58000, "Los Angeles", "2020-01-15"),
    (4, "David Lee", "HR", "HR Coordinator", 55000, "Chicago", "2021-05-10"),
    (5, "Eva Brown", "HR", "HR Specialist", 72000, "Miami", "2017-10-01"),
    (6, "Frank Wright", "HR", "HR Generalist", 68000, "Austin", "2016-08-22"),
    (7, "Grace ", "HR", "HR Director", 90000, "Boston", "2015-06-05"),
    (8, "Henry Miller", "HR", "HR Consultant", 77000, "Denver", "2020-11-30"),
    (9, "Isla Davis", "HR", "Recruiter", 61000, "San Diego", "2022-02-17"),
    (10, "Jack Wilson", "HR", "Compensation Analyst", 88000, "Seattle", "2019-09-14")
]

# Insert data
cursor.executemany("""
INSERT INTO employees (id, name, department, designation, salary, location, hire_date)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", employees)

# Commit and close
conn.commit()
conn.close()

print("✅ HR database created with 10 employees.")
