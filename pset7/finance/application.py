from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    purchases = db.execute("select * from purchase where user_id=:userid and quantity>0", userid=session["user_id"])
    if purchases != None and len(purchases) > 0:
        stocks = []
        stock_total = 0
        for purchase in purchases:
            quote = lookup(purchase["symbol"])
            stocks.append(Stock(quote["name"], purchase["symbol"], purchase["quantity"], quote["price"]))
            stock_total = stock_total + (quote["price"] * purchase["quantity"])

        user_details = db.execute("select cash from users where id=:user_id ", user_id=session["user_id"])
        grand_total = stock_total+ (float)(user_details[0]["cash"])
        model = IndexViewModel(stocks, grand_total, user_details[0]["cash"])
        return render_template("homepage.html", model=model)

    else:
        return render_template("error.html",message="You current do not have any stocks.")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol name")
        if not request.form.get("quantity"):
            return apology("must provide quantity")
        try:
            quantity = (int)(request.form.get("quantity"))
        except ValueError:
            return apology("quantity should be a numeric value")
        if quantity <= 0:
            return apology("quantity should be a positive numeric value")

        symbol = (request.form.get("symbol")).upper()
        quote = lookup(symbol)
        if quote != None:
            quoteprice = quote["price"];
            row = db.execute("SELECT * FROM users WHERE id = :userid", userid=session["user_id"])
            if row != None:
                if ((quoteprice*quantity) > row[0]["cash"]):
                    return apology("Sorry, you don't have enought cash");
                else:
                    db.execute("insert into history(user_id,symbol,purchase_price,quantity,purchase_time,hold_flag) values(:user_id, :symbol, :purchase_price, :quantity, :purchase_time, :hold_flag)", user_id=session["user_id"],symbol=symbol,purchase_price=quoteprice,quantity=quantity,purchase_time=datetime.now(),hold_flag=1)
                    db.execute("update users set cash = cash - :purchase_price where id = :user_id", purchase_price=((float)(quoteprice*quantity)), user_id=session["user_id"])

                    hasStock = db.execute("select * from purchase where user_id=:user_id and symbol=:symbol", user_id=session["user_id"], symbol=symbol)
                    if len(hasStock)==0:
                        db.execute("insert into purchase(user_id,symbol,quantity,last_update_datetime) values(:user_id, :symbol, :quantity, :last_update_datetime)", user_id=session["user_id"], symbol=symbol, quantity=quantity, last_update_datetime=datetime.now())
                    else:
                        db.execute("update purchase set quantity = quantity + :quantity, last_update_datetime=:update_datetime where user_id=:user_id and symbol=:symbol", quantity=quantity, user_id=session["user_id"], update_datetime=datetime.now(),symbol=symbol)

                    return redirect(url_for("index"))

            else:
                return apology("Unable to retrieve user details")
        else:
            return apology("entered symbol not found")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    historyData = db.execute("select * from history where user_id=:user_id",user_id=session["user_id"])
    if historyData == None or len(historyData) <= 0:
        return apology("You haven't made any transaction yet")
    else:
        return render_template("history.html", history=historyData)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock's symbol")
        quote = lookup((request.form.get("symbol")).upper())
        if quote != None:
            return render_template("quoted.html", name=str(quote["name"]), price=str(quote["price"]), symbol=str(quote["symbol"]))
        else:
            return apology("entered symbol not found")
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        if not request.form.get("confirmPassword"):
            return apology("must provide confirm password")

        if request.form.get("confirmPassword") != request.form.get("password"):
            return apology("password and confirm password should match")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1:
            db.execute("insert into users(username, hash) values(:username, :password)", username=request.form.get("username"), password=pwd_context.hash(request.form.get("password")))
        else:
            return apology("user with same username already registered")

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol name")
        if not request.form.get("quantity"):
            return apology("must provide quantity")
        try:
            quantity = (int)(request.form.get("quantity"))
        except ValueError:
            return apology("quantity should be a numeric value")
        if quantity <= 0:
            return apology("quantity should be a positive numeric value")

        symbol = (request.form.get("symbol")).upper()
        quote = lookup(symbol)
        if quote != None:
            quoteprice = quote["price"];
            purchase_details = db.execute("SELECT * FROM purchase WHERE symbol=:symbol and user_id=:userid", symbol=symbol, userid=session["user_id"])
            if purchase_details != None:
                if ((int)(purchase_details[0]["quantity"]) < quantity):
                    return apology("Sorry, you don't have enought stocks");
                else:
                    db.execute("insert into history(user_id,symbol,purchase_price,quantity,purchase_time,hold_flag) values(:user_id, :symbol, :purchase_price, :quantity, :purchase_time, :hold_flag)", user_id=session["user_id"],symbol=symbol,purchase_price=quoteprice,quantity=quantity,purchase_time=datetime.now(),hold_flag=0)
                    db.execute("update users set cash = cash + :selling_price where id = :user_id", selling_price=((float)(quoteprice*quantity)), user_id=session["user_id"])
                    db.execute("update purchase set quantity = quantity - :quantity, last_update_datetime=:update_datetime where user_id=:user_id and symbol=:symbol", quantity=quantity, user_id=session["user_id"], update_datetime=datetime.now(), symbol=symbol)
                    return redirect(url_for("index"))

            else:
                return apology("Unable to retrieve user details")
        else:
            return apology("entered symbol not found")

    else:
        return render_template("sell.html")


@app.route("/changepassword", methods=["GET","POST"])
@login_required
def changepassword():
    """Change Password"""
    if request.method == "POST":

        if not request.form.get("currentpassword"):
            return apology("must provide password")

        # ensure password was submitted
        elif not request.form.get("newpassword"):
            return apology("must provide new password")

        if not request.form.get("confirmpassword"):
            return apology("must provide confirm password")

        if request.form.get("confirmpassword") != request.form.get("newpassword"):
            return apology("password and confirm password should match")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        if len(rows) == 1 or pwd_context.verify(request.form.get("currentpassword"), rows[0]["hash"]):
            db.execute("update users set hash=:password where id=:user_id", password=pwd_context.hash(request.form.get("newpassword")), user_id=session["user_id"])
            # Logout user and redirect to home page
            return redirect(url_for("logout"))

        else:
            return apology("Unexpected error occured")

    else:
        return render_template("changepassword.html")