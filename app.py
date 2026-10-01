from flask import Flask, render_template

app = Flask(__name__)

# Landing Page
@app.route('/')
def home():
    return render_template('index.html')

# Full Dashboard Page
@app.route('/dashboard')
def dashboard():
    # Sample farmer data — replace with real DB queries later
    farmers = [
        {"id": "F001", "name": "Maria Santos", "location": "Cagayan de Oro", "crop": "Rice", "status": "Active"},
        {"id": "F002", "name": "Juan Dela Cruz", "location": "Misamis Oriental", "crop": "Corn", "status": "Active"},
        {"id": "F003", "name": "Elena Reyes", "location": "Villanueva", "crop": "Vegetables", "status": "Pending"},
        {"id": "F004", "name": "Pedro Lim", "location": "Tagoloan", "crop": "Coconut", "status": "Active"},
        {"id": "F005", "name": "Ana Garcia", "location": "Opol", "crop": "Banana", "status": "Inactive"},
    ]
    
    # Statistics
    stats = {
        "total_farmers": 248,
        "active": 215,
        "crops_listed": 38,
        "market_connected": 189
    }
    
    return render_template('dashboard.html', farmers=farmers, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
