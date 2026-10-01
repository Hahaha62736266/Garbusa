from flask import Flask, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Register Dashboard Blueprint
from routes import dashboard
app.register_blueprint(dashboard.bp, url_prefix='/dashboard')

# Root → go straight to Dashboard
@app.route('/')
def home():
    return redirect(url_for('dashboard.main'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
