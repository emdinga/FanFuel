#!/usr/bin/env python3
""" Flask application for live streams """

from models import Stream, db, Profile, User
from flask import render_template, Flask, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

""" SQLite DB configuration """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fanfuel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.secret_key = '123456789'

"""Initialize the database"""
db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    """Create tables if they don't exist"""
    with app.app_context():
        db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for starting a stream
@app.route('/start_stream', methods=['GET', 'POST'])
@login_required
def start_stream():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Title is required!')
            return redirect(url_for('start_stream'))

        new_stream = Stream(title=title, description=description, streamer_id=current_user.id, is_live=True)
        db.session.add(new_stream)
        db.session.commit()
        flash('Stream started successfully!')
        return redirect(url_for('home'))

    return render_template('start_stream.html')

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('home'))

# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        flash('Invalid credentials!')
        return redirect(url_for('login'))
    return render_template('login.html')

# Route for signing up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')
@app.route('/')
def home():
    # Query for live streams
    streams = Stream.query.filter_by(is_live=True).all()
    
    # Query for profiles if no streams are live
    if not streams:
        profiles = Profile.query.all()
    else:
        profiles = []

    return render_template('home.html', streams=streams, profiles=profiles)

@app.route('/watch/<int:stream_id>')
def watch_stream(stream_id):
    """ Display live streams """
    stream = Stream.query.get_or_404(stream_id)
    return render_template('watch_stream.html', stream=stream)

@app.route('/profile')
@login_required
def profile():
    """ Show user profile """
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    """Run migrations before starting the app"""
    with app.app_context():
        """Apply migrations (Create tables if they don't exist)"""
        from flask_migrate import upgrade
        upgrade()
    app.run(host='0.0.0.0', port=5000, debug=True)
