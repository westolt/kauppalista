import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import shopping_lists

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    if 'username' not in session:
        return render_template("index.html")
    
    user_id = session.get('user_id')
    
    own_shopping_lists = shopping_lists.get_lists(user_id)
    return render_template('index.html', own_shopping_lists=own_shopping_lists)

@app.route("/new_shopping_list", methods=['POST'])
def new_shopping_list():
    if 'user_id' not in session:
        return redirect("/login")
    
    name = request.form['name']
    creator_id = session['user_id']
    password = request.form["password"]
    
    password_hash = generate_password_hash(password)

    shopping_lists.create_list(name, password_hash, creator_id)
        
    return redirect("/")

@app.route('/join_shopping_list', methods=['POST'])
def join_shopping_list():
    shopping_list_id = request.form['shopping_list_id']
    password = request.form['password']
    user_id = session['user_id']

    sql = "SELECT password FROM shopping_list WHERE id = ?"
    result = db.query(sql, [shopping_list_id])
    
    if not result:
        return "VIRHE: kauppalistaa ei löydy", 401
    
    password_hash = result[0][0]
    
    if check_password_hash(password_hash, password):
        try:
            db.execute("INSERT INTO shopping_list_user (shopping_list_id, user_id) VALUES (?, ?)", 
                      (shopping_list_id, user_id))
            return redirect("/")
        except sqlite3.IntegrityError:
            return "VIRHE: olet jo liittynyt tähän kauppalistaan"
    else:
        return "VIRHE: väärä salasana", 401

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")