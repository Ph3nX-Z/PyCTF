from flask import Flask, request, render_template, redirect, send_from_directory, make_response
from webob import second
from libs.users import *
from libs.utils import *
import time
import datetime

global start_time 
start_time = time.time()

app = Flask(__name__)
@app.route('/')
def index():
    global start_time
    seconds = int(time.time()) - start_time
    minutes = seconds//60
    hours = seconds//3600
    return render_template("index.html",hour=int(hours),minute=int(minutes))

@app.route('/login/', methods=["POST","GET"])
def my_form():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        user = User()
        if user.check_pass(password,email):
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(hours=1)
            res = make_response(redirect("/user", code=302))
            res.set_cookie('user', generate_cookie(40,email), expires=expire_date)
            return res
        else:
            return redirect("/register/", code=302)

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
        return redirect("/login/", code=302)

    else:
        return render_template("register.html")


@app.route('/user/')
def user():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            user = get_email_cookie(request.cookies.get("user"))
            return user
    return redirect("/login/", code=302)

#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")