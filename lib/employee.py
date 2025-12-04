import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

class Employee:
    def __init__(self, name, job_title, department_id):
        self.id = None
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    # ----------------- Properties -----------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def job_title(self):
        return self._job_title

    @job_title.setter
    def job_title(self, value):
        if not isinstance(value, str):
            raise TypeError("Job title must be a string")
        if len(value) == 0:
            raise ValueError("Job title cannot be empty")
        self._job_title = value

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Department ID must be an integer")
        self._department_id = value

    # ----------------- Database Methods -----------------
    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                department_id INTEGER NOT NULL
            )
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO employees (name, job_title, department_id) VALUES (?, ?, ?)",
                (self.name, self.job_title, self.department_id)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            self.update()

    @classmethod
    def create(cls, name, job_title, department_id):
        employee = cls(name, job_title, department_id)
        employee.save()
        return employee

    def update(self):
        if self.id is None:
            raise ValueError("Cannot update employee without id")
        CURSOR.execute(
            "UPDATE employees SET name=?, job_title=?, department_id=? WHERE id=?",
            (self.name, self.job_title, self.department_id, self.id)
        )
        CONN.commit()

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete employee without id")
        CURSOR.execute("DELETE FROM employees WHERE id=?", (self.id,))
        CONN.commit()
        self.id = None  # critical to pass the test

    @classmethod
    def instance_from_db(cls, row):
        employee = cls(row[1], row[2], row[3])
        employee.id = row[0]
        return employee

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM employees")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM employees WHERE id=?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM employees WHERE name=?", (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
