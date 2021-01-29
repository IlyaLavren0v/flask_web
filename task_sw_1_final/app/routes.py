from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import BookForm, LoginForm, UserRegisterForm, LogoutForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book
from werkzeug.urls import url_parse

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = UserRegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created.")
        return redirect(url_for('login'))
    if request.method == 'POST' and not form.validate():  
        flash(f"Invalid credentials while register.")
        return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid credentials while login")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f"User successfully logged-in")
        next_pages = request.args.get('next')
        if not next_pages or url_parse(next_pages).netloc !='':
            next_pages = url_for('books_list')
        return redirect(next_pages)   
    return render_template('login.html', form=form,)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('home'))
    return render_template('logout.html', form=form)

@app.route('/books', methods=['GET'])
@login_required
def books_list():
    books = Book.query.all()
    return render_template('books_list.html', books=books)

@app.route('/books/<id>/detail', methods=['GET'])
@login_required
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def book_new():
    form = BookForm()
    if request.method == 'POST' and form.validate():
        new_book = Book(title=form.title.data, author=form.author.data, pages_amount=form.pages_amount.data, owner=current_user)
        db.session.add(new_book)
        db.session.commit()
        flash('Create book')
        return redirect(url_for('book_detail',id=new_book.id))
    return render_template('book_new.html', form=form)

@app.route('/books/<id>/delete', methods=['GET', 'POST'])
@login_required
def book_delete(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST' and book:
        db.session.delete(book)
        db.session.commit()
        flash("Book successfully delted")
        return redirect(url_for('books_list'))
    return render_template('book_delete.html', book=book)

@app.route('/books/<id>/edit', methods=['GET', 'POST'])
@login_required
def book_update(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if request.method == 'POST' and form.validate():
        book.title = form.title.data 
        book.author = form.author.data
        book.pages_amount = form.pages_amount.data
        db.session.add(book)
        db.session.commit()
        flash("Successfully editing book")
        return redirect(url_for("book_detail", id=book.id))
    return render_template("book_edit.html", book=book, form=form)

@app.route('/')
def home():
    return render_template('home.html')
