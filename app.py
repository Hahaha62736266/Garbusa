from flask import Flask, redirect, url_for
import os
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "<h1 style='padding:2rem; color:#2e7d32;'>🚧 Dashboard coming soon — connected successfully!</h1>"

if __name__ == '__main__':
    app.run(debug=True)

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
