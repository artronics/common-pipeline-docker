"""version.py

Usage:
  version.py [--git-remote-name name] --git-remote-url url --git-user-name user-name --git-user-email user-email --github-token token --github-account account
  version.py (-h | --help)

Options:
  -h --help                       Show this screen
  -n --git-remote-name remote-name    Remote name [default: pipeline]
  -r --git-remote-url remote-url      Add remote to git with username and token
  -u --git-user-name username          git username
  -e --git-user-email email          git user email
  -t --github-token token             GitHub token. Note: don't use your password
  -p --github-account account             GitHub account name

"""
import os
from dataclasses import dataclass

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


def main(config: Config):
    d = os.getcwd()
    repo = Repo(d)
    c = repo.config_reader()
    if not c.has_option("user", "email"):
        repo.config_writer().set_value("user", "email", config.git_user_email)
    if not c.has_option("user", "name"):
        repo.config_writer().set_value("user", "name", config.git_user_name)


if __name__ == '__main__':
    args = docopt(__doc__)
    config = Config(
        github_account=args["--github-account"],
        github_token=args["--github-token"],
        git_user_name=args["--git-user-name"],
        git_user_email=args["--git-user-email"],
        git_remote_name=args["--git-remote-name"],
        git_remote_url=args["--git-remote-url"],
    )
    main(config)
