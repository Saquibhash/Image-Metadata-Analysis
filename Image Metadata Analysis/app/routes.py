from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Image
from app.utils import extract_metadata
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password using pbkdf2:sha256
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):  # Check hashed password
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Login failed. Check email and password", "danger")
    return render_template("login.html", form=form)

# User Dashboard (Upload & View Metadata)
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    filter_query = request.args.get('filter', '')
    sort_by = request.args.get('sort', 'timestamp')

    # Filtering logic
    query = Image.query.filter_by(user_id=current_user.id)
    if filter_query:
        query = query.filter(Image.image_metadata.like(f'%{filter_query}%'))

    # Sorting logic
    if sort_by == 'timestamp':
        query = query.order_by(Image.timestamp.desc())
    elif sort_by == 'format':
        query = query.order_by(Image.image_metadata['Format'].asc())  # Adjust field name accordingly
    elif sort_by == 'megapixels':
        query = query.order_by(Image.image_metadata['Megapixels'].asc())  # Adjust field name accordingly

    images = query.all()

    # Parse image metadata JSON into a Python dictionary before rendering
    for image in images:
        image.image_metadata = json.loads(image.image_metadata)  # Convert JSON string to dict

    return render_template("dashboard.html", images=images)

# Image Upload
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        flash("No file selected!", "danger")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected!", "danger")
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Extract image metadata
        image_metadata = extract_metadata(filepath)

        # Create new image entry
        new_image = Image(filename=filename, image_metadata=image_metadata, user_id=current_user.id)
        db.session.add(new_image)
        db.session.commit()

        flash("Image uploaded successfully!", "success")
        return redirect(url_for("dashboard"))

@app.route("/edit_metadata/<int:image_id>", methods=["GET", "POST"])
@login_required
def edit_metadata(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard"))

    # Parse image metadata into dictionary
    image.image_metadata = json.loads(image.image_metadata)  # Convert JSON string to dictionary

    if request.method == "POST":
        # Handle metadata editing and save back to database
        updated_metadata = {
            "Description": request.form.get("description", ""),
            "Keywords": request.form.get("keywords", ""),
            # Add other fields to be edited here...
        }

        # Update image metadata
        image.image_metadata = json.dumps(updated_metadata)  # Convert back to JSON string
        db.session.commit()

        flash("Metadata updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_metadata.html", image=image)

# Download Metadata JSON
@app.route("/download_metadata/<int:image_id>")
@login_required
def download_metadata(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard"))

    # Create a temporary folder to store the metadata file
    temp_folder = os.path.join(app.config["UPLOAD_FOLDER"], "temp_metadata")
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    metadata = json.loads(image.image_metadata)
    filename = f"{image.filename}_metadata.json"
    metadata_file_path = os.path.join(temp_folder, filename)

    # Write the metadata to a JSON file
    with open(metadata_file_path, "w") as json_file:
        json.dump(metadata, json_file, indent=4)

    # Send the metadata JSON file to the user
    return send_file(metadata_file_path, as_attachment=True, download_name=filename)

# User Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))
