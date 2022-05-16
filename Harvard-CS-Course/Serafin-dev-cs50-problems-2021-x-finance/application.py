import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    cols = ["Symbol","Name", "Shares", "Price", "Total"]
    rows = db.execute("SELECT * FROM holdings WHERE user_id = ?", user_id)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    table = {}
    totals = 0
    for row in rows:
        symbol = row["symbol"]
        shares = row["shares"]
        company_name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        total = shares * price
        totals = totals + total
        table[symbol] = [company_name, shares, price, total]
    
    
    return render_template("index.html", cols=cols, cash=cash, table=table, liquidity=cash+totals)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    # user id
    user_id = session["user_id"]

    #GET
    if request.method == "GET":
        return render_template("buy.html")

    #POST
    if request.method == "POST":

        #INPUT
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        # Check if user entered all inputs
        if not symbol or not shares:
           return apology("All fields are necessary.")

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)
        
        # Check if shares are a positive number
        if not int(shares) > 0:
            return apology("You must enter a value greater than 0")

        # Check if symbol exists
        if lookup(symbol) == None:
            return apology("Symbol does not exist. Try another one.", 400)

        # check if user has enough cash
        shares = int(shares)
        share_price = lookup(symbol)["price"]
        outcome = shares * share_price
        balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        
        if not balance >= outcome:
            return apology("Not enough cash available.")

        # Update balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance - outcome, user_id)

        # REGISTER new transaction
        db.execute("INSERT INTO transactions (user_id, sym, shares, price, transacted) VALUES(?, ?, ?, ?, CURRENT_TIMESTAMP)",
        user_id, symbol, shares, share_price)

        #if user do not have that stock, add it to his holdings. Otherwise, UPDATE shares amount
        holding_sym = db.execute("SELECT symbol FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol)
        if not holding_sym:
            db.execute("INSERT INTO holdings (user_id, symbol, shares) VALUES(?, ?, ?)", user_id, symbol, shares)
        else:
            user_shares = db.execute("SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["shares"]
            db.execute("UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?", user_shares + shares, user_id, symbol)


        # msg Flashing: BOUGHT alert
        flash("Bought!" ,category="message")

        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    cols = ["Symbol", "Shares", "Price", "Transacted"]
    registers = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY transacted DESC", user_id)
    return render_template("history.html", cols=cols, registers=registers)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        n = request.form.get("username")
        p = request.form.get("password")
        # Ensure username was submitted
        if not n:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not p:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", n.upper())

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
    
    # POST
    if request.method == "POST":

        #Look up the stock Symbol by calling the Lookup function and display the results
        sym = request.form.get("symbol")
        
        #If the symbol is empty, or lookup returns None, the symbol is invalid.
        if not sym:
            return apology("You must provide a symbol to look up to")
        
        # check if symbol exists
        quote = lookup(sym.upper())
        if quote == None:
            return apology("The symbol does not exist")
        
        price = quote["price"]
        return render_template("quoted.html", quote=quote, price=price)
        
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    #POST
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if any input is blank
        if not username or not password or not confirmation:
            return apology("All fields are required")

        # if if username already exist
        user = db.execute("SELECT UPPER(username) FROM users WHERE username = ?", username.upper())
        if user:
            return apology("That username already exists.")

        # check if passwords do not match
        if not confirmation == password:
            return apology("Confirmation and password do not match")


        # Create new user
        id = db.execute("INSERT INTO users (username,hash) VALUES (?, ?)",
        username.upper(), generate_password_hash(password))

        #set session id for new user
        session["user_id"] = id

        #check if new user was succesfully created
        row = db.execute("SELECT * FROM users WHERE id IN (?)", id)
        if not row:
            return apology("Something went wrong during registration. Try again please.")

        #send registered mssg
        flash("Registered!", category="message")

        return redirect("/")

    #GET
    if request.method == "GET":
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    #GET
    if request.method == "GET":
        symbols = db.execute("SELECT sym FROM transactions WHERE user_id = ? GROUP BY sym HAVING sum(shares) > 0 ORDER BY sym ASC", user_id)
        return render_template("sell.html", symbols=symbols)

    #POST
    if request.method == "POST":

        # input
        sym = request.form.get("symbol")
        shares = request.form.get("shares")
        shares = int(shares)

        # Check if the user failed to select a symbol and if shares value has been entered correctly
        if not sym:
            return apology("No symbol specified")
        if not shares:
            return apology("No shares specified")
        if shares < 1:
            return apology("Please, enter an amount bigger than 0.")

        # Check if there are enough shares for the transaction
        #user_shares = db.execute("SELECT shares FROM transactions WHERE sym = ? GROUP BY sym HAVING SUM(shares)", sym)[0]["shares"]
        user_shares = db.execute("SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, sym)[0]["shares"]
        if user_shares and user_shares < shares:
            return apology("You do not have that amount of shares")

        # update user shares
        actual_shares = user_shares - shares
        db.execute("UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?", actual_shares, user_id, sym)
        
        #if symbol shares are = 0 DELETE ROW 
        if actual_shares == 0:
            db.execute("DELETE FROM holdings WHERE user_id = ? AND symbol = ?", user_id, sym)
 
        # Update user balance
        share_price = lookup(sym)["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        income = share_price * shares
        new_balance = user_cash + income

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, user_id)

        #insert transaction
        #stock’s symbol, the (purchase or sale) price, the number of shares bought or sold, and the date and time at which the transaction occurred
        db.execute(
            "INSERT INTO transactions (user_id, sym, shares, price, transacted) VALUES(?, ?, ?, ?, CURRENT_TIMESTAMP)", user_id, sym, shares*-1, share_price)

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
