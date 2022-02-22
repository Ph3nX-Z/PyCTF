import os
import random

def execute_cmd(cmd):
    return "".join(list(os.popen(cmd)))

def list_dockers():
    return execute_cmd("docker container ls")

def docker_build(file):
    with open(file,"r") as fich:
        data = fich.read().replace("{{random}}",''.join([str(random.randint(0,9)) for i in range(100)]))
    filename = ''.join([str(random.randint(0,9)) for i in range(10)])
    with open(filename,"w") as fich:
        fich.write(data)
    out = execute_cmd(f"docker build - <{filename}")
    os.remove(filename)
    for i in out.split("\n"):
        if "Successfully built" in i:
            return i.split()[2]

def delete_all():
    with open("./instances/instances.all",'w') as file:
        file.write("")
    return execute_cmd('docker system prune -a --force')

def delete_container(id):
    try:
        execute_cmd(f"docker stop {id}")
    except:
        pass
    try:
        execute_cmd(f"docker rm {id}")
    except:
        raise "Failed"
    towrite=[]
    with open("./instances/instances.all",'r') as file:
        data = file.read().split("\n")
        for line in data:
            if id not in line:
                towrite.append(line)
    with open("./instances/instances.all","w") as file:
        file.write(towrite)
        

def deploy_instance_user(docker_id,email):
    docker_name = [None,"Test"][int(docker_id)]
    if not os.path.isdir("./instances/"):
        os.mkdir("./instances/")
    if not os.path.isfile("./instances/instances.all"):
        with open(f"./instances/instances.all",'w') as file:
            file.write("")
    with open(f"./instances/instances.all",'r') as file:
        if file.read().count(email)>3:
            return False # ce qui signifie que le user a trop d'instances actives
    with open(f"./instances/instances.all",'a') as file:
        out = docker_build(f'./dockerfiles/{docker_name}')
        if out:
            file.write(f"{email}-{out}\n")
            return True # bien effectué
        else:
            return False

if __name__=="__main__":
    delete_all()
    print(docker_build("./dockerfiles/Test"))
    list_dockers()
    #delete_container("bfba93f9dbbb")