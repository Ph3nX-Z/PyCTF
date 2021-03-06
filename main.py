from flask import Flask, request, render_template, redirect, send_from_directory, make_response, send_file
from libs.users import *
from libs.utils import *
from libs.docker import *
from libs.graphs import *
from libs.verification import *
import time
import datetime
import glob

global start_time 
start_time = time.time()

global user_deploy
user_deploy = {}

global code_ip
code_ip = {}

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
    minutes-=hours*60
    return render_template("index.html",hour=int(hours),minute=int(minutes))

@app.route('/login/', methods=["POST","GET"])
def my_form():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        user = User()
        if request.remote_addr not in get_ip_banned():
            if user.check_pass(password,email):
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(hours=1)
                res = make_response(redirect("/user", code=302))
                res.set_cookie('user', generate_cookie(40,email), expires=expire_date)
                return res
            else:
                return redirect("/login/", code=302)
        else:
            return render_template("banned.html")
    else:
        if request.cookies.get("user"):
            if get_email_cookie(request.cookies.get("user")):
                user = User()
                email = get_email_cookie(request.cookies.get("user"))
                if f"./users/{email}.xml" in glob.glob("./users/*"):
                    return redirect("/user/", code=302)
        return render_template("login.html")

@app.route('/register/', methods=["POST","GET"])
def register():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        nickname = request.values.get("nickname")

        if not email or not password or not nickname:
            return redirect("/register/",code=302)

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

@app.route('/verify/', methods=["POST","GET"])
def verify():
    global code_ip
    create_or_check()
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            if not is_verified(get_email_cookie(request.cookies.get("user"))):
                if request.method=="GET":
                    codee = gen_and_send(get_email_cookie(request.cookies.get("user")))
                    code_ip[request.remote_addr] = codee
                    return render_template("verify.html")
                else:
                    if not request.remote_addr in code_ip.keys():
                        return redirect('/verify/',code=302)
                    code_from_page = request.values.get("verify")
                    #print(codee,code_from_page)
                    if code_ip[request.remote_addr]==code_from_page:
                        set_as_verified(get_email_cookie(request.cookies.get("user")))
                    else:
                        return render_template("verify.html")

    return redirect("/user/",code=302)

@app.route('/instances/', methods=["POST","GET"])
def instances():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            if not is_verified(get_email_cookie(request.cookies.get("user"))):
                return redirect("/verify/",code=302)
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
                    return render_template("instances.html",instances=liste_active_instances,ip=ip, success="The containers may need some time to deploy (1-5 minutes), please wait and refresh the page !")
                except:
                    return redirect("/", code=302)
            else:
                email = get_email_cookie(request.cookies.get("user"))
                if "delete_instance" in request.form:
                    delete_container(get_id_by_image(request.form.get('delete_instance')),request.form.get('delete_instance'))
                    user_deploy[email]=0
                    return redirect("/instances/", code=302)
                if not email in user_deploy.keys():
                    user_deploy[email]=0
                if user_deploy[email]!=1:
                    name = request.form.get("auto")
                    user_deploy[email]=1
                    status = deploy_instance_user(name,email)
                    if status:
                        return redirect("/instances/", code=302)
                    else:
                        user_deploy[email]=0
                        return redirect("/instances/", code=302)
                else:
                    return redirect("/instances/", code=302)
    return redirect("/login/", code=302)

@app.route("/user/", methods=["POST","GET"])
def submit():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            if not is_verified(get_email_cookie(request.cookies.get("user"))):
                return redirect("/verify/",code=302)
            if request.method=="GET":
                user = User()
                email = get_email_cookie(request.cookies.get("user"))
                user.import_user(email)
                points = user.points
                cat = get_cat_for_email(email)
                challs_done = get_challs_for_email(email)
                main_graph(cat, email)
                liste_chall = {}
                with open("./var/challs.txt","r") as file:
                    challs = file.read().split("\n")
                for i in challs:
                    if i!="":
                        i=i.split("-")
                        liste_chall[i[0]] = [i[1],i[2]]
                
                rank_points = {"B0t":0,"N00b1e":40,"W1z4rd":60,"M4st3r":100,"Bug Hunt3r":150,"H4x0r":200}
                for i in range(len(list(rank_points.values())[::-1])):
                    if int(points) >= int(list(rank_points.values())[::-1][i]):
                        rank = str(list(rank_points.keys())[::-1][i])
                        break

                return render_template("submit_flag.html",points=points,email=email,liste_chall = liste_chall,challs_done=", ".join(challs_done),rank=rank)
            else:
                email = get_email_cookie(request.cookies.get("user"))
                id = request.values.get("id")
                flag = request.values.get("flag")
                submit_flag(email,flag,id)
                refresh_points(email)
                return redirect("/user/", code=302)
    return redirect("/login/", code=302)

@app.route("/logout/")
def logout():
    resp = make_response(redirect("/", code=302))
    resp.delete_cookie('user')
    return resp

@app.route("/scoreboard/")
def score():
    users = []
    for i in glob.glob("./users/*"):
        user1 = User()
        user1.import_user(".".join(i.split("/")[-1].split(".")[:-1]))
        users.append([user1.pseudo,user1.points])
    sorted = scoreboard_sort(users)
    return render_template("scoreboard.html",users=sorted,long=len(sorted))

@app.route("/admin/users/", methods=["POST","GET"])
def admin():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            users = {}
            for i in glob.glob("./users/*"):
                email = ".".join(i.split("/")[-1].split(".")[:-1])
                user = User()
                user.import_user(email)
                users[user.email]=[user.id,user.pseudo,user.right,user.points]

            if request.method=="GET":
                email = get_email_cookie(request.cookies.get("user"))
                user = User()
                user.import_user(email)
                if user.right == "admin":
                    return render_template("admin.html",users=users)
                else:
                    return redirect("/", code=302)
            elif request.method=="POST":
                email = get_email_cookie(request.cookies.get("user"))
                user = User()
                user.import_user(email)
                if user.right != "admin":
                    return redirect("/", code=302)
                email_delete = request.values.get("id")
                user1 = User()
                try:
                    user1.destroy_entry(email_delete)
                except:
                    return render_template("admin.html",users=users, error="Non-existent user !")
                return render_template("admin.html",users=users, success="Success, refresh the page to see the changes.")
    return redirect("/login/", code=302)

@app.route("/admin/banned/", methods=["POST","GET"])
def banned():
    success = ""
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            email = get_email_cookie(request.cookies.get("user"))
            user = User()
            user.import_user(email)
            if request.method == "GET":
                if user.right == "admin":
                    with open("./var/banned_ips.txt",'r') as file:
                        ips = file.read().split("\n")
                        ips = {i:ips[i] for i in range(len(ips)) if ips[i]!=""}
                    return render_template("admin-banned.html",ips=ips)
                else:
                    return redirect("/",code=302)
            elif request.method=="POST":
                if user.right == "admin":
                    ip = request.values.get("id")
                    if request.form['sub_but'] == 'Delete':
                        with open("./var/banned_ips.txt",'r') as file:
                            data = [i for i in file.read().split("\n") if i!=""]
                        with open("./var/banned_ips.txt",'w') as file:
                            try:
                                success = str(data.pop(data.index(ip)))+" Has been removed."
                            except:
                                error = "Non-existent ip !"
                            file.write("\n".join(data))
                    elif request.form['sub_but'] == 'Add':
                        with open("./var/banned_ips.txt",'r') as file:
                            data = [i for i in file.read().split("\n") if i!=""]
                            data.append(ip)
                            success = "Done !"
                        with open("./var/banned_ips.txt",'w') as file:
                            file.write("\n".join(data))
                    else:
                        error = "Invalid arguments."

                    with open("./var/banned_ips.txt",'r') as file:
                        ips = file.read().split("\n")
                        ips = {i:ips[i] for i in range(len(ips)) if ips[i]!=""}
                    if success!="":
                        return render_template("admin-banned.html",ips=ips,success=success)
                    else:
                        return render_template("admin-banned.html",ips=ips,error=error)
                else:
                    return redirect("/",code=302)
    return redirect("/login/", code=302)

@app.route("/admin/")
def admin_panel():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            email = get_email_cookie(request.cookies.get("user"))
            user = User()
            user.import_user(email)
            if user.right == "admin":
                return render_template("admin-index.html")
            else:
                return redirect("/",code=302)
    return redirect("/login/", code=302)
    

@app.route('/admin/challs/')
def challs_manag():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            email = get_email_cookie(request.cookies.get("user"))
            user = User()
            user.import_user(email)
            if user.right == "admin":
                return "challs management"
            else:
                return redirect("/",code=302)
    return redirect("/login/", code=302)

@app.route("/download_config/", methods=["POST","GET"])
def download_config():
    if request.cookies.get("user"):
        if get_email_cookie(request.cookies.get("user")):
            email = get_email_cookie(request.cookies.get("user"))
            user1 = User()
            user1.import_user(email)
            if "/root/"+str(user1.pseudo)+".ovpn" in glob.glob("/root/*.ovpn"):
                return send_file(f'/root/{str(user1.pseudo)+".ovpn"}')
    return redirect("/", code=302)




#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")
execute_cmd("docker system prune -af")