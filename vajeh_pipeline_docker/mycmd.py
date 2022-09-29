import subprocess


def cmd(_cmd: str, err_msg: str = ""):
    c = _cmd.split(" ")
    p = subprocess.run(c)
    if p.returncode != 0:
        raise Exception(err_msg)
