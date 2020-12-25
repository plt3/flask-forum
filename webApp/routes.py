import time

from flask import redirect, render_template, request, url_for

from webApp import app, db
from webApp.forms import CommentForm, PostForm
from webApp.models import Comment, Post
from webApp.utils import createListDict


@app.route("/")
def home():
    PER_PAGE = 5

    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=PER_PAGE)

    return render_template("home.html", posts=posts)


@app.route("/post/<int:postId>")
def post(postId):
    form = CommentForm()

    postObj = Post.query.get(postId)
    commentQuery = Comment.query.filter(Comment.postedOn == postObj).all()

    # createListDict loads all the comment objects into a nested dictionary (fakeJson)
    # to avoid querying the database with every new comment

    fakeJson = createListDict(commentQuery)

    # DELETE t=time.time() once javascript is good!!!

    return render_template(
        "post.html",
        post=postObj,
        data=fakeJson,
        numComments=len(commentQuery),
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
    newComment = Comment.fromDict(request.json, postId)

    db.session.add(newComment)
    db.session.commit()

    return newComment.toDict()


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("errors/404.html"), 404
