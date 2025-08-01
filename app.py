from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv
from openpyxl import Workbook
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
            amount REAL,
            payment_method TEXT,
            reference_id TEXT,
            vendor_customer TEXT,
            invoice_no TEXT,
            status TEXT,
            entered_by TEXT,
            attachment TEXT
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
    data = request.form
    file = request.files.get('attachment')
    attachment_path = ''
    if file and file.filename:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(attachment_path)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (
            date, description, category, type, amount, payment_method, reference_id,
            vendor_customer, invoice_no, status, entered_by, attachment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['date'], data['description'], data['category'], data['type'], float(data['amount']),
        data['payment_method'], data['reference_id'], data['vendor_customer'], data['invoice_no'],
        data['status'], data['entered_by'], attachment_path
    ))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/export/csv')
def export_csv():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    rows = c.fetchall()
    headers = [i[0] for i in c.description]
    conn.close()
    filename = "transactions.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return send_file(filename, as_attachment=True)

@app.route('/export/excel')
def export_excel():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    rows = c.fetchall()
    headers = [i[0] for i in c.description]
    conn.close()

    filename = "transactions.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws.append(headers)
    for row in rows:
        ws.append(row)
    wb.save(filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)