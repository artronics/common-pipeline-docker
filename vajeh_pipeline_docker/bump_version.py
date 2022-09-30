"""version.py

Usage:
  version.py [--bump=BUMP] \
[--git-remote-name=name] [--github-account=account] --github-token=token \
--git-remote-url=url --git-user-name=user-name --git-user-email=user-email
  version.py (-h | --help)

Options:
  -h --help                       Show this screen
  --bump=[major | minor | patch]  Bump [major | minor | patch] version [default: minor]
  --git-remote-name remote-name    Remote name [default: pipeline]
  --git-remote-url remote-url      Add remote to git with username and token
  --git-user-name username          git username
  --git-user-email email          git user email
  --github-token token             GitHub token. Note: don't use your password
  --github-account account             GitHub account name. If not present it will be inferred from --git-remote-url

"""
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime

import toml
import semver
from typing import Literal

from docopt import docopt
from git import Repo


@dataclass
class Config:
    github_account: str
    git_user_name: str
    git_user_email: str
    git_remote_url: str
    github_token: str
    git_remote_name: str = "pipeline"
    bump: Literal["major", "minor", "patch"] = "minor"


def main(_config: Config):
    cwd = os.getcwd()
    repo = Repo(cwd)

    # config
    cr = repo.config_reader()
    if not cr.has_option("user", "email"):
        repo.config_writer().set_value("user", "email", _config.git_user_email).release()
    if not cr.has_option("user", "name"):
        repo.config_writer().set_value("user", "name", _config.git_user_name).release()

    # add remote
    i = len("https://")
    url = config.git_remote_url
    auth_url = url[:i] + config.github_account + ":" + config.github_token + "@" + url[i:]

    remotes = list(filter(lambda x: x.name == config.git_remote_name, repo.remotes))
    if remotes:
        remote = remotes[0]
        u = list(remote.urls)
        if not u[0] == auth_url:
            remote.set_url(auth_url, u[0])
    else:
        remote = repo.create_remote(config.git_remote_name, auth_url)

    pyproject = f"{cwd}/pyproject.toml"
    pyproject_file = toml.load(pyproject)
    current_ver = semver.VersionInfo.parse(pyproject_file["tool"]["poetry"]["version"])

    if config.bump == 'major':
        new_ver = current_ver.bump_major()
    elif config.bump == 'patch':
        new_ver = current_ver.bump_patch()
    else:
        new_ver = current_ver.bump_minor()

    content = ""
    with open(pyproject, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("version"):
                content = content + f"version = \"{new_ver}\" # Auto updated on {datetime.now()}\n"
            else:
                content = content + line

    with open(pyproject, "w") as f:
        f.write(content)

    repo.index.add([pyproject])
    repo.index.commit(f"Publish new version: {new_ver}")
    repo.remote(remote.name).push()

    tag = repo.create_tag(f"v{new_ver}")
    repo.remote(remote.name).push(tag.path)


if __name__ == '__main__':
    args = docopt(__doc__)


    def err(msg):
        print(__doc__)
        print(msg)
        sys.exit(1)


    url_re = r"https://github.com/(.+)/.+\.git$"
    remote_url = args["--git-remote-url"]
    if match := re.search(url_re, remote_url, re.IGNORECASE):
        if not args.get("--github-account"):
            args["--github-account"] = match.group(1)
    else:
        err("--git-remote-url is invalid. "
            "It must be a valid repository url like: https://github.com/<account>/<repo-name>.git")

    if not os.path.exists(f"{os.getcwd()}/pyproject.toml"):
        err("Can't find pyproject.toml file. This script must be executed in a poetry project's root directory")

    if bump := args.get("--bump"):
        if bump != "major" and bump != "minor" and bump != "patch":
            err("--bump must be one of major, minor or patch")

    config = Config(
        github_account=args["--github-account"],
        github_token=args["--github-token"],
        git_user_name=args["--git-user-name"],
        git_user_email=args["--git-user-email"],
        git_remote_name=args["--git-remote-name"],
        git_remote_url=args["--git-remote-url"],

        bump=args["--bump"]
    )
    print(config)
    main(config)
