import re
import sqlite3
import secrets
from flask import Flask, redirect, render_template, request, session, url_for, abort, flash
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import shopping_lists
import list_users

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

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
    if "user_id" not in session:
        abort(401)

    shopping_list_id = request.args.get("shopping_list_id")
    if not shopping_list_id:
        abort(404)

    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)

    if not shopping_lists.has_user_access(shopping_list_id, user_id):
        abort(403)

    user = list_users.get_user(user_id)
    if not user:
        abort(404)

    shopping_list = shopping_lists.get_list(shopping_list_id)
    purchased_items = list_users.purchased_items_by_user(user_id, shopping_list_id)
    total_price = list_users.total(user_id, shopping_list_id)

    overall_total_price = None
    users_count = shopping_lists.get_users_count(shopping_list_id)
    if users_count > 1:
        overall_total_price = list_users.overall_total(shopping_list_id)

    return render_template(
        "show_user.html",
        user=user,
        shopping_list=shopping_list,
        shopping_list_id=shopping_list_id,
        purchased_items=purchased_items,
        total_price=total_price,
        overall_total_price=overall_total_price
    )

# Buy item from shopping list
@app.route("/shopping_list/<int:shopping_list_id>/buy_item/<int:item_id>",
           methods=["GET", "POST"])
def buy_item(shopping_list_id, item_id):
    if "user_id" not in session:
        abort(401)
    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)

    if request.method == "POST":
        check_csrf()
        price = request.form["price"]
        buyer = request.form["purchased_by_user_id"]

        if (not re.match(r'^\d{1,5}(\.\d{1,2})?$', price) or
                float(price) < 0 or float(price) > 10000):
            flash("Anna kelvollinen hinta väliltä 0 - 10000, enintään kaksi desimaalia.")
            return redirect(url_for("buy_item", shopping_list_id=shopping_list_id,
                                  item_id=item_id))

        shopping_lists.buy_item(price, buyer, item_id, shopping_list_id)
        return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

    item = shopping_lists.get_item(item_id, shopping_list_id)
    users = shopping_lists.get_users(shopping_list_id)
    if not item:
        abort(404)
    return render_template(
        "buy_item.html",
        item=item[0],
        shopping_list_id=shopping_list_id,
        users=users
    )

@app.route("/shopping_list/<int:shopping_list_id>/edit_item/<int:item_id>",
           methods=["GET", "POST"])
def edit_item(shopping_list_id, item_id):
    if "user_id" not in session:
        abort(401)

    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)

    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        quantity = request.form["quantity"]
        category_id = request.form["category_id"]

        if not name or len(name) > 20 or not quantity or len(quantity) > 10:
            abort(403)

        shopping_lists.update_item(name, quantity, item_id, category_id, shopping_list_id)
        return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

    item = shopping_lists.get_item(item_id, shopping_list_id)
    if not item:
        abort(404)
    return render_template("edit_item.html", item=item[0], shopping_list_id=shopping_list_id)

# Remove item from shopping list
@app.route("/shopping_list/<int:shopping_list_id>/delete_item/<int:item_id>",
           methods=["POST"])
def delete_item(shopping_list_id, item_id):
    check_csrf()
    if "user_id" not in session:
        abort(401)
    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)
    shopping_lists.delete_item(item_id, shopping_list_id)
    return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

# Add item to shopping list
@app.route("/shopping_list/<int:shopping_list_id>/add_item", methods=["POST"])
def add_item(shopping_list_id):
    check_csrf()
    name = request.form["name"]
    quantity = request.form["quantity"]
    category_id = request.form["category_id"]

    if not name or len(name) > 20 or not quantity or len(quantity) > 10:
        abort(403)

    shopping_lists.add_item_to_list(name, quantity, category_id, shopping_list_id)
    return redirect(url_for("show_shopping_list", shopping_list_id=shopping_list_id))

# Leave shopping list
@app.route("/leave_shopping_list", methods=["POST"])
def leave_shopping_list():
    check_csrf()
    if "user_id" not in session:
        abort(401)

    shopping_list_id = request.form.get("shopping_list_id")
    if not shopping_list_id:
        abort(401)

    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)

    users_count = shopping_lists.get_users_count(shopping_list_id)
    confirm_delete = request.form.get("confirm_delete") == "true"

    if users_count == 1 and not confirm_delete:
        shopping_list = shopping_lists.get_list(shopping_list_id)
        return render_template("confirm_leave_last.html",
                            shopping_list=shopping_list,
                            shopping_list_id=shopping_list_id)

    shopping_lists.remove_user_from_list(session["user_id"], shopping_list_id)

    if users_count == 1 and confirm_delete:
        shopping_lists.delete_entire_list(shopping_list_id)
        return redirect("/")

    return redirect("/")

# View shopping list
@app.route("/shopping_list/<int:shopping_list_id>")
def show_shopping_list(shopping_list_id):
    if "user_id" not in session:
        abort(401)

    shopping_list = shopping_lists.get_list(shopping_list_id)
    if not shopping_lists.has_user_access(shopping_list_id, session["user_id"]):
        abort(403)

    items = shopping_lists.get_items(shopping_list_id)
    shopping_list_users = shopping_lists.get_users(shopping_list_id)
    categories = shopping_lists.get_categories()

    category_filter = request.args.get("category_filter", "all")
    filtered_items = [
        item for item in items
        if category_filter == "all" or str(item["category_id"]) == category_filter
    ]

    return render_template(
        "show_shopping_list.html",
        shopping_list=shopping_list,
        items=items,
        filtered_items=filtered_items,
        shopping_list_users=shopping_list_users,
        categories=categories
    )

# Create a new shopping list
@app.route("/new_shopping_list", methods=["POST"])
def new_shopping_list():
    check_csrf()
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    password = request.form["password"]

    if not name or len(name) > 25 or len(password) < 3 or len(password) > 20:
        abort(403)

    user_id = session["user_id"]
    password_hash = generate_password_hash(password)

    try:
        shopping_lists.create_list(name, password_hash, user_id)
        flash("Lista luotu onnistuneesti!")
        return redirect("/")
    except sqlite3.IntegrityError:
        flash(f"Lista nimellä '{name}' on jo olemassa!")
        return redirect("/")

# Join another user's list
@app.route("/join_shopping_list", methods=["POST"])
def join_shopping_list():
    check_csrf()
    if "user_id" not in session:
        return redirect("/")

    name = request.form["name"]
    password = request.form["password"]
    user_id = session["user_id"]

    result = shopping_lists.get_list_by_name(name)
    if not result:
        flash("Kauppalistaa ei löydy")
        return redirect("/")

    shopping_list_id = result[0][0]
    password_hash = result[0][1]

    if not check_password_hash(password_hash, password):
        flash("Väärä salasana!")
        return redirect("/")

    try:
        shopping_lists.join_list(shopping_list_id, user_id)
        flash("Kauppalistaan liittyminen onnistui!")
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("Olet jo liittynyt tähän kauppalistaan!")
        return redirect("/")

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

    if not username or len(username) > 15:
        abort(403)

    if len(password1) < 3 or len(password1) > 20:
        abort(403)

    if password1 != password2:
        flash("Salasanat eivät ole samat")
        return redirect("/register")

    password_hash = generate_password_hash(password1)

    try:
        shopping_lists.create_user(username, password_hash)
        flash("Tunnukset luotu!")
        return redirect("/register")
    except sqlite3.IntegrityError:
        flash("Tunnus on jo varattu!")
        return redirect("/register")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("/")

    username = request.form.get("username")
    password = request.form.get("password")

    result = shopping_lists.log_in(username)
    if not result:
        flash("Väärä tunnus tai salasana!")
        return redirect("/")

    user_id, password_hash = result[0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        flash("Väärä tunnus tai salasana!")
        return redirect("/")

# Logout
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")