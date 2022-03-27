import smtplib, ssl
import random
import json
import glob
import os

def gen_and_send(email):

    verif_code = "".join([str(random.randint(0,9)) for i in range(6)])

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "bot.pyctf@gmail.com"
    receiver_email = f"{email}"
    password = ""
    message = f"""\
    Subject: PyCTF verification

    Here is your verification code :{verif_code}"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return verif_code



def create_or_check():
    if not "./var/verified.json" in glob.glob("./var/*"):
        dico_json = {}
    else:
        with open("./var/verified.json","r") as file:
            dico_json = json.load(file)
    for i in glob.glob("./users/*"):
        if os.path.isfile(i):
            email = ".".join(i.split("/")[-1].split(".")[:-1])
            if email not in dico_json.keys():
                dico_json[email]=False
    with open("./var/verified.json","w") as file:
        json.dump(dico_json,file)

def is_verified(email):
    with open("./var/verified.json","r") as file:
        dico_json = json.load(file)
    if email in dico_json.keys():
        return dico_json[email]
    else:
        return False

def set_as_verified(email):
    with open("./var/verified.json","r") as file:
        dico_json = json.load(file)
    dico_json[email]=True
    with open("./var/verified.json","w") as file:
        json.dump(dico_json,file)
    
