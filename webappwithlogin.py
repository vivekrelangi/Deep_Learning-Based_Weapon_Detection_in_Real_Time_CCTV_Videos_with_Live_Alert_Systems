from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import bcrypt
from wepdet import WD,WD1

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/WepDet"
app.config['SECRET_KEY'] = "giveastrongsecretkey"

mongo = PyMongo(app)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def is_valid(username, password):
        user = mongo.db.users.find_one({"username": username})
        if user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password']) == user['password']:
                session['username'] = request.form['username']
                return True
        #if user and user["password"] == password:
            #return True
        return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.is_valid(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password. If you are a new user then Sign Up")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username' : request.form['username'], 'password' : hashpass, 'email':request.form['email']})
            
            return redirect(url_for('login'))
        
        return 'That username already exists go back to login page!'

    return render_template('register.html')

@app.route("/", methods=["GET","POST"])
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    #from wepdet import value
    #WD(0)
    return render_template("home.html", username=session["username"])

@app.route("/livedet", methods=["GET","POST"])
def livedet():
    if "username" not in session:
        return redirect(url_for("login"))
    #from wepdet import value
    uname=session["username"]
    user = mongo.db.users.find_one({"username": uname})
    m=user["email"]
    #print(m)
    WD(0,m)
    print("Weapon Detection done")
    return render_template("home.html", username=session["username"])

@app.route("/offlinedet", methods=["GET","POST"])
def offlinedet():
    if "username" not in session:
        return redirect(url_for("login"))
    #from wepdet import value
    uname=session["username"]
    user = mongo.db.users.find_one({"username": uname})
    m=user["email"]
    if request.form['filepath'] != "":
        pt=request.form['filepath']
        WD1(pt,m)
    
    return render_template("home.html", username=session["username"])

if __name__ == "__main__":
    app.run(debug=True)