# remotebrowserrunner
Python Flask project that spins up a browser container for a defined amount of time

## description
Allows a user to request a browser container via webui. The user can visit /webtop/ to view their browser inside browser.

<img width="621" alt="image" src="https://github.com/BoredHackerBlog/remotebrowserrunner/assets/38662926/26797941-cab9-4c7b-a3af-682f609e39e8">

Access to the container is cookie based. The container will get shutdown and removed based on the time configured

The code and architecture can be redesigned. Also you can use gluetun container to route browser/container traffic through VPN. See https://gist.github.com/BoredHackerBlog/d23d0de7225ca0bc8c552571d1cb6f7b

## containers
- Redis - This is for keeping track of start/stop tasks by python-rq
- Worker - Python-rq worker, starts and stops containers
- Caddy - reverse proxy. Traffic that hits it either goes to the browser container or main app. Traffic to browser container is routed based on cookie and path
- App - Main webui the user hits to spin up their container and get cookie assigned to their browser

## configuration
- docker-compose.yaml - you can modify this to add gluetun container for VPN. Caddy port (entry to this network, default 8888) can be modified here too. 
Additionally, modify path to docker.sock, if you have rootless docker, your path may look similar to the default one. 
- app.py - This is where you can add more images. see https://fleet.linuxserver.io/ & https://hub.docker.com/u/kasmweb for other images, or build your own.
You can also define CONTAINER_TIME_SECONDS to define when the container gets shut down and removed.
- worker.py - browser container options can be modified in here. network should match the network caddy container is running in
- Caddyfile - Basic auth & reverse proxy options can be modified here, if needed.

## Running
- Install docker (podman might work too), git
- Git clone the repo
- cd into the repo directory, run `docker compose up --build` to start up all the containers
- visit yourip:8888, login with admin/changeme and use the webui to request a container

## modifications
- You can change worker.py and add code to make sure a limited number of containers can run
- app.py, html templates, and worker.py can be modified so you can let the user define how long they need the container for and also pass other variables (URL, proxy, etc...)
- You may be able to have multiple gluetun network and have the container join 2 diff networks (one with caddy & one with gluetun) (untested)
- app.py, html templates, and worker.py can be modified to let the user start/stop container instead of doing time-based stop (or in addition to)

## security & other issues
- Change password in Caddyfile from changeme to something else...
- There is no user management, access to container is based on cookie. container name is COOKIE-browser and you're redirected to the container by reverse proxy based on the cookie.
- container can access other containers, this can be addressed by randomizing the SUBFOLDER in worker.py and ensuring that the user is redirected to the right path (requires modifying app.py & container.html)
- There is copy & paste for text but no file upload/download.
- There isn't much logging but it can be turned on by modifying Caddyfile and Gunicorn command. The logs can be collected from file or docker output.
- Probably let trusted users access this

