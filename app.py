from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Routes — Dashboard
from routes import dashboard
app.register_blueprint(dashboard.bp)

@app.route('/')
def home():
    return """
    ✅ Garbusa Server Running!<br>
    Go to <a href='/dashboard'>/dashboard</a> → Acquaflow Tracking
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
