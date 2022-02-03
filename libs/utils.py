import random

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


