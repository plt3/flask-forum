from flask import redirect, render_template, request, url_for

from webApp import app, db
from webApp.forms import CommentForm, PostForm
from webApp.models import Comment, Post
from webApp.search import addPostToIndex
from webApp.utils import createListDict


@app.route("/")
def home():
    PER_PAGE = 10

    search = request.args.get("q", default="")
    page = request.args.get("page", default=1, type=int)

    if search == "":
        posts = Post.query.order_by(Post.id.desc()).paginate(
            page=page, per_page=PER_PAGE
        )
    else:
        searchQuery = Post.search(search)
        if searchQuery is None:
            posts = None
        else:
            posts = searchQuery.paginate(page=page, per_page=PER_PAGE)

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
        addPostToIndex(postObj)

        # should flash a message here

        return redirect(url_for("home"))

    return render_template("createPost.html", form=form)


@app.route("/api/posts", methods=["GET"])
def apiGetPosts():
    page = request.args.get("page", default=1, type=int)
    perPage = request.args.get("perPage", default=20, type=int)
    id = request.args.get("id", default=0, type=int)

    if perPage > 20:
        perPage = 20

    if id == 0:
        posts = Post.query.order_by(Post.id.desc()).paginate(
            page=page, per_page=perPage
        )

        return {
            "response": [post.toDict() for post in posts.items],
            "hasNext": posts.has_next,
        }
    else:
        return Post.query.get_or_404(id).toDict()


@app.route("/api/comments", methods=["GET"])
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

    return {
        "response": [comment.toDict() for comment in comments.items],
        "hasNext": comments.has_next,
    }


@app.route("/api/createPost", methods=["POST"])
def apiCreatePost():
    userData = request.get_json(force=True) or {}
    newPost = Post.fromDict(userData)

    db.session.add(newPost)
    db.session.commit()
    addPostToIndex(newPost)

    return newPost.toDict()


@app.route("/api/<int:postId>/addComment", methods=["POST"])
def apiAddComment(postId):
    Post.query.get_or_404(
        postId
    )  # return 404 if trying to post comment on nonexisting post

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
