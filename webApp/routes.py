from flask import redirect, render_template, url_for

from webApp import app, db
from webApp.forms import PostForm
from webApp.models import Post
from webApp.utils import createListDict

listComments = [
    {"id": 1, "content": "here is first comment, very nice", "replyTo": 0},
    {"id": 2, "content": "second comment yolo", "replyTo": 0},
    {"id": 3, "content": "first reply to 2", "replyTo": 2},
    {"id": 4, "content": "I agree with whomever said 3", "replyTo": 2},
    {"id": 5, "content": "this is so facts", "replyTo": 2},
    {"id": 6, "content": "nah mr. facts you're kinda wrong", "replyTo": 5},
    {"id": 7, "content": "what? he's super right bro", "replyTo": 6},
    {"id": 8, "content": "nah you aren't dawg", "replyTo": 6},
    {"id": 9, "content": "just back one level out", "replyTo": 2},
    {"id": 10, "content": "main level baby", "replyTo": 0},
    {"id": 11, "content": "should be responding to comment 5", "replyTo": 5},
    {"id": 12, "content": "I agree with comment 8", "replyTo": 8},
    {"id": 13, "content": "It's true, he's super right", "replyTo": 7},
    {"id": 14, "content": "testing", "replyTo": 10},
    {"id": 15, "content": "replying to the OG man", "replyTo": 1},
    {"id": 16, "content": "yes you are indeed", "replyTo": 11},
]


@app.route("/")
def home():
    posts = Post.query.all()

    return render_template("home.html", posts=posts)


@app.route("/post", methods=["GET", "POST"])
def createPost():
    form = PostForm()

    if form.validate_on_submit():
        postObj = Post(
            author=form.name.data, title=form.title.data, content=form.content.data
        )
        db.session.add(postObj)
        db.session.commit()

        # should flash a message here

        return redirect(url_for("home"))

    return render_template("createPost.html", form=form)


@app.route("/test")
def test():
    dataQuery = listComments
    fakeJson = createListDict(dataQuery)
    return render_template("commentTest.html", data=fakeJson)
