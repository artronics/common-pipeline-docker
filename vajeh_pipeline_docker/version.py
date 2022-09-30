import dataclasses
import datetime
from typing import Literal, List

import semver
import toml
from datetime import datetime


@dataclasses.dataclass
class VersionConfig:
    project_path: str
    write_file: bool = True
    project_type: Literal["poetry"] = "poetry"  # only poetry is supported for now
    bump: Literal["major", "minor", "patch"] = "minor"


def calc_version(conf: VersionConfig) -> str:
    if conf.project_type == "poetry":
        pyproject = toml.load(f"{conf.project_path}/pyproject.toml")
    else:
        raise Exception("only poetry project is supported")

    current_ver = semver.VersionInfo.parse(pyproject["tool"]["poetry"]["version"])

    if conf.bump == "major":
        new_ver = current_ver.bump_major()
    elif conf.bump == "patch":
        new_ver = current_ver.bump_patch()
    else:
        new_ver = current_ver.bump_minor()

    return str(new_ver)


def write_file(conf: VersionConfig, new_ver: str) -> List[str]:
    if conf.project_type == "poetry":
        pyproject = toml.load(f"{conf.project_path}/pyproject.toml")
    else:
        raise Exception("only poetry project is supported")

    changed_files = [pyproject]

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

    return changed_files
