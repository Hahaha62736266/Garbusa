from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your existing routes here...

def submit_form():
    """Handle form submission: validate, process, and return response"""
    if request.method == 'POST':
        # Get form data — adjust field names to match your HTML form
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()

            # Basic validation
            if not name or not email:
                return jsonify({
                    "success": False,
                    "message": "Name and email are required fields"
                }), 400

            # --- Add your processing logic here ---
            # Example: Save to database, send email, etc.
            print(f"Received submission from {name} ({email}): {message}")

            return jsonify({
                "success": True,
                "message": "Form submitted successfully!"
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

# Register the route
@app.route('/submit-form', methods=['POST'])
def form_submit_route():
    return submit_form()

if __name__ == '__main__':
    app.run(debug=True)
