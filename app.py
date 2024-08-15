#!/usr/bin/env python3
""" Flask application for live streams """

from models import Stream, db
from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

""" SQLite DB configuration """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fanfuel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

""" Initialize the database """
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    """ Query for active streams """
    streams = Stream.query.filter_by(is_live=True).all()
    return render_template('home.html', streams=streams)

@app.route('/watch/<int:stream_id>')
def watch_stream(stream_id):
    """ Display live streams """
    stream = Stream.query.get_or_404(stream_id)
    return render_template('watch_stream.html', stream=stream)

if __name__ == '__main__':
    """Run migrations before starting the app"""
    with app.app_context():
        """Apply migrations (Create tables if they don't exist)"""
        from flask_migrate import upgrade
        upgrade()
    app.run(host='0.0.0.0', port=5000, debug=True)
