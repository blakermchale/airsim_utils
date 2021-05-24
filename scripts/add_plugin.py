#!/bin/env python3
import json
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--env-path", required=True, type=str, help="Path to environment where AirSim needs to be added.")
parser.add_argument("-n", "--env-name", type=str, help="Name of environment project.")
args, _ = parser.parse_known_args()
env_path = args.env_path
if not args.env_name:
    env_name = os.path.basename(os.path.normpath(env_path))
else:
    env_name = args.env_name
uproject_path = os.path.join(env_path, f"{env_name}.uproject")
airsim_plugin = {
    "Name": "AirSim",
    "Enabled": True
}
uproject = None
with open(uproject_path, "r") as json_file:
    uproject = json.load(json_file)
    # Assume that first module is what we want
    if "AdditionalDependencies" not in uproject["Modules"][0].keys():
        uproject["Modules"][0]["AdditionalDependencies"] = ["AirSim"]
    elif "AirSim" not in uproject["Modules"][0]["AdditionalDependencies"]:
        uproject["Modules"][0]["AdditionalDependencies"].append("AirSim")

    if "Plugins" not in uproject.keys():
        uproject["Plugins"] = [
            airsim_plugin
        ]
    elif airsim_plugin not in uproject["Plugins"]:
        uproject["Plugins"].append(airsim_plugin)

with open(uproject_path, "w") as json_file:
    json.dump(uproject, json_file, indent=4)
