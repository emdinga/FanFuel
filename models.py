from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    picture = db.Column(db.String(200), nullable=True, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False, default='offline')
    streams = db.relationship('Stream', backref='profile', lazy=True)
    
    def __repr__(self):
        return f'<Profile {self.username}>'

class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    streamer_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    is_live = db.Column(db.Boolean, default=False)
    viewers_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stream {self.title}>'
