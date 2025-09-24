from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'employees.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data['name']
    role = data['role']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, role) VALUES (?, ?)", (name, role))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee added successfully!"}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

