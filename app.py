import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import shopping_lists
import list_users

app = Flask(__name__)
app.secret_key = config.secret_key

# Render the front page
@app.route("/")
def index():
    if "username" not in session:
        return render_template("index.html")

    user_id = session.get("user_id")
    own_shopping_lists = shopping_lists.get_lists(user_id)
    return render_template("index.html", own_shopping_lists=own_shopping_lists)

# Show user
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = list_users.get_user(user_id)
    shopping_list_id = request.args.get("shopping_list_id")
    shopping_list = shopping_lists.get_list(shopping_list_id)
    purchased_items = list_users.purchased_items_by_user(user_id, shopping_list_id)
    total_price = list_users.total(user_id, shopping_list_id)

    return render_template("show_user.html", user=user, shopping_list=shopping_list, shopping_list_id=shopping_list_id, purchased_items=purchased_items, total_price=total_price)

# Buy item from shopping list
@app.route("/shopping_list/<int:shopping_list_id>/buy_item/<int:item_id>", methods=["GET", "POST"])
def buy_item(shopping_list_id, item_id):
    if request.method == "POST":
        price = request.form["price"]
        buyer = request.form["purchased_by_user_id"]
        shopping_lists.buy_item(price, buyer, item_id, shopping_list_id)
        return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))
    else:
        item = shopping_lists.get_item(item_id, shopping_list_id)
        users = shopping_lists.get_users(shopping_list_id)
        if item:
            return render_template("buy_item.html", item=item[0], shopping_list_id=shopping_list_id, users=users)
        else:
            return "Item not found", 404

# Edit item in shopping list
@app.route("/shopping_list/<int:shopping_list_id>/edit_item/<int:item_id>", methods=["GET", "POST"])
def edit_item(shopping_list_id, item_id):
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        shopping_lists.update_item(name, quantity, item_id, shopping_list_id)
        return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))
    else:
        item = shopping_lists.get_item(item_id, shopping_list_id)
        if item:
            return render_template("edit_item.html", item=item[0], shopping_list_id=shopping_list_id)
        else:
            return "Item not found", 404

# Remove item from shopping list
@app.route("/shopping_list/<int:shopping_list_id>/delete_item/<int:item_id>", methods=["POST"])
def delete_item(shopping_list_id, item_id):
    shopping_lists.delete_item(item_id, shopping_list_id)
    return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

# Add item to shopping list
@app.route("/shopping_list/<int:shopping_list_id>/add_item", methods=["POST"])
def add_item(shopping_list_id):
    name = request.form["name"]
    quantity = request.form["quantity"]
    shopping_lists.add_item_to_list(name, quantity, shopping_list_id)
    return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

# Leave shopping list
@app.route("/leave_shopping_list", methods=["POST"])
def leave_shopping_list():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    shopping_list_id = request.form.get("shopping_list_id")
    shopping_lists.remove_user_from_list(user_id, shopping_list_id)
    return redirect("/")

# View shopping list
@app.route("/shopping_list/<int:shopping_list_id>")
def show_shopping_list(shopping_list_id):
    shopping_list = shopping_lists.get_list(shopping_list_id)
    items = shopping_lists.get_items(shopping_list_id)
    shopping_list_users = shopping_lists.get_users(shopping_list_id)

    return render_template("show_shopping_list.html", shopping_list=shopping_list, items=items, shopping_list_users=shopping_list_users)


# Create a new shopping list
@app.route("/new_shopping_list", methods=["POST"])
def new_shopping_list():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    password = request.form["password"]
    user_id = session["user_id"]
    password_hash = generate_password_hash(password)

    shopping_lists.create_list(name, password_hash, user_id)

    return redirect("/")

# Join another user's list
@app.route("/join_shopping_list", methods=["POST"])
def join_shopping_list():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    password = request.form["password"]
    user_id = session["user_id"]

    result = shopping_lists.get_list_by_name(name)

    if not result:
        return redirect(url_for("error", message="Kauppalistaa ei löydy"))

    shopping_list_id = result[0][0]
    password_hash = result[0][1]

    if check_password_hash(password_hash, password):
        try:
            shopping_lists.join_list(shopping_list_id, user_id)
            return redirect("/")
        except sqlite3.IntegrityError:
            return redirect(url_for("error", message="Olet jo liittynyt tähän kauppalistaan"))
    else:
        return redirect(url_for("error", message="Väärä salasana"))

# Redirect to registration page
@app.route("/register")
def register():
    return render_template("register.html")

# Create a new user
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return redirect(url_for("error", message="Salasanat eivät ole samat"))
    password_hash = generate_password_hash(password1)

    try:
        shopping_lists.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return redirect(url_for("error", message="Tunnus on jo varattu"))

    return redirect(url_for("account_created"))

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html") 

    username = request.form.get("username")
    password = request.form.get("password")

    result = shopping_lists.log_in(username)

    if not result:
        return redirect(url_for("error", message="Väärä tunnus tai salasana"))

    user_id, password_hash = result[0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return redirect(url_for("error", message="Väärä tunnus tai salasana"))

# Logout
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# Account created message
@app.route("/account_created")
def account_created():
    return render_template("account_created.html")

# Error message
@app.route("/error")
def error():
    message = request.args.get("message", "Tuntematon virhe")
    return render_template("error.html", message=message)