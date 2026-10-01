from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# =============================================
# 📊 DASHBOARD HOME PAGE — Aqua Flow Branding
# =============================================
@app.route("/")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Aqua Flow Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }
        body { background: #f0f9f9; padding: 2rem; max-width: 1200px; margin: 0 auto; }
        .logo { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; padding-bottom: 1rem; border-bottom: 2px solid #c6e6e6; }
        .logo-icon { font-size: 2.2rem; filter: drop-shadow(0 2px 4px rgba(14,124,123,0.25)); }
        .logo-text { font-size: 1.8rem; color: #0e7c7b; font-weight: 700; letter-spacing: -0.5px; }
        .status { background: #e6f7f7; color: #0e7c7b; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid #0e7c7b; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 6px rgba(14,124,123,0.08); }
        .card h3 { color: #0e7c7b; margin-bottom: 1rem; }
        form { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 6px rgba(14,124,123,0.08); }
        label { display: block; margin: 1rem 0 0.3rem; font-weight: 500; color: #0a5f5e; }
        input, textarea { width: 100%; padding: 0.75rem; border: 1px solid #b2d8d8; border-radius: 6px; background: #fcfefe; }
        button { margin-top: 1.2rem; padding: 0.75rem 2rem; background: #0e7c7b; color: white; border: none; border-radius: 6px; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0b6362; }
        a { color: #0e7c7b; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; }
        h2 { color: #0e7c7b; margin: 2rem 0 1rem; }
    </style>
</head>
<body>
    <div class="logo">
        <span class="logo-icon">💧</span>
        <span class="logo-text">Aqua Flow</span>
    </div>

    <div class="status">✅ System Online — Welcome to Aqua Flow</div>

    <div class="grid">
        <div class="card">
            <h3>📈 System Status</h3>
            <p><strong>Status:</strong> Online</p>
            <p><strong>Environment:</strong> GitHub Codespaces</p>
            <p><strong>Version:</strong> 1.0.0</p>
        </div>
        <div class="card">
            <h3>📋 Quick Links</h3>
            <p><a href="/test">System Health Check</a></p>
            <p><a href="/api/customers">Customer API</a></p>
        </div>
        <div class="card">
            <h3>🔧 Actions</h3>
            <p>Submit the form below to test your endpoint.</p>
        </div>
    </div>

    <h2>📝 Contact / Form Test</h2>
    <form action="/submit-form" method="POST">
        <label for="name">Name *</label>
        <input type="text" id="name" name="name" required>

        <label for="email">Email *</label>
        <input type="email" id="email" name="email" required>

        <label for="message">Message / Concern</label>
        <textarea id="message" name="message" rows="4"></textarea>

        <button type="submit">Submit Form</button>
    </form>
</body>
</html>
    """)

# =============================================
# ✅ TEST ENDPOINT
# =============================================
@app.route("/test")
def test():
    return jsonify({
        "status": "online",
        "app": "Aqua Flow",
        "message": "Flask server is responding correctly"
    }), 200

# =============================================
# 📝 FORM SUBMISSION FUNCTION
# =============================================
@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            return jsonify({
                "success": False,
                "message": "Name and email are required fields"
            }), 400

        print(f"📩 FORM SUBMITTED → Name: {name}, Email: {email}")

        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Submission Successful — Aqua Flow</title>
    <style>
        body { font-family: system-ui; padding: 2rem; max-width: 600px; margin: 0 auto; background: #f0f9f9; }
        .box { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(14,124,123,0.1); }
        h2 { color: #0e7c7b; }
        .btn { display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #0e7c7b; color: white; text-decoration: none; border-radius: 6px; }
        .btn:hover { background: #0b6362; }
    </style>
</head>
<body>
    <div class="box">
        <h2>✅ Submission Received!</h2>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Message:</strong> {{ message }}</p>
        <a href="/" class="btn">← Back to Aqua Flow</a>
    </div>
</body>
</html>
        """, name=name, email=email, message=message), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# =============================================
# 🧾 API PLACEHOLDERS
# =============================================
@app.route("/api/customers", methods=["GET"])
def api_customers():
    return jsonify({
        "status": 200,
        "data": [],
        "note": "Controller integration pending",
        "app": "Aqua Flow"
    }), 200

# =============================================
# 🚀 START SERVER
# =============================================
if __name__ == "__main__":
    print("=" * 50)
    print("💧 Aqua Flow Server Starting...")
    print("📍 Dashboard: http://0.0.0.0:5000")
    print("📝 Form endpoint: /submit-form")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
