"""deploy.py

Usage:
  deploy.py version [--bump=BUMP] \
[--git-remote-name=name] [--github-account=account] --github-token=token \
--git-remote-url=url --git-user-name=user-name --git-user-email=user-email
  deploy.py version [--bump=BUMP] --github-context=context --git-user-name=user-name --git-user-email=user-email

  deploy.py (-h | --help)

Options:
  -h --help                       Show this screen
  -c --github-context context            GitHub context as JSON
  --bump=[major | minor | patch]  Bump [major | minor | patch] version [default: minor]
  --git-remote-name remote-name    Remote name [default: pipeline]
  --git-remote-url remote-url      Add remote to git with username and token
  --git-user-name username          git username
  --git-user-email email          git user email
  --github-token token             GitHub token. Note: don't use your password
  --github-account account             GitHub account name. If not present it will be inferred from --git-remote-url

"""
import json
import os
import re
import sys
from dataclasses import dataclass

from docopt import docopt

import git_helper as _git
import version as ver
from git_helper import GitConfig
from version import VersionConfig


@dataclass
class Config:
    git_config: GitConfig
    version_config: VersionConfig


def main(_config: Config):
    git_conf = config.git_config

    repo = _git.get_repo(git_conf)
    repo = _git.config(git_conf, repo)
    repo, remote = _git.add_remote(git_conf, repo)

    ver_conf = config.version_config
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


    if context := args.get("--github-context"):
        c = json.loads(context)
        args["--git-remote-url"] = c["repositoryUrl"].replace("git://", "https://")
        args["--github-account"] = c["repository_owner"]
        args["--github-token"] = c["token"]

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

    cwd = os.getcwd()
    git_config = GitConfig(repo_path=cwd,
                           account_name=args["--github-account"],
                           commit_name=args["--git-user-name"],
                           commit_email=args["--git-user-email"],
                           remote_url=args["--git-remote-url"],
                           token=args["--github-token"],
                           remote_name=args["--git-remote-name"])
    ver_config = VersionConfig(project_path=cwd, write_file=True, project_type="poetry", bump=args["--bump"])
    config = Config(git_config=git_config, version_config=ver_config)
    print(args)
    print(config)
    # main(config)
