import sys
import semver
from git import Repo

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


def add_tag(proj_path, new_ver):
    repo = Repo(proj_path)
    # ref = repo.create_tag(f"v{new_ver}")
    # repo.remote("origin").push(ref.path)


def main(prj_path, bump):
    new_ver = calc_version(prj_path, bump)
    add_tag(prj_path, new_ver)


def print_usage():
    print("Usage:\nversion <absolute/path/to/project> [major|minor|patch]")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    path = sys.argv[1]
    bump = sys.argv[2]
    main(path, bump)
