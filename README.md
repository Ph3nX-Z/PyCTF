# PyCTF
Web Based CTF Platform, multithreaded and powered by python3

Hosted Version : https://pyctf.fr/

VERSION : Beta 1.0

![](./readme_img/index.png)

## Presentation

PyCTF is a CTF platform that allows you to add challenges and deploy them dynamicaly. The storage of the personnal information are secured, such as the password, that are hashed with a complex algorithm (sha256, multi-round, with complex salt). This platform supports one or more users, and can be personalized (style and code).


## Usage

### Linux/Windows :

#### Install
```sh
git clone [url]
cd PyCTF
sudo python3 main.py
(for the external access, you will have to setup an openvpn server)
```
You will have to run the app in screen if you want to deploy it in production:
```sh
sudo apt install screen
screen 
sudo python3 main.py
Ctrl-A
Ctrl-D
screen -r (to get back into the screen session)
```

#### Add Challenges
* Add a folder containing the challenge, with the dockerfile (in which you'll put one echo {{random}} to detach every docker id).
* Add a challenge with a category, an id and a flag in ./var/challs.txt
* Add the challenge in ./templates/instances.html
There are no needs to restart the app, it will be reloaded automatically

#### Uninstall
```sh
rm -rf PyCTF
sudo docker system prune -a (Optional)
```

### Features to come :
* Global Chat
* Improve admin panel

### Features :
* Users management
* Instances Management
* Points and ranks system
* Scoreboard
* Email verification
* Login/logout and register panel
* Stats and personalized graphs
* User Friendly interface
* Automatic network configuration
* External access to docker network
* Optimisation of the website 
* Admin Panel
* Port representation (ranges and unique)

## Media


### Stats

![](./readme_img/stat.png)

### Scoreboard

![](./readme_img/scoreboard.png)

### Instances

![](./readme_img/instances.png)

### Admin Panel

![](./readme_img/admin.png)

## Legal

Usefull Info:
* Informations are only stored in your computer.
* This project isn't GPDR compliant and must be used for personnal usage.

## Project Info

Back-End / Front-End / Code : [Ph3nX](https://github.com/Ph3nX-Z)

Report a Bug : [Report](https://github.com/Ph3nX-Z/PyCTF/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)

## Supporters:
[![](https://reporoster.com/stars/dark/ph3nx-Z/PyCTF)](https://github.com/Ph3nX-Z/PyCTF/stargazers)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
