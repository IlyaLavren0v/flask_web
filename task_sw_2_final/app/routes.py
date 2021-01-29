from app.forms import LoginForm, RegistrationForm, UpdateProfileForm, LogoutForm, PasswordChangeForm
from flask import redirect, url_for, render_template, flash, request
from app import app, db
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import secrets
import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) 
    file_ext = form_picture.filename.split('.')[-1]
    picture_filename = random_hex + "." +  file_ext
    picture_path = os.path.join(app.root_path, 'static/media/' , picture_filename)
    form_picture.save(picture_path)
    return picture_filename

@app.route("/")
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    if request.method == 'POST' and not form.validate_on_submit():
        flash('Error while profile updating', 'danger')
    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template("profile.html", image_file=image_file, form=form)

@app.route('/password/change/done')
@login_required
def done():
    return render_template("done.html", title="Done")

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html')
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    if request.method == 'POST' and not form.validate():
        flash('Invalid credentials. Try again', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials. Try again', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('profile')
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route('/password/change', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials. Try again', 'danger')
            return redirect(url_for('login'))
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('done'))
    return render_template('password_change.html', form=form)
