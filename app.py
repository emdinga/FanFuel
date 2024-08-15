#!/usr/bin/env python3
""" Flask application for live streams"""


from models import Stream
from flask import render_template, Flask

app = Flask(__name__)


@app.route('/')
def home():
    """Query for active streams"""
    streams = Stream.query.filter_by(is_live=True).all()
    return render_template('home.html', streams=streams)

@app.route('/watch/<int:stream_id>')
def watch_stream(stream_id):
    """display live streams"""
    stream = Stream.query.get_or_404(stream_id)
    return render_template('watch_stream.html', stream=stream)


if __name__ == '__main__':
    app.run()