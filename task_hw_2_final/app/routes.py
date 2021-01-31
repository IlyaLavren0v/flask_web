from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import BookForm, JournalForm, LoginForm, UserRegisterForm, UpdateAccountForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book, Journal
from werkzeug.urls import url_parse
import secrets
import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = form_picture.filename.split('.')[-1]
    picture_fn = random_hex + '.' +  f_ext
    picture_path = os.path.join(app.root_path, 'static/media', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == 'POST' and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_Name = form.last_Name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('account'))
    if request.method == 'POST' and not form.validate_on_submit():
        flash('Error while profile updating', 'danger')
    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = UserRegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, first_name=form.first_name.data, last_Name=form.last_Name.data, age=form.age.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Great you've registered.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login credetials")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f"Successfully logged_in as { user.username }")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('home')
        return redirect(next_page)   
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/publish')
@login_required
def create_list():
    return render_template('create_list.html')

@app.route('/books')
@login_required
def books_list():
    books = Book.query.all()
    return render_template('books_list.html', books=books)

@app.route('/books/books_reversed')
@login_required
def books_reversed():
    books = Book.query.all()
    return render_template('books_reversed.html', books=books)

@app.route('/books/book/<id>', methods=['GET'])
@login_required
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

@app.route('/publish/book', methods=['GET', 'POST'])
@login_required
def book_create():
    form = BookForm()
    if request.method == 'POST' and form.validate():
        new_book = Book(title=form.title.data, author=form.author.data, rating=form.rating.data, book_owner=current_user)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            new_book.image_file = picture_file
        db.session.add(new_book)
        db.session.commit()
        flash('The book was published successfully!')
        return redirect(url_for('books_list'))
    image_file = url_for('static', filename='media/' + Book.image_file)
    return render_template('book_create.html', image_file=image_file, form=form)

@app.route('/books/book/<id>/update', methods=['GET', 'POST'])
@login_required
def book_update(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if request.method == 'POST' and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            book.image_file = picture_file
        book.title = form.title.data 
        book.author = form.author.data
        book.rating = form.rating.data
        db.session.add(book)
        db.session.commit()
        flash("Successfully updated book")
        return redirect(url_for("book_detail", id=book.id))
    image_file = url_for('static', filename='media/' + book.image_file)
    return render_template("book_update.html", book=book, image_file=image_file, form=form)

@app.route('/books/book/<id>/delete', methods=['GET', 'POST'])
@login_required
def book_delete(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST' and book:
        db.session.delete(book)
        db.session.commit()
        flash("Post successfully delted")
        return redirect(url_for('books_list'))

    return render_template('book_delete.html', book=book)

@app.route('/journals')
@login_required
def journals_list():
    journals = Journal.query.all()
    return render_template('journals_list.html', journals=journals)

@app.route('/journals/journals_reversed')
@login_required
def journals_reverse():
    journals = Journal.query.all()
    return render_template('journals_reversed.html', journals=journals)

@app.route('/journals/journal/<id>', methods=['GET'])
@login_required
def journal_detail(id):
    journal = Journal.query.get_or_404(id)
    return render_template('journal_detail.html', journal=journal)

@app.route('/publish/journal', methods=['GET', 'POST'])
@login_required
def journal_create():
    form = JournalForm()
    if request.method == 'POST' and form.validate():
        new_journal = Journal(title=form.title.data, editor=form.editor.data, page_amount=form.page_amount.data, journal_owner=current_user)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            new_journal.image_file = picture_file
        db.session.add(new_journal)
        db.session.commit()
        
        flash('The journal was published successfully!')
        return redirect(url_for('journals_list'))
    image_file = url_for('static', filename='media/' + Journal.image_file)
    return render_template('journal_create.html', image_file=image_file, form=form)

@app.route('/journals/journal/<id>/update', methods=['GET', 'POST'])
@login_required
def journal_update(id):
    journal = Journal.query.get_or_404(id)
    form = JournalForm(obj=journal)
    if request.method == 'POST' and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            journal.image_file = picture_file
        journal.title = form.title.data 
        journal.editor = form.editor.data
        journal.page_amount = form.page_amount.data
        db.session.add(journal)
        db.session.commit()
        flash("Successfully updated journal")
        return redirect(url_for("journal_detail", id=journal.id))
    image_file = url_for('static', filename='media/' + journal.image_file)
    return render_template("journal_update.html", journal=journal, image_file=image_file, form=form)

@app.route('/journals/journal/<id>/delete', methods=['GET', 'POST'])
@login_required
def journal_delete(id):
    journal = Journal.query.get_or_404(id)
    if request.method == 'POST' and journal:
        db.session.delete(journal)
        db.session.commit()
        flash("Post successfully delted")
        return redirect(url_for('journals_list'))
    return render_template('journal_delete.html', journal=journal)
