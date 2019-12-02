# ASK ABOUT HOW TO IMPORT ALL OF THIS
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database, will need tables for follower/followee + people at each location
db = SQL("sqlite:///friends.db")

@app.route("/")
@login_required
def map():
    """Show interactive map of where students are on campus Note: potential harry potter theme!!!"""
    # Query for all relevant info for how many students are at each study spot
    
    return render_template("map.html", rows=rows)


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    """Check the user into a study location"""
     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        location = request.form.get("location")
        check = request.form.get("check") 

        #Ensure the location exists and the number of shares is positive
        if location == '':
            return apology("must provide location")
        # Check the user in
        elif check == "in":            
            # cancel process if user is already checked into that location (figure it out)
            else:
                db.execute # update query to add 1 to user's location
            
        elif check == "out":                       
            # cancel process if user is not already checked into that location (figure it out)
            
            # insert the transaction into the database
            else:
                db.execute # update query to subtract 1 to user's location

                return redirect("/confirm")

    #User reached route via GET, display form to request stock quote
    else:
        return render_template("check.html")


@app.route("/confirm")
@login_required
def confirm():
    """Confirm user successfully submitted request"""
    
    return render_template("confirm.html")


@app.route("/friends", methods=["GET", "POST"])
def friends():
    """Allow user to follow their friends and see their current location in a table"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        new=request.form.get("new")

        # Ensure username, password, and new password are all correctly submitted
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide old password", 403)
        elif not new:
            return apology("must provide new password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct before changing password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        else:
            db.execute("UPDATE users SET hash=:hash WHERE username=:username", hash=generate_password_hash(new), username=username)

        return redirect("/")

    else:
        return render_template("change.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        #Ensure the symbol exists
        if symbol == '':
            return apology("must provide symbol", 403)
        elif lookup(symbol) == None:
            return apology("invalid symbol", 403)

        #Look up the stock symbol and get a quote
        else:
            quote = lookup(symbol)
            quote["price"] = usd(quote["price"])
            return render_template("quoted.html", quote=quote)

    #User reached route via GET, display form to request stock quote
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure username is not already taken
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        if len(rows) != 0:
            return apology("username already taken", 403)

        # Ensure password and confirmation password were submitted
        elif not password or not confirmation:
            return apology("must provide password", 403)

        # Ensure passwords match
        elif password != confirmation:
            return apology("passwords don't match", 403)

        #Add new users to your users database
        else:
            session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    # Identify all symbols of purchased stocks and add them to a list
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id=:user_id GROUP BY symbol", user_id=session["user_id"])
    symbolList = []
    for item in symbols:
        symbolList.append(item['symbol'])

    # Figure out the number of shares you own of the chosen stock
    owned = db.execute("SELECT SUM(shares) FROM transactions WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol)
    ownedShares = owned[0]['SUM(shares)']

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
       #Ensure the symbol exists and the number of shares is positive
        if symbol not in symbolList:
            return apology("invalid symbol", 403)
        elif int(shares) <= 0:
            return apology("must provide a positive number of shares", 403)
        elif int(shares) > ownedShares:
            return apology("user does not own enough shares", 403)
        # make the transaction
        else:
            quote = lookup(symbol) # Look up the stock symbol and get a quote
            # Get value of current cash blance
            cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"]) # returns a dictionary
            currentCash = cash[0]['cash']

            # insert the transaction into the database
            db.execute("INSERT INTO transactions (user_id, name, symbol, price, shares) VALUES (:user_id, :name, :symbol, :price, :shares)",
            user_id=session["user_id"], name=quote["name"], symbol=symbol, price=quote["price"], shares=-int(shares))

            # Add the value of sold stock to the user's cash balance
            currentCash += float(quote["price"])*int(shares)
            db.execute("UPDATE users SET cash=:cash WHERE id=:user_id", cash=currentCash, user_id=session["user_id"])

            return redirect("/")

    #User reached route via GET, display form to request stock quote
    else:
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
