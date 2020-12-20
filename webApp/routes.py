import time
from datetime import datetime

from flask import redirect, render_template, request, url_for

from webApp import app, db
from webApp.forms import CommentForm, PostForm
from webApp.models import Post
from webApp.utils import createListDict

# these also need a date posted and then I need to fix the patch in utils.py

listComments = [
    {
        "author": "Mr. Paul",
        "id": 1,
        "postedOn": 1,
        "content": "here is first comment, very nice",
        "replyTo": 0,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 2,
        "content": "second comment yolo",
        "replyTo": 0,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 3,
        "content": "first reply to 2",
        "replyTo": 2,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 4,
        "content": "second reply to 2",
        "replyTo": 2,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 5,
        "content": "third reply to 2 this is so facts",
        "replyTo": 2,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 6,
        "content": "nah mr. facts you're kinda wrong",
        "replyTo": 5,
    },
    {
        "author": "I am the coolest person in the entire world and I would like you to know that",
        "postedOn": 1,
        "id": 7,
        "content": "what? he's super right bro you have no idea how bigoted your comment sounds to someone like me who knows the lay of the land so much better",
        "replyTo": 6,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 8,
        "content": "nah you aren't dawg",
        "replyTo": 6,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 9,
        "content": "just back one level out",
        "replyTo": 2,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 10,
        "content": "main level baby",
        "replyTo": 0,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 11,
        "content": "should be responding to comment 5",
        "replyTo": 5,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 12,
        "content": "I agree with comment 8",
        "replyTo": 8,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 13,
        "content": "It's true, he's super right",
        "replyTo": 7,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 14,
        "content": "testing",
        "replyTo": 10,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 15,
        "content": "replying to the OG man",
        "replyTo": 1,
    },
    {
        "author": "Mr. Paul",
        "postedOn": 1,
        "id": 16,
        "content": "yes you are indeed",
        "replyTo": 11,
    },
]


@app.route("/")
def home():
    # should probably paginate at some point
    posts = Post.query.all()
    posts.reverse()

    return render_template("home.html", posts=posts)


@app.route("/post/<int:postId>")
def post(postId):
    form = CommentForm()

    postObj = Post.query.get(postId)
    dataQuery = listComments
    fakeJson = createListDict(dataQuery)

    # DELETE t=time.time() once javascript is good!!!

    return render_template(
        "post.html",
        post=postObj,
        data=fakeJson,
        numComments=len(dataQuery),
        form=form,
        t=time.time(),
    )


@app.route("/createPost", methods=["GET", "POST"])
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


@app.route("/addComment/<int:postId>", methods=["POST"])
def addComment(postId):
    # this needs a lot more input sanitization

    # this is a stand-in for adding to the database

    comDict = {
        "id": max([com["id"] for com in listComments]) + 1,
        "postedOn": postId,
        "author": request.json.get("name", "Generic User"),
        "content": request.json.get("content", "no content"),
        "replyTo": request.json.get("replyTo", 0),
    }

    listComments.append(comDict)

    comDict["date"] = datetime.now().strftime("%-m/%-d/%Y, %-I:%M %p")

    return comDict
