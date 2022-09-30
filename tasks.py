import os

from invoke import task

docker_username = "artronics"


def project_root_dir() -> str:
    return os.path.dirname(os.path.realpath(__file__))


@task
def docker_login(c):
    token = os.getenv("DOCKERHUB_TOKEN")
    if not token:
        raise Exception("DOCKERHUB_TOKEN is not set")

    c.run(f"docker login -u {docker_username} -p {token}")


@task
def docker_build(c):
    c.run(f"docker build -t pipeline -t {docker_username}/pipeline:local .")


@task(pre=[docker_build, docker_login])
def docker_push(c):
    c.run(f"docker push {docker_username}/pipeline")


@task
def docker_push_multi(c, version):
    c.run(f"docker buildx build --platform linux/amd64,linux/arm64 --push -t {docker_username}/pipeline:{version} .")
