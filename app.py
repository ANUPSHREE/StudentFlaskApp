from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM students")

    if cursor.fetchone()[0] == 0:
        students = [
            (1, "Ananya", "CSE", 85),
            (2, "Rahul", "ECE", 78),
            (3, "Priya", "CSE", 92),
            (4, "Arjun", "IT", 81),
            (5, "Sneha", "EEE", 88)
        ]

        cursor.executemany(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            students
        )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    students = connection.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()
    connection.close()

    return render_template("index.html", students=students)


create_database()

if __name__ == "__main__":
    app.run(debug=True)
