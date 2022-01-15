#!/bin/env python3
import os
import time
from argparse import ArgumentParser
import threading


def execute_environment(env):
    """Runs given environment executable in Windows and waits until the log file stops changing before returning."""
    screenlock = threading.Semaphore(value=1)
    screenlock.acquire()
    print(f"Executing '{env}'")
    screenlock.release()
    sub_path = env.split("\\")
    disk = sub_path[0]
    exe = sub_path[-1]
    path = "\\".join(sub_path[:-1])
    name = sub_path[-2]
    # TODO: fix permission error
    kill(name)  # Make sure no other environments are running
    os.system(f"cmd.exe /c \"{disk} && cd {path} && {exe} > NUL\" >/dev/null 2>&1")


def wait_environment(env):
    print(f"Waiting for '{env}'")
    sub_path = env.split("\\")
    name = sub_path[-2]

    # TODO: check until log file stops changing
    wsl_disk = f"/mnt/{sub_path[0][0].lower()}/"
    wsl_path = wsl_disk + "/".join(sub_path[1:-1])
    log_path = f"{wsl_path}/{name}/Saved/Logs/{name}.log"
    last_change = time.time()

    start = time.time()
    while not os.path.exists(log_path):
        now = time.time()
        if now - start > 10.0:
            print(f"AirSim preparation failed since log file could not be found: {log_path}")
            kill(name)
            return False
        time.sleep(0.01)
    while True:
        now = time.time()
        last_change = os.path.getmtime(log_path)
        dt = now - last_change
        dt_start = now - start
        if dt > 5.0 and last_change > start:
            return True
        elif dt_start > 50.0:
            print("AirSim preparation failed since log file kept changing")
            kill(name)
            return False
        time.sleep(0.01)


#TODO: use kill whenever launch is shutdown
def kill(name):
    """Kills all processes that are started by this file."""
    # os.system(f"taskkill /IM \"{name}.exe\" /F")
    return


def run_environment(env: str):
    exe = threading.Thread(target=execute_environment, args=(env,))
    exe.start()
    return wait_environment(env)


def main():
    parser = ArgumentParser()
    parser.add_argument("-env", "--environment", type=str, help="Path to environment executable on Windows.")
    args, _ = parser.parse_known_args()
    run_environment(env=args.environment)


if __name__=="__main__":
    main()
