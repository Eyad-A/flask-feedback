from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback 
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm 
from werkzeug.exceptions import Unauthorized
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgres:///feedback")

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def homepage():
    """Homepage route"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Render a registration form and handle form submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}") 

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 

        user = User.register(username, password, email, first_name, last_name)
    
        db.session.commit() 
        session['username'] = user.username 

        return redirect(f"/users/{user.username}") 
    
    else: 
        return render_template("register.html", form=form) 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show login form and handle login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 

        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username 
            return redirect(f"/users/{user.username}") 
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("login.html", form=form)
        
    return render_template("login.html", form=form)



@app.route("/logout")
def logoout():
    """Logout"""

    session.pop("username")
    return redirect("/")


@app.route("/users/<username>")
def show_user(username):
    """Show information on user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm() 

    return render_template("show_user.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete a user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/") 


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Show feedback form and process submission"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data 
        content = form.content.data 
        feedback = Feedback(title=title, content=content, username=username,)

        db.session.add(feedback)
        db.session.commit() 
        return redirect(f"/users/{feedback.username}") 

    else: 
        return render_template("new_feedback.html", form=form) 


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show the update feedback form and process it""" 

    feedback = Feedback.query.get(feedback_id) 
    
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized() 

    form = FeedbackForm(obj=feedback) 

    if form.validate_on_submit():
        feedback.title = form.title.data 
        feedback.content = form.content.data 

        db.session.commit() 

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/edit_feedback.html", form=form, feedback=feedback) 


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"]) 
def delete_feedback(feedback_id):
    """Delete a feedback"""

    feedback = Feedback.query.get(feedback_id) 

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized() 

    form = DeleteForm() 

    if form.validate_on_submit():
        db.session.delete(feedback) 
        db.session.commit() 

    return redirect(f"/users/{feedback.username}") 