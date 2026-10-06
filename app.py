from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_expense():
    # Handle incoming form data to save a new expense
    category = request.form.get('category')
    amount = float(request.form.get('amount'))

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (category, amount) VALUES (?, ?)', (category, amount))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Expense recorded!"})

@app.route('/data')
def get_data():
    # Query database and sum up total spending per category for Chart.js
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = cursor.fetchall()
    conn.close()

    # Format into key-value structure for JavaScript
    categories = [row[0] for row in rows]
    amounts = [row[1] for row in rows]

    return jsonify({"categories": categories, "amounts": amounts})

if __name__ == '__main__':
    app.run(debug=True)