from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tervetuloa sovellukseen!"

@app.route("/page1")
def page1():
    return "Ensimmäinen sivu"

@app.route("/page2")
def page2():
    return "Toinen sivu"