from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from config import Config

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGIN}})

def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "AquaFlow Water Refilling System",
        "version": "1.0.0"
    })

@app.route("/api/stations", methods=["GET"])
def get_stations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stations ORDER BY name")
    stations = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(stations)

@app.route("/api/records", methods=["GET"])
def get_records():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, s.name as station_name 
        FROM refilling_records r
        JOIN stations s ON r.station_id = s.id
        ORDER BY r.recorded_at DESC
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@app.route("/api/records", methods=["POST"])
def add_record():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        INSERT INTO refilling_records 
        (station_id, volume_liters, customer_name, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["station_id"],
        data["volume_liters"],
        data.get("customer_name", ""),
        data["amount_paid"],
        data.get("payment_method", "cash")
    ))
    
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"id": new_id, "message": "Record added successfully"}), 201

@app.route("/api/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM refilling_records WHERE id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Record deleted"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
