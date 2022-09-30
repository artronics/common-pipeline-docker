import dataclasses

from git import Repo, Remote
from typing import List


@dataclasses.dataclass
class GitConfig:
    repo_path: str
    account_name: str
    commit_name: str
    commit_email: str
    remote_url: str
    token: str
    remote_name: str = "pipeline"


def add_remote(conf: GitConfig, repo: Repo) -> (Repo, Remote):
    i = len("https://")
    url = conf.remote_url
    auth_url = url[:i] + conf.account_name + ":" + conf.token + "@" + url[i:]

    remotes = list(filter(lambda x: x.name == conf.remote_name, repo.remotes))
    if remotes:
        remote = remotes[0]
        u = list(remote.urls)
        if not u[0] == auth_url:
            remote.set_url(auth_url, u[0])
    else:
        remote = repo.create_remote(conf.remote_name, auth_url)

    return repo, remote


def commit(repo: Repo, files: List[str], message: str, remote: Remote) -> (Repo, Remote):
    repo.index.add(files)
    repo.index.commit(message)
    repo.remote(remote.name).push()

    return repo, remote


def tag(repo: Repo, tag: str, remote: Remote) -> (Repo, Remote):
    git_tag = repo.create_tag(tag)
    repo.remote(remote.name).push(git_tag.path)

    return repo, remote


def config(conf: GitConfig, repo: Repo) -> Repo:
    cr = repo.config_reader()
    if not cr.has_option("user", "email"):
        repo.config_writer().set_value("user", "email", conf.commit_email).release()
    if not cr.has_option("user", "name"):
        repo.config_writer().set_value("user", "name", conf.commit_name).release()

    return repo


def get_repo(conf: GitConfig) -> Repo:
    return Repo(conf.repo_path)
