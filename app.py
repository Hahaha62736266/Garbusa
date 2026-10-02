from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Auth helpers
def get_current_user():
    if "user" in session:
        return session["user"]
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session["user"] = res.user
            flash("Login successful!")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Login failed: {str(e)}")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            flash("Account created! Check your email to verify.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Registration failed: {str(e)}")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('home'))

# Farmer CRUD
@app.route('/')
def home():
    try:
        res = supabase.table("garbusa_farmers").select("*").order("created_at", desc=True).execute()
        farmers = res.data
        
        # Calculate dashboard stats
        crop_set = set(f['crop'] for f in farmers if f.get('crop'))
        crops_count = len(crop_set)
        
        from datetime import datetime, timedelta
        one_month_ago = datetime.now() - timedelta(days=30)
        recent_count = sum(
            1 for f in farmers 
            if f.get('created_at') and f['created_at'] > one_month_ago.isoformat()
        )
        
        return render_template('index.html', 
            farmers=farmers, 
            user=get_current_user(),
            crops_count=crops_count,
            recent_count=recent_count
        )
    except Exception as e:
        flash(f"Error loading data: {str(e)}", "error")
        return render_template('index.html', farmers=[], user=get_current_user(), crops_count=0, recent_count=0)

@app.route('/add', methods=['GET', 'POST'])
def add_farmer():
    user = get_current_user()
    if not user:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        crop = request.form['crop']
        contact = request.form['contact']
        location = request.form.get('location', '')
        
        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            ext = file.filename.rsplit('.', 1)[-1].lower()
            fn = f"{uuid.uuid4()}.{ext}"
            supabase.storage.from_("farmer_images").upload(
                path=fn,
                file=file.read(),
                file_options={"content-type": file.mimetype}
            )
            image_url = f"{SUPABASE_URL}/storage/v1/object/public/farmer_images/{fn}"

        try:
            supabase.table("garbusa_farmers").insert({
                "user_id": user['id'],
                "name": name,
                "crop": crop,
                "contact": contact,
                "location": location,
                "image_url": image_url
            }).execute()
            flash("Farmer added successfully!")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Save failed: {str(e)}")
    return render_template('form.html', action='add', user=user)

@app.route('/edit/<int:farmer_id>', methods=['GET', 'POST'])
def edit_farmer(farmer_id):
    user = get_current_user()
    if not user:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "crop": request.form['crop'],
            "contact": request.form['contact'],
            "location": request.form.get('location', '')
        }
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            ext = file.filename.rsplit('.', 1)[-1].lower()
            fn = f"{uuid.uuid4()}.{ext}"
            supabase.storage.from_("farmer_images").upload(fn, file.read(), {"content-type": file.mimetype})
            data["image_url"] = f"{SUPABASE_URL}/storage/v1/object/public/farmer_images/{fn}"
        
        try:
            supabase.table("garbusa_farmers").update(data).eq("id", farmer_id).eq("user_id", user['id']).execute()
            flash("Updated successfully!")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Update failed: {str(e)}")
    
    res = supabase.table("garbusa_farmers").select("*").eq("id", farmer_id).execute()
    if not res.data:
        flash("Record not found.")
        return redirect(url_for('home'))
    return render_template('form.html', action='edit', farmer=res.data[0], user=user)

@app.route('/delete/<int:farmer_id>', methods=['POST'])
def delete_farmer(farmer_id):
    user = get_current_user()
    if not user:
        flash("Please log in first.")
        return redirect(url_for('login'))
    try:
        supabase.table("garbusa_farmers").delete().eq("id", farmer_id).eq("user_id", user['id']).execute()
        flash("Deleted.")
    except Exception as e:
        flash(f"Delete failed: {str(e)}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
