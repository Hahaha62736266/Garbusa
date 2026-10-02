from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key_here'  # Replace with your own

# Database configuration (XAMPP default)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'garbusa_db',
    'user': 'root',
    'password': '',  # Leave blank for XAMPP default
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM farmers")
        farmers = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', farmers=farmers)
    return "Database connection failed"

@app.route('/add', methods=['GET', 'POST'])
def add_farmer():
    if request.method == 'POST':
        name = request.form['name']
        crop = request.form['crop']
        contact = request.form['contact']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO farmers (name, crop, contact) VALUES (%s, %s, %s)",
                (name, crop, contact)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Farmer added successfully!")
            return redirect(url_for('home'))
        flash("Connection error")
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
