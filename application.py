# import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
# db = SQL("sqlite:///amstest.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
def index():
    """Show index page"""
    return render_template("index.html")


@app.route("/viewall")
def viewall():
    """View all articles on the database"""
    return render_template("viewall.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Sell shares of stock"""

    if request.method == "POST":
#         symbol = request.form.get("symbol")
#         shares = int(request.form.get("shares"))
#         if not symbol:
#             return apology("must provide symbol", 400)
#         quote = lookup(symbol)

#         if not quote:
#             return apology("Enter a valid symbol plix", 400)
#         if not shares:
#             return apology("must provide shares", 400)
#         if shares < 1:
#             return apology("shares should be a positive integer", 400)
#         symbol = quote['symbol']
#         rows = db.execute("SELECT SUM(shares) FROM tranzact WHERE user_id = :id AND symbol = :symbol",
#                           id=session["user_id"], symbol=symbol)

#         stock = rows[0]['SUM(shares)']
#         if not stock:
#             return apology(f"Sorry ... You don't have any shares with {quote['name']}", 400)

#         if stock < shares:
#             return apology(f"Sorry ... You don't have enough {quote['name']} shares to sell", 400)

#         price = shares * quote['price']
#         shares = -shares

#         db.execute("INSERT INTO tranzact (user_id, symbol, shares, price) VALUES (:user, :symbol, :shares, :price)",
#                    user=session["user_id"], symbol=symbol, shares=shares, price=quote["price"])

#         rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
#         cash = rows[0]['cash']
#         balance = cash + price
#         db.execute("UPDATE users SET cash=:balance WHERE id=:id", balance=balance, id=session["user_id"])

#         # Redirect user to home page
        return redirect("/")
    else:
#         rows = db.execute("SELECT symbol FROM tranzact WHERE user_id=:id", id=session["user_id"])
#         symbols = []
#         for row in rows:
#             symbols.append(row['symbol'])
#         symbols = list(set(symbols))
#         data = []
#         for symbol in symbols:
#             rows = db.execute("SELECT symbol, SUM(shares) FROM tranzact WHERE user_id=:id AND symbol=:symbol",
#                             id=session["user_id"], symbol=symbol)
#             if rows[0]['SUM(shares)'] > 0:
#                 data.append(rows[0]['symbol'])
#         print(data)
        return render_template("search.html")


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

        #     # Check if username/email already exist
            if len(rows) > 0:
                return render_template("register.html", msg="username/email already exists")

            hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash, email) VALUES (:username, :hash, :email)",
                       username=username, hash=hash, email=email)

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
#         # Ensure usermail and password were submitted
        if not username or not password:
            return render_template("login.html", msg="all fields must be filled")

#         # Query database for username/mail
        rows = db.execute("SELECT * FROM users WHERE username = :username OR email =:email",
#                           username=username, email=email)

#         # Ensure username/email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", msg="invalid username and/or password")
#         print
#         # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/view")
# @login_required
def view():
    """Show history of transactions"""

    # rows = db.execute("SELECT symbol, shares, price, time FROM tranzact WHERE user_id=:id ORDER BY time DESC",
    #                   id=session["user_id"])
    print(rows)
    return render_template("view.html")


@app.route("/edit", methods=["GET", "POST"])
# @login_required
def edit():
    """Get stock quote."""
    if request.method == "POST":

        return render_template("edited.html")

    else:
        return render_template("add_article.html")




# @app.route("/delete", methods=["GET"])
# def check():
    # """Return true if username available, else false, in JSON format"""
    # username = request.args.get("username")
    # print(username)
    # # Query database for username
    # rows = db.execute("SELECT * FROM users WHERE username = :username",
    #                   username=username)
    # print(rows)
    # # Ensure username exists and password is correct
    # if len(rows) >= 1:
    #     return jsonify(False)
    # else:
    #     return jsonify(True)


# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# # Listen for errors
# for code in default_exceptions: