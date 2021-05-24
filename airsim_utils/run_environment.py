#!/bin/env python3
import os
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-env", "--environment", type=str, help="Path to environment executable on Windows.")
    args, _ = parser.parse_known_args()
    sub_path = args.environment.split("\\")
    disk = sub_path[0]
    exe = sub_path[-1]
    path = "\\".join(sub_path[:-1])
    os.system(f"cmd.exe /c \"{disk} && cd {path} && {exe}\"")


if __name__=="__main__":
    main()
