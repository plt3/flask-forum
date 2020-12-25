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

    def toDict(self):
        """
        Convert Comment object to dictionary for /addComment/<postId> to return
        """
        selfDict = {
            "id": self.id,
            "postedOn": self.postId,
            "author": self.author,
            "content": self.content,
            "replyTo": self.replyId,
            "created": self.created.strftime("%-m/%-d/%Y, %-I:%M %p"),
        }

        return selfDict

    @classmethod
    def fromDict(cls, commentDict, postNum):
        """
        Create Comment object from POST request body passed to /addComment/<postId>
        """
        newComment = cls(
            author=commentDict.get("name", "Generic User"),
            content=commentDict.get("content", "no content"),
            postId=postNum,
            replyId=commentDict.get("replyTo", 0),
        )

        return newComment

    def __repr__(self):
        return f"<Comment on post {self.postId} replying to {self.replyId}>"
