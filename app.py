from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your-secret-key"

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="eteshsingh12345",
        database="Akatsuki_Group",
    )
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']   # storing directly (NO hashing)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Email already exists!')
            cursor.close()
            conn.close()
            return redirect(url_for('signup'))

        cursor.execute("INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
                       (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Account created! Please login.')
        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # entered password

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] == password:   # simple check without hashing
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

def login_required_redirect(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/home')
@login_required_redirect
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required_redirect
def dashboard():
    return render_template('dashboard.html')

@app.route('/contact')
@login_required_redirect
def contact():
    return render_template('contact.html')

@app.route('/about')
@login_required_redirect
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
