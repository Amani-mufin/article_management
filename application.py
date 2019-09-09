import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import login_required, allowed_file

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ams.db")


@app.route("/")
def index():
    """Show index page"""
    return render_template("index.html")


@app.route("/viewall")
def viewall():
    """View all articles on the database"""
    
    rows = db.execute("""SELECT articles.id, users.username, articles.title, articles.description, 
    articles.content, articles.like, articles.dislike, articles.image, articles.date 
    FROM users JOIN articles ON users.id = articles.userid  ORDER BY date DESC""")
    return render_template("view.html", data=rows)


@app.route("/viewone/<id>")
def viewone(id):
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM users JOIN articles ON users.id = articles.userid WHERE articles.id=:id", id=id)
    if rows[0]['image']:
        rows[0]['image'] = "../" + rows[0]['image']
    return render_template("viewone.html", datum=rows[0])


@app.route("/viewall/<id>")
def viewall_author(id):
    """View all articles on the database"""
    
    rows = db.execute("""SELECT articles.id, users.username, articles.title, articles.description, 
    articles.content, articles.like, articles.dislike, articles.image, articles.date 
    FROM users JOIN articles ON users.id = articles.userid WHERE articles.userid = :id ORDER BY date DESC""", id=id)

    for row in rows:
        if row['image']:
            row['image'] = "../" + row['image']

    return render_template("view.html", data=rows)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Sell shares of stock"""

    if request.method == "POST":
        search =  "%"+ request.form.get("search").strip()+"%"
        # check for empty search key
        if search=="%%":
            return render_template("view.html", msg=" Enter a valid search key")
        # search db with search key
        data = db.execute("SELECT articles.id, users.username, articles.title, articles.description, articles.content, articles.like, articles.dislike, articles.image, articles.date FROM users JOIN articles ON users.id = articles.userid WHERE username LIKE (:search)  OR title LIKE (:search)  OR description LIKE (:search)  OR content LIKE (:search)  ORDER BY date DESC", search=search)
        if not data:
            return render_template("view.html", msg=" article not found ")
        else:
            return render_template("view.html", data=data)
        


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure all fields were submitted
        if not username or not password or not confirmation or not email:
            return render_template ("register.html", msg="all fields must be filled")
        # ensure passwords match
        if password != confirmation:
            return render_template ("register.html", msg="passwords must match")
        
        #ensure username and email are unique
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username OR email =:email",
                              username=username, email=email)

            # Check if username/email already exist
            if len(rows) > 0:
                return render_template("register.html", msg="username/email already exists")

            hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)",
                       username=username, password=hash, email=email)

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        usermail = request.form.get("usermail").strip()
        password = request.form.get("password")
        # Ensure usermail and password were submitted
        if not usermail or not password:
            return render_template("login.html", msg="all fields must be filled")

        # Query database for username/mail
        rows = db.execute("SELECT * FROM users WHERE username = :username OR email =:email",
                           username=usermail, email=usermail)

        # Ensure username/email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return render_template("login.html", msg="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/view")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/article", methods=["GET", "POST"])
@login_required
def article():
    if request.method == "POST":
        userid = session["user_id"]
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        like = 0
        dislike =0
        if not title or not description or not content:
            return render_template ("add_article.html", msg="Title, Description and Content fields must be filled")

        file = request.files['image']
        
        if not allowed_file(file.filename):
            return render_template("add_article.html", msg="Wrong file type selected. You can only use png, jpg, jpeg and gif")

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = UPLOAD_FOLDER + filename
        # return redirect(url_for('uploaded_file', filename=filename))
        
        db.execute("INSERT INTO articles ('userid', 'title', 'description', 'content','like', 'dislike', 'image') VALUES (:userid, :title, :description, :content, :like, :dislike, :image)",
            userid=userid, title=title, description=description, content=content, like=like, dislike=dislike, image=image)
        return redirect("/viewall")

    else:
        return render_template("add_article.html")


@app.route("/view")
@login_required
def userView():
        userid = session["user_id"]
        data = db.execute("SELECT articles.id, users.username, articles.title, articles.description, articles.content, articles.like, articles.dislike, articles.image, articles.date FROM users JOIN articles ON users.id = articles.userid WHERE articles.userid = :userid ORDER BY date DESC", 
        userid=userid)
        return render_template("userView.html", data=data)


@app.route("/like/<id>", methods=["GET", "POST"])
def like(id):
    data= db.execute("select * FROM articles WHERE id= :id", id=id)
    db_like = data[0]["like"]+1
    db.execute("UPDATE articles SET like=:like WHERE id=:id",id=id, like=db_like)
    return redirect("/viewall")

@app.route("/dislike/<id>", methods=["GET", "POST"])
def dislike(id):
    data= db.execute("select * FROM articles WHERE id= :id", id=id)
    db_dislike = data[0]["dislike"]+1
    db.execute("UPDATE articles SET dislike=:dislike WHERE id=:id",id=id, dislike=db_dislike)
    return redirect("/viewall")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        userid = session["user_id"]
        title = request.form.get("title")
        description = request.form.get("description")
        content = request.form.get("content")
        image = request.form.get("image")
        db.execute("UPDATE articles SET title=:title, description=:description, content=:content, image=:image WHERE id=:id",
            title=title, description=description, content=content, image=image, id=id)
        return redirect("/view")
    else:
        data= db.execute("select * FROM articles WHERE id= :id", id=id)
        return render_template("edit.html", data=data)


@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    """Return true if username available, else false, in JSON format"""
    
    # DELETE ITEM FROM database WITH ID
    db.execute("DELETE FROM articles WHERE id = :id", id=id)
    # get the remaining article from DB
    userid = session["user_id"]
    data = db.execute("SELECT articles.id, users.username, articles.title, articles.description, articles.content, articles.like, articles.dislike, articles.image, articles.date FROM users JOIN articles ON users.id = articles.userid WHERE articles.userid = :userid", 
        userid=userid)
    for datum in data:
        if datum['image']:
            datum['image'] = "../"+datum['image']
    return render_template("userView.html", data=data, msg="Article deleted successfully")