from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv
from openpyxl import Workbook
import os

app = Flask(__name__)

DB_FILE = 'books.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            date TEXT,
            description TEXT,
            category TEXT,
            type TEXT CHECK(type IN ('income','expense')),
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', transactions=rows)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    description = request.form['description']
    category = request.form['category']
    ttype = request.form['type']
    amount = float(request.form['amount'])
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO transactions (date, description, category, type, amount) VALUES (?, ?, ?, ?, ?)',
              (date, description, category, ttype, amount))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/export/csv')
def export_csv():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    rows = c.fetchall()
    conn.close()
    filename = "transactions.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Description", "Category", "Type", "Amount"])
        writer.writerows(rows)
    return send_file(filename, as_attachment=True)

@app.route('/export/excel')
def export_excel():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    rows = c.fetchall()
    conn.close()
    filename = "transactions.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws.append(["ID", "Date", "Description", "Category", "Type", "Amount"])
    for row in rows:
        ws.append(row)
    wb.save(filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port or 5000 locally
    app.run(host='0.0.0.0', port=port)
