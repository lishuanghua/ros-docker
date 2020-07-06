#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time

import docker

_docker_cli = None


def get_docker_cli():
    global _docker_cli
    if _docker_cli is None:
        _docker_cli = docker.client.from_env()
    return _docker_cli


def start_container(container_name, start_timeout):
    try:
        docker_cli.containers.get(container_name)
    except docker.errors.NotFound:
        docker_cli.containers.run("moliqingwa/ros-vnc:melodic",
                                  name=container_name,
                                  environment={},  # key=>value
                                  ports={'6080/tcp': 16080,
                                         "5900/tcp": 15900,
                                         },
                                  restart_policy={"Name": "on-failure",
                                                  "MaximumRetryCount": 1,
                                                  },
                                  # tmpfs=,  # mount
                                  detach=True,
                                  )

    container = docker_cli.containers.get(container_name)
    first_time = time.time()
    while container.status != "running":
        container = docker_cli.containers.get(container_name)
        if container.status != "running":
            container.start()
            time.sleep(0.1)
        else:
            curr_time = time.time()
            if curr_time - first_time > start_timeout:
                raise TimeoutError(f"docker start timeout after {start_timeout} seconds!")
    return container


if __name__ == "__main__":
    container_name = "ros-melodic-v1"
    start_timeout = 60  # seconds
    docker_cli = get_docker_cli()
    # docker_cli.images.load()

    try:
        container = start_container(container_name, start_timeout)
    except docker.errors.APIError as ex:
        print("docker api error", ex)
        raise ex
    except Exception as ex:
        print("docker unknown error", ex)
        raise ex

    print(f"Container {container_name} is in {container.status} status!")
    assert container.status == 'running'

    prev_time = curr_time = time.time()
    # for line in container.logs(stream=True, until=5):
    #     print(line)

    pass
