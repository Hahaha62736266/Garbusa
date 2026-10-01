from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Server running — go to /dashboard"

@app.route('/dashboard')
def dashboard():
    return "<h1>Garbusa Dashboard</h1><p>Acquaflow Tracking is active!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
