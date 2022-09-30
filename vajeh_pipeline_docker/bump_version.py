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
from typing import Literal

from docopt import docopt

import git_helper as _git
import version as ver
from git_helper import GitConfig
from version import VersionConfig


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
    git_conf = GitConfig(repo_path=cwd, account_name=config.github_account, commit_name=config.git_user_name,
                         commit_email=config.git_user_email, remote_url=config.git_remote_url,
                         token=config.github_token, remote_name=config.git_remote_name)

    repo = _git.get_repo(git_conf)
    repo = _git.config(git_conf, repo)
    repo, remote = _git.add_remote(git_conf, repo)

    ver_conf = VersionConfig(project_path=cwd, write_file=True, project_type="poetry", bump=config.bump)
    new_ver = ver.calc_version(ver_conf)
    changed_files = ver.write_file(ver_conf, new_ver)

    tag = f"v{new_ver}"
    commit_msg = f"Publish new version: {tag}"
    repo, remote = _git.commit(repo, changed_files, commit_msg, remote)

    _, _ = _git.tag(repo, tag, remote)

    print(f"Pushed new tag: {tag}")


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
    main(config)
