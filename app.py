from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = "karkoliToleJeSkrivnost123"

db = TinyDB("db.json")
users = db.table("users")

User = Query()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #print(username, password)
        if users.search(User.username == username):
            return redirect("/register")
        else:
            users.insert({"username" : username, "password": password, "note" : ""})
            return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(User.username == username )
        #print(user)
        if user and user["password"] == password:
            session["user"] = username
            return redirect("/dashboard")


    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    user = users.get(User.username == session["user"] )
    return render_template("dashboard.html", user = session["user"], text = user["note"])

# shrani note
@app.route("/saveNote", methods = ["POST"])
def saveNote():
    note = request.form["text"]
    users.update({"note": note}, User.username == session["user"] )

    return "SAVED"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
app.run(debug=True)