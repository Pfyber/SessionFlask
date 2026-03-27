from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB, Query
# pip install flask, tinydb

app = Flask(__name__)
app.secret_key = "skrivamoTaKljuč"

db = TinyDB("db.json")
users = db.table("users")

User = Query()

#home
@app.route("/")
def home():
    if "user" in session:
        redirect("/dashboard")
    return redirect("/login")
#register
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #print(username, password)

        if users.search(User.username == username):
            return "Uporabnik obstaja"
        
        users.insert({"username" : username, "password": password, "note": ""})
        return redirect("/login")

    return render_template("register.html")
#login
#dashboard
#save_note
#logout

app.run(debug = True)