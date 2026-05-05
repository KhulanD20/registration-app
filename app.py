from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import re
from datetime import datetime

app = Flask(__name__)
DATABASE = "register.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
last_name TEXT,
first_name TEXT,
phone TEXT,
email TEXT,
created_at TEXT
)
""")
    conn.commit()
    conn.close()

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route("/", methods=["GET", "POST"])
def register():
    message = ""
    error = ""

    if request.method == "POST":
        last_name = request.form["last_name"]
        first_name = request.form["first_name"]
        phone = request.form["phone"]
        email = request.form["email"]

        if not valid_email(email):
            error = "Имэйл буруу байна"
        else:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("""
INSERT INTO registrations (last_name, first_name, phone, email, created_at)
VALUES (?, ?, ?, ?, ?)
""", (last_name, first_name, phone, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            message = "Амжилттай бүртгэгдлээ"

    
return render_template("templates/register.html", message=message, error=error)

@app.route("/download")
def download():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query("SELECT * FROM registrations", conn)
    conn.close()

    file = "data.xlsx"
    df.to_excel(file, index=False)

    return send_file(file, as_attachment=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
