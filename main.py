from flask import Flask, request, render_template, redirect, send_from_directory, make_response
from webob import second
from libs.users import *
import time

global start_time 
start_time = time.time()

app = Flask(__name__)
@app.route('/')
def index():
    global start_time
    duration = time.time() - start_time
    minute = duration % 360
    hour = minute%60
    second = hour%60
    hour=hour//60
    minute = minute//60
    return render_template("index.html",hour=int(hour),minute=int(minute))

@app.route('/login/', methods=["POST","GET"])
def my_form():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        user = User()
        if user.check_pass(password,email):
            return "Logged in"
        else:
            return "WRONG"

    else:
        return render_template("login.html")

@app.route('/register/', methods=["POST","GET"])
def register():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        nickname = request.values.get("nickname")
        if not os.path.isdir("./var/"):
            os.mkdir("./var")
        if not os.path.isfile("./var/id"):
            with open("./var/id","w") as file:
                file.write(str(1))
            id = 1
        else:
            with open("./var/id","r") as file:
                id = int(file.read().split("\n")[0])
            with open("./var/id","w") as file:
                file.write(str(id+1))
        user = User("user",nickname,"0",str(id),email,password)
        user.hash_pass()
        try:
            user.export_user()
        except ValueError:
            return render_template("register.html",status="User already exists !")
        return render_template("register.html",status="Done !")

    else:
        return render_template("register.html")

#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")