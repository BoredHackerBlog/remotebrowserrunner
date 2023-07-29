import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def create_container(image_name, uuid):
    image = image_name
    environment = {
        "PUID": "1000",
        "PGID": "1000",
        "TZ": "Etc/UTC",
        "SUBFOLDER": "/webtop/"
    }
    shm_size = "2gb"
    network = "remotebrowsers_default"
    container = client.containers.run(
        image,
        detach=True,
        environment=environment,
        shm_size=shm_size,
        name=uuid,
        network=network,
    )

    return True

def kill_container(uuid):
    container = client.containers.get(uuid)
    container.kill()
    container.remove()

    return True
