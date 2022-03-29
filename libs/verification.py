import random
import json
import glob
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def gen_and_send(email_from):

    verif_code = "".join([str(random.randint(0,9)) for i in range(6)])

    sender = "bot.pyctf@gmail.com"
    receiver = email_from
    port_number =587
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'PYCTF Verification'
    message = f'Here is your verification code :{verif_code}'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',port_number)
    mailserver.connect('smtp.gmail.com',port_number)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(sender, "") # put the code here for your smtp
    mailserver.sendmail(sender,receiver,msg.as_string())
    mailserver.quit()
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
    
