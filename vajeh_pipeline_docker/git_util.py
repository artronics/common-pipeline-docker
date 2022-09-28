"""git.py

Usage:
  git.py --username username --password token --tag tag URL
  git.py (-h | --help)

Options:
  -h --help                       Show this screen
  URL                             GitHub repository url
  -t --tag tag                    Add tag and push it to the "origin"
  -u --username username          GitHub username
  -p --password token             GitHub token. Note: don't use your password

"""

import subprocess

from docopt import docopt


def add_tag(remote, tag):
    subprocess.run(f"git tag {tag}".split(" "))
    subprocess.run(f"git push {remote} {tag}".split(" "))


def add_remote(url, username, token, remote):
    i = len("https://")
    new_url = url[:i] + username + ":" + token + "@" + url[i:]

    subprocess.run(f"git remote add {remote} {new_url}".split(" "))


def main(username, token, url, tag):
    remote = "util"
    add_remote(url, username, token, remote)
    add_tag(remote, tag)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args["--username"], args["--password"], args["URL"], args["--tag"])
