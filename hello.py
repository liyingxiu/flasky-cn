from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"

bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# 如果新提交的名字和之前存储的名字不同，则会调用flash函数
# 如果只调用flash函数并不能显示出来，需要使用模版进行渲染
@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("looks like you have changed your name!")
        session["name"] = form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"))


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
