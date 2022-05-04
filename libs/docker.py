import os
import random
import _thread


def execute_cmd(cmd):
    return "".join(list(os.popen(cmd)))


def get_id_by_image(image):
    out = execute_cmd("docker container ps -a")
    final = ""
    for i in out.split("\n")[1:]:
        if image in i:
            final = i
    final = final.replace("   "," ").split()
    return final[0]

def get_ip_by_id(id):
    out = execute_cmd("docker container ps -a")
    final = ""
    for i in out.split("\n")[1:]:
        if id in i:
            final = i
    final = final.replace("   "," ").split()
    back = execute_cmd("docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}'"+f" {final[0]}").split("\n")[0]
    return back

def create_docker_network():
    execute_cmd("docker network create --subnet=172.18.0.0/16 network1")

def list_dockers():
    return execute_cmd("docker container ls")

def exec_docker(id):
    execute_cmd(f"docker run --net network1 -it {id}")

def docker_build(file):
    with open(f"{file}/Dockerfile","r") as fich:
        data = fich.read().replace("{{random}}",''.join([str(random.randint(0,9)) for i in range(100)]))
    filename = ''.join([str(random.randint(0,9)) for i in range(10)])
    with open(f"{file}/"+filename,"w") as fich:
        fich.write(data)
    random_file = "./dockerfiles/"+''.join([str(random.randint(0,9)) for i in range(100)])
    out = execute_cmd(f"cp -r {file} {random_file}/;cd {random_file}/;rm Dockerfile;mv {filename} Dockerfile;docker build .;cd ../..;rm -rf {random_file}")
    os.remove(f"{file}/"+filename)
    for i in out.split("\n"):
        if "Successfully built" in i:
            try:
                _thread.start_new_thread(exec_docker,(i.split()[2],))
                return i.split()[2]
            except:
                pass



def delete_all():
    with open("./instances/instances.all",'w') as file:
        file.write("")
    return execute_cmd('docker system prune -a --force')

def delete_container(id,image):
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
            if image not in line:
                towrite.append(line)
    with open("./instances/instances.all","w") as file:
        file.write("\n".join(towrite))
        

def deploy_instance_user(docker_id,email):
    with open("./var/challs.txt","r") as file:
        data = file.read().split("\n")
        names = [i.split("-")[1] for i in data if i!=""]
    docker_name = names[int(docker_id)-1]
    if not os.path.isdir("./instances/"):
        os.mkdir("./instances/")
    if not os.path.isfile("./instances/instances.all"):
        with open(f"./instances/instances.all",'w') as file:
            file.write("")
    with open(f"./instances/instances.all",'r') as file:
        if file.read().count(email)>0:
            return False # ce qui signifie que le user a trop d'instances actives
    with open(f"./instances/instances.all",'a') as file:
        out = docker_build(f'./dockerfiles/{docker_name}')
        if out:
            file.write(f"{email}-{out}\n")
            return True # bien effectué
        else:
            return False

if __name__=="__main__":
    #print(get_ip_by_id("8c4a3e0f1204"))
    #delete_all()
    #print(docker_build("./dockerfiles/Test"))
    #list_dockers()
    #delete_container("bfba93f9dbbb")
    pass
