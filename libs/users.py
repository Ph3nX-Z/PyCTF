from lxml import etree
import xml.etree.ElementTree as ET
import os
import hashlib

class User:
    def __init__(self,right="",pseudo="",points="",id="",email="",password=""):
        self.right = right
        self.pseudo = pseudo
        self.points = points
        self.id = id
        self.email = email
        self.password = password
    
    def export_user(self):
        if not os.path.isdir("users"):
            os.mkdir("./users/")
        user = etree.Element("user")
        infos = etree.SubElement(user,"infos")
        infos.set("id",self.id)
        pseudo = etree.SubElement(infos,"pseudo")
        pseudo.text = self.pseudo
        points = etree.SubElement(infos,"points")
        points.text = self.points
        right = etree.SubElement(infos,"right")
        right.text = self.right
        email = etree.SubElement(infos,"email")
        email.text = self.email
        password = etree.SubElement(infos,"password")
        password.text = self.password
        if not os.path.isfile(f"./users/{self.email}.xml"):
            with open(f"./users/{self.email}.xml",'w') as file:
                file.write(etree.tostring(user,pretty_print=True).decode("utf-8"))
        else:
            raise ValueError("[-] File already exists ! User already registered !")

    def update_user(self):
        if not os.path.isdir("users"):
            os.mkdir("./users/")
        user = etree.Element("user")
        infos = etree.SubElement(user,"infos")
        infos.set("id",self.id)
        pseudo = etree.SubElement(infos,"pseudo")
        pseudo.text = self.pseudo
        points = etree.SubElement(infos,"points")
        points.text = self.points
        right = etree.SubElement(infos,"right")
        right.text = self.right
        email = etree.SubElement(infos,"email")
        email.text = self.email
        password = etree.SubElement(infos,"password")
        password.text = self.password
        if os.path.isfile(f"./users/{self.email}.xml"):
            with open(f"./users/{self.email}.xml",'w') as file:
                file.write(etree.tostring(user,pretty_print=True).decode("utf-8"))
        else:
            raise ValueError("This user does not exists")

    def import_user(self,email):
        if os.path.isdir("./users/"):
            if os.path.isfile(f"./users/{email}.xml"):
                tree = ET.parse(f"./users/{email}.xml")
                root = tree.getroot()
                values = [values.text for values in root[0]] # Get only infos keys
                self.pseudo = values[0]
                self.points = values[1]
                self.right = values[2]
                self.email = values[3]
                self.password = values[4]
                self.id = root[0].attrib["id"]
                print("[+] Imported !")
            else:
                raise ValueError("[-] This email does not have entry !")
        else:
            raise ValueError("[-] ./users/ directory does not exists !")

    def destroy_entry(self,email):
        if os.path.isfile(f"./users/{email}.xml"):
            os.remove(f"./users/{email}.xml")
        else:
            raise ValueError("[-] Email not registered !")

    def hash_pass(self):
        dk = hashlib.pbkdf2_hmac('sha256', bytes(self.password,'utf-8'), bytes(self.pseudo+self.email+self.id,"utf-8"), 100000)
        self.password = dk.hex()
        print("[+] Password Hashed !")
    
    def check_pass(self,clearpass,email):
        try:
            self.import_user(email)
        except ValueError:
            return False
        if hashlib.pbkdf2_hmac('sha256', bytes(clearpass,'utf-8'), bytes(self.pseudo+self.email+self.id,"utf-8"), 100000).hex()==self.password:
            return True
        return False
    

if __name__=="__main__":
    #user = User()
    #user.import_user("email")
    #user.hash_pass()
    #print(user.password,user.points,user.right,user.pseudo,user.id,user.email)
    user1=User("admin","Ph3nX","10000","0","email","motdepasse")
    user1.destroy_entry("email")
    user1.hash_pass()
    user1.export_user()
    user1.check_pass("motdepasse","email")
