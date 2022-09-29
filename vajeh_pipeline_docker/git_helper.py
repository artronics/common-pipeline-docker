"""git.py

Usage:
  git.py --username username --password token [--remote-name remote-name] --remote-url remote-url
  git.py (-h | --help)

Options:
  -h --help                       Show this screen
  URL                             GitHub repository url
  -n --remote-name remote-name    Remote name [default: pipeline]
  -r --remote-url remote-url      Add remote to git with username and token
  -u --username username          GitHub username
  -p --password token             GitHub token. Note: don't use your password

"""

from docopt import docopt
from mycmd import cmd


def add_remote(url, username, token, remote):
    i = len("https://")
    new_url = url[:i] + username + ":" + token + "@" + url[i:]

    cmd(f"git remote add {remote} {new_url}", "creating remote failed")


def main(username, token, remote_url, remote_name):
    add_remote(remote_url, username, token, remote_name)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args["--username"], args["--password"], args["--remote-url"], args["--remote-name"])
