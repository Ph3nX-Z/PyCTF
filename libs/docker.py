import os

def execute_cmd(cmd):
    return "".join(list(os.popen(cmd)))

def list_dockers():
    return execute_cmd("docker container ls")

def docker_build(file):
    out = execute_cmd(f"docker build - <{file}")
    for i in out.split("\n"):
        if "Successfully built" in i:
            return i.split()[2]

def delete_all():
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

def deploy_instance_user(file,email):
    if not os.path.isdir("./instances/"):
        os.mkdir("./instances/")
    if not os.path.isfile("./instances/instances.all"):
        with open(f"./instances/instances.all",'w') as file:
            file.write("")
    with open(f"./instances/instances.all",'r') as file:
        if file.read().count(email)>3:
            return False # ce qui signifie que le user a trop d'instances actives
    with open(f"./instances/instances.all",'a') as file:
        file.write(f"{email}-{docker_build(file)}")
        return True # bien effectué

if __name__=="__main__":
    delete_all()
    print(docker_build("./dockerfiles/Test"))
    list_dockers()
    #delete_container("bfba93f9dbbb")