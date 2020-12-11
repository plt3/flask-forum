from datetime import datetime

from webApp import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(20000), nullable=False)

    def __repr__(self):
        return f"<Post {self.title[:30]} by {self.author}>"
