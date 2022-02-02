from flask import Flask, request, render_template, redirect, send_from_directory, make_response
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login/', methods=["POST","GET"])
def my_form():
    if request.method=="POST":
        email = request.values.get("email")
        password = request.values.get("password")
        print("ok")

    else:
        return render_template("login.html")

@app.route('/register/', methods=["POST","GET"])
def register():
    pass

#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")