from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =============================================
# 🏠 HOME PAGE
# =============================================
@app.route("/")
def home_page():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"""
        <html><body style="padding:2rem;font-family:sans-serif;">
            <h1>🌾 Garbusa — Farmer Support System</h1>
            <p style="color:green;">✅ Server is running!</p>
            <p>Template message: {e}</p>
            <h3>Endpoints:</h3>
            <ul>
                <li><a href="/test">/test</a> — Health check</li>
                <li>POST → <code>/submit-form</code> — Form test below</li>
            </ul>
            <hr>
            <h3>Test Form:</h3>
            <form action="/submit-form" method="POST">
                <p>Name: <input name="name" required></p>
                <p>Email: <input name="email" required></p>
                <p>Message:<br><textarea name="message" rows="3"></textarea></p>
                <button type="submit">Submit</button>
            </form>
        </body></html>
        """, 200

# =============================================
# ✅ TEST ENDPOINT
# =============================================
@app.route("/test")
def test():
    return jsonify({"status": "ok", "message": "Garbusa backend is live!"}), 200

# =============================================
# 📝 YOUR FORM SUBMIT FUNCTION
# =============================================
@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            return jsonify({"success": False, "message": "Name and email required"}), 400

        print(f"✅ Form submitted: {name} | {email} | {message}")

        return f"""
        <html><body style="padding:2rem;font-family:sans-serif;">
            <h2 style="color:green;">✅ Submitted Successfully!</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong> {message}</p>
            <a href="/">← Go Back</a>
        </body></html>
        """, 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# =============================================
# ✅ RUN
# =============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
