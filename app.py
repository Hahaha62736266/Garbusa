from flask import Flask, render_template

app = Flask(__name__)

# THIS IS THE HOME PAGE ROUTE — "Cannot GET /" means this was missing!
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/customers")
def customers():
    return render_template("customers/list.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
