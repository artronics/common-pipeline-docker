"""version.py

Usage:
  version.py [--bump BUMP] [--write] DIR
  version.py (-h | --help)

Options:
  -h --help                       Show this screen
  DIR                             Absolute path to project directory containing poetry pyproject.toml file
  --bump=[major | minor | patch]  Bump [major | minor | patch] version [default: minor]
  -w --write                      Modify the pyproject.toml file with the new version

"""
import datetime
import sys

import semver
import toml
from docopt import docopt


def calc_version(prj_path, bump):
    pyproject_file = toml.load(f"{prj_path}/pyproject.toml")
    current_ver = semver.VersionInfo.parse(pyproject_file["tool"]["poetry"]["version"])

    new_ver = None
    if bump == 'major':
        new_ver = current_ver.bump_major()
    if bump == 'minor':
        new_ver = current_ver.bump_minor()
    if bump == 'patch':
        new_ver = current_ver.bump_patch()

    return new_ver


def rewrite_file(prj_path, new_ver):
    content = ""
    with open(f"{prj_path}/pyproject.toml", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("version"):
                content = content + f"version = \"{new_ver}\" # Auto updated on {datetime.datetime.now()}\n"
            else:
                content = content + line

    with open(f"{prj_path}/pyproject.toml", "w") as f:
        f.write(content)


def main(prj_path, bump, write):
    new_ver = calc_version(prj_path, bump)
    if write:
        rewrite_file(prj_path, new_ver)
    else:
        print(new_ver)

    return new_ver


if __name__ == '__main__':
    args = docopt(__doc__)
    if not args["--bump"] in ("major", "minor", "patch"):
        print(__doc__)
        print("ERROR: wrong value for --bump option. It must be one of \"major\", \"minor\" or \"patch\"")
        sys.exit(1)
    main(args["DIR"], args["--bump"], args["--write"])
