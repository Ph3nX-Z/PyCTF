from lxml import etree
import os
class User:
    def __init__(self,right,pseudo,points,id,email,password):
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
            raise "File already exists ! User already registered !"

    def import_user(self):
        pass

    def hash_pass(self):
        pass
        
if __name__=="__main__":
    user1=User("admin","Ph3nX","10000","0","ph3nxx@protonmail.com","motdepasse")
    user1.hash_pass()
    user1.export_user()