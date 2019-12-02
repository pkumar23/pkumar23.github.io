#TODO Get custom domain name using Github Student Pack https://www.name.com/partner/github-students
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
        username=request.form.get("username") # search for friend's username
        
        # Ensure username is entered
        if not username:
            return apology("must provide username", 403)
        else:          
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=username)
        # Ensure username exists before following friend
        if len(rows) != 1:
            return apology("invalid username , 403)
        else:
            #TODO update queries to establish follower/followee relationship
                           
        return redirect("/friends")

    else:
        # query to get your friends and their current locations
        return render_template("friends.html", rows=rows)



@app.route("/login", methods=["GET", "POST"]) # ?do we still need this if using Harvard authentication?
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



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
