from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Supabase
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected")
except Exception as e:
    print(f"⚠️ Supabase: {e}")

# === ROUTES — Dashboard included ===
try:
    from routes import home, dashboard  # ← Dashboard connected!
    app.register_blueprint(home.bp)
    app.register_blueprint(dashboard.bp)
    print("✅ Dashboard & all routes loaded")
except Exception as e:
    print(f"⚠️ Route loading: {e}")

@app.route('/')
def index():
    return """
    ✅ Garbusa Server is Running!<br>
    Go to <a href='/dashboard'>/dashboard</a> to view your Dashboard
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5000)
