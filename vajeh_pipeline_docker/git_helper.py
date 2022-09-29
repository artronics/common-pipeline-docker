"""git.py

Usage:
  git.py --username username --password token [--remote remote] URL
  git.py (-h | --help)

Options:
  -h --help                       Show this screen
  URL                             GitHub repository url
  -r --remote remote              Add remote to git with username and token [default: pipeline]
  -u --username username          GitHub username
  -p --password token             GitHub token. Note: don't use your password

"""

from docopt import docopt
from mycmd import cmd


def add_remote(url, username, token, remote):
    i = len("https://")
    new_url = url[:i] + username + ":" + token + "@" + url[i:]

    cmd(f"git remote add {remote} {new_url}", "creating remote failed")


def main(username, token, url, remote):
    add_remote(url, username, token, remote)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args["--username"], args["--password"], args["URL"], args["--remote"])
