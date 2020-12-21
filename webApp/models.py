from datetime import datetime

from webApp import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(20000), nullable=False)
    comments = db.relationship("Comment", backref="postedOn", lazy=True)

    def __repr__(self):
        return f"<Post {self.title[:30]} by {self.author}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    replyId = db.Column(
        db.Integer, db.ForeignKey("comment.id"), nullable=False, default=0
    )
    replies = db.relationship(
        "Comment", backref=db.backref("replyTo", remote_side=[id]), lazy=True
    )

    def __repr__(self):
        return f"<Comment on post {self.postId} replying to {self.replyId}>"

    # this class really needs a from_dict and to_dict method for use in /addComment/*
    # API endpoint!!!
