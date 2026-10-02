from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change_this_to_secure_key")

# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    try:
        res = supabase.table("garbusa_farmers").select("*").order("id", desc=True).execute()
        farmers = res.data
        return render_template('index.html', farmers=farmers)
    except Exception as e:
        flash(f"Error loading data: {str(e)}")
        return render_template('index.html', farmers=[])

@app.route('/add', methods=['GET', 'POST'])
def add_farmer():
    if request.method == 'POST':
        name = request.form['name']
        crop = request.form['crop']
        contact = request.form['contact']
        
        try:
            supabase.table("garbusa_farmers").insert({
                "name": name,
                "crop": crop,
                "contact": contact
            }).execute()
            flash("Farmer added successfully!")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Save failed: {str(e)}")
    return render_template('add.html')

@app.route('/delete/<int:farmer_id>', methods=['POST'])
def delete_farmer(farmer_id):
    try:
        supabase.table("garbusa_farmers").delete().eq("id", farmer_id).execute()
        flash("Deleted successfully!")
    except Exception as e:
        flash(f"Delete failed: {str(e)}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
