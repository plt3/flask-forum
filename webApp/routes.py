from flask import redirect, render_template, url_for

from webApp import app, db
from webApp.forms import PostForm
from webApp.models import Post


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
