import random
from users import *

global all_cookies 
all_cookies = {}

def generate_cookie(lenght,email):
    global all_cookies
    data = [i for i in "azertyuiopqsdfghjklmwxcvbn£µ%M/.!:;,*p@1234567890"]
    cookie = "".join([data[random.randint(0,len(data)-1)] for _ in range(lenght)])[::-1]
    all_cookies[cookie]=email
    return cookie

def get_email_cookie(cookie):
    global all_cookies
    if cookie in all_cookies.keys():
        if all_cookies[cookie]:
            return all_cookies[cookie]
    return False

def create_files():
    with open("./var/challs.txt","w") as file, open("./var/resolve.txt","w") as file2 :
        file.write("")
        file2.write("")

def get_cat(chall_id):
    with open("./var/challs.txt","r") as file:
        for i in file.read().split("\n"):
            if chall_id in i.split("-"):
                return i.split("-")[2] # challid - nom - cat - flag
    return "None"

def get_cat_for_email(email):
    with open("./var/challs.txt",'r') as file:
        challs = file.read().split("\n")
    with open("./var/resolve.txt","r") as file:
        resolves = file.read().split("\n") # challid - nom - email - flag - cat
    user_res = []
    cat = {}
    for i in resolves:
        if email in i:
            user_res.append(i)
    l_keep = []
    for resolution_attempts in user_res:
        resolution_attempts = resolution_attempts.split("-")
        if f"{resolution_attempts[0]}-{resolution_attempts[1]}-{resolution_attempts[4]}-{resolution_attempts[3]}" in challs and f"{resolution_attempts[0]}-{resolution_attempts[1]}-{resolution_attempts[4]}-{resolution_attempts[3]}" not in l_keep:
            if resolution_attempts[4] not in cat:
                cat[resolution_attempts[4]] = 1
            else:
                cat[resolution_attempts[4]] += 1
        l_keep.append(f"{resolution_attempts[0]}-{resolution_attempts[1]}-{resolution_attempts[4]}-{resolution_attempts[3]}")
    return cat

def get_name(chall_id):
    with open("./var/challs.txt",'r') as file:
        for i in file.read().split("\n"):
            if chall_id in i:
                return i.split("-")[1]

def submit_flag(email,flag,chall_id):
    nom = get_name(chall_id)
    with open("./var/resolve.txt","a") as file:
        file.write(f"{chall_id}-{nom}-{email}-{flag}-{get_cat(chall_id)}\n") 

def refresh_points(email):
    user1 = User()
    try:
        user1.import_user(email)
    except:
        return "Failed"
    list_of_cat = get_cat_for_email(email)
    sum_of_points = sum(list_of_cat.values())
    user1.points = str(sum_of_points*10)
    user1.update_user()
    return "Done"



if __name__=="__main__":
    #create_files()
    submit_flag("a@a.a","flag1","1")
    submit_flag("b@b.b","flag1","1")
    submit_flag("b@b.b","flag2","2")
    submit_flag("b@b.b","flag2","2")
    submit_flag("b@b.b","flag2","2")
    submit_flag("b@b.b","flag3","3")
    submit_flag("a@a.a","flag3","3")
    submit_flag("a@a.a","flag3","3")
    submit_flag("a@a.a","flag4","4")
    submit_flag("a@a.a","flag5","5")
    submit_flag("a@a.a","flag5","6")
    submit_flag("a@a.a","flag5","7")
    submit_flag("a@a.a","flag5","8")
    submit_flag("a@a.a","flag5","9")
    print(get_cat_for_email("b@b.b"))
    refresh_points("b@b.b")
    
