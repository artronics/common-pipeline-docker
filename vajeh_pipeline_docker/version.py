"""version.py

Usage:
  version.py [--bump BUMP] DIR
  version.py (-h | --help)

Options:
  -h --help                       Show this screen
  DIR                             Absolute path to project directory containing poetry pyproject.toml file
  --bump=[major | minor | patch]  Bump [major | minor | patch] version [default: minor]

"""
from docopt import docopt

import sys
import semver

import toml


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


def main(prj_path, bump):
    new_ver = calc_version(prj_path, bump)
    print(new_ver)

    return new_ver


if __name__ == '__main__':
    args = docopt(__doc__)
    if not args["--bump"] in ("major", "minor", "patch"):
        print(__doc__)
        print("ERROR: wrong value for --bump option. It must be one of \"major\", \"minor\" or \"patch\"")
        sys.exit(1)
    main(args["DIR"], args["--bump"])
