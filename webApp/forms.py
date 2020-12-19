from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    title = StringField("Title:", validators=[DataRequired()])
    content = TextAreaField("Content:", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    postId = HiddenField("postId")
    name = StringField("Name:", validators=[DataRequired()])
    content = TextAreaField("Content:", validators=[DataRequired()])
    submit = SubmitField("Post a comment...")
