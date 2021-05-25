#!/bin/env python3
import os
import time
from argparse import ArgumentParser


def run_environment(env):
    """Runs given environment executable in Windows and waits until the log file stops changing before returning."""
    sub_path = env.split("\\")
    disk = sub_path[0]
    exe = sub_path[-1]
    path = "\\".join(sub_path[:-1])
    name = sub_path[-2]
    os.system(f"cmd.exe /c \"{disk} && cd {path} && {exe}\"")

    # TODO: check until log file stops changing
    wsl_disk = f"/mnt/{sub_path[0][0].lower()}/"
    wsl_path = wsl_disk + "/".join(sub_path[1:-1])
    log_path = f"{wsl_path}/{name}/Saved/Logs/{name}.log"
    last_change = time.time()

    start = time.time()
    while not os.path.exists(log_path):
        now = time.time()
        if now - start > 10.0:
            kill(name)
            return False
    while True:
        now = time.time()
        last_change = os.path.getmtime(log_path)
        dt = now - last_change
        dt_start = now - start
        if dt > 5.0 and last_change > start:
            return True
        elif dt_start > 50.0:
            kill(name)
            return False


#TODO: use kill whenever launch is shutdown
def kill(name):
    """Kills all processes that are started by this file."""
    os.system(f"taskkill /IM \"{name}.exe\" /F")


def main():
    parser = ArgumentParser()
    parser.add_argument("-env", "--environment", type=str, help="Path to environment executable on Windows.")
    args, _ = parser.parse_known_args()
    run_environment(env=args.environment)


if __name__=="__main__":
    main()
