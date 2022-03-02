from flask import Flask, request, render_template, redirect, send_from_directory, make_response
from webob import second
from libs.users import *
from libs.utils import *
from libs.docker import *
from libs.graphs import *
import time
import datetime

global start_time 
start_time = time.time()

try:
    create_docker_network()
except:
    pass

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

@app.route('/instances/', methods=["POST","GET"])
def instances():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            if request.method=="GET":
                email = get_email_cookie(request.cookies.get("user"))
                try:
                    with open("./instances/instances.all") as file:
                        liste_active_instances = []
                        for i in file.read().split("\n"):
                            if email in i:
                                liste_active_instances.append(i.split("-")[1])
                    try:
                        ip = get_ip_by_id(liste_active_instances[0])
                    except:
                        ip=None
                    return render_template("instances.html",instances=liste_active_instances,ip=ip)
                except:
                    return redirect("/home/", code=302)
            else:
                if "delete_instance" in request.form:
                    delete_container(get_id_by_image(request.form.get('delete_instance')),request.form.get('delete_instance'))
                    return redirect("/instances/", code=302)
                name = request.form.get("auto")
                email = get_email_cookie(request.cookies.get("user"))
                if deploy_instance_user(name,email):
                    return redirect("/instances/", code=302)
                else:
                    return redirect("/instances/", code=302)
    return redirect("/login/", code=302)

@app.route("/submit/", methods=["POST","GET"])
def submit():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            if request.method=="GET":
                user = User()
                email = get_email_cookie(request.cookies.get("user"))
                user.import_user(email)
                points = user.points
                cat = get_cat_for_email(email)
                generate_graph(cat, email)
                with open("./var/challs.txt","r") as file:
                    challs = file.read().split("\n")
                challs = [f"{i.split('-')[0]} {i.split('-')[1]} {i.split('-')[3]}" for i in challs]
                return render_template("submit_flag.html",challs_with_number = challs, points=points,email=email)
            else:
                email = get_email_cookie(request.cookies.get("user"))
                id = request.values.get("id")
                flag = request.values.get("flag")
                submit_flag(email,flag,id)
                refresh_points(email)
                return redirect("/submit/", code=302)
    return redirect("/login/", code=302)

@app.route("/logout/")
def logout():
    resp = make_response(redirect("/", code=302))
    resp.delete_cookie('user')
    return resp

#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")
execute_cmd("docker system prune -a")