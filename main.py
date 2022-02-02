from flask import Flask, request, render_template, redirect, send_from_directory, make_response
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login/')
def my_form():
    return render_template("login.html")

#app.logger.disabled = True
app.run(port=80,threaded=True,host="0.0.0.0")