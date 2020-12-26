from flask import redirect, render_template, request, url_for

from webApp import app, db
from webApp.forms import CommentForm, PostForm
from webApp.models import Comment, Post
from webApp.utils import createListDict


@app.route("/")
def home():
    PER_PAGE = 5

    search = request.args.get("q", default="")
    page = request.args.get("page", default=1, type=int)

    if search == "":
        posts = Post.query.order_by(Post.id.desc()).paginate(
            page=page, per_page=PER_PAGE
        )
    else:
        posts = (
            Post.query.filter(
                (Post.content.contains(search)) | (Post.title.contains(search))
            )
            .order_by(Post.id.desc())
            .paginate(page=page, per_page=PER_PAGE)
        )

    return render_template("home.html", posts=posts, search=search)


@app.route("/post/<int:postId>")
def post(postId):
    form = CommentForm()

    postObj = Post.query.get(postId)
    commentQuery = Comment.query.filter(Comment.postedOn == postObj).all()

    # createListDict loads all the comment objects into a nested dictionary (fakeJson)
    # to avoid querying the database with every new comment

    fakeJson = createListDict(commentQuery)

    # DELETE THIS ONCE JAVASCRIPT IS UNCACHED

    import time

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


@app.route("/api/getPosts", methods=["GET"])
def apiGetPosts():
    page = request.args.get("page", default=1, type=int)
    perPage = request.args.get("perPage", default=20, type=int)

    if perPage > 20:
        perPage = 20

    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=perPage)

    return {"response": [post.toDict() for post in posts.items]}


@app.route("/api/getComments", methods=["GET"])
def apiGetComments():
    page = request.args.get("page", default=1, type=int)
    perPage = request.args.get("perPage", default=20, type=int)
    postId = request.args.get("post", default=0, type=int)

    if perPage > 20:
        perPage = 20

    if postId == 0:
        comments = Comment.query.order_by(Comment.id.desc()).paginate(
            page=page, per_page=perPage
        )
    else:
        comments = (
            Comment.query.filter(Comment.postId == postId)
            .order_by(Comment.id.desc())
            .paginate(page=page, per_page=perPage)
        )

    return {"response": [comment.toDict() for comment in comments.items]}


@app.route("/api/createPost", methods=["POST"])
def apiCreatePost():
    userData = request.get_json(force=True) or {}
    newPost = Post.fromDict(userData)

    db.session.add(newPost)
    db.session.commit()

    return newPost.toDict()


@app.route("/api/<int:postId>/addComment", methods=["POST"])
def apiAddComment(postId):
    userData = request.get_json(force=True) or {}
    newComment = Comment.fromDict(userData, postId)

    db.session.add(newComment)
    db.session.commit()

    return newComment.toDict(timeFormat=request.json.get("timeFormat", False))


@app.errorhandler(404)
def pageNotFound(error):
    # determine if user wants JSON or HTML response and return appropriate error message
    if (
        request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
    ):
        return {"response": "404: Page not found."}, 404
    else:
        return render_template("errors/404.html"), 404
