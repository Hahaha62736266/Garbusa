from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# App configuration
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Supabase Setup (if using it)
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected successfully")
except Exception as e:
    print(f"⚠️ Supabase connection skipped: {e}")

# Import and register routes
try:
    from routes import home, auth, products, farmers  # match YOUR actual files
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(farmers.bp)
    print("✅ Routes loaded successfully")
except Exception as e:
    print(f"⚠️ Some routes not loaded yet: {e}")

# Default homepage
@app.route('/')
def index():
    return "✅ Garbusa — Server is Running! Your routes are being restored."

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)
