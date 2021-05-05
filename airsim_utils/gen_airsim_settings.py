#!/bin/env python3
import json
import os
import subprocess
from argparse import ArgumentParser
import numpy as np


# https://microsoft.github.io/AirSim/settings/#available-settings-and-their-defaults
def main(args=None):
    nb = 3
    hfov_color = 69.39
    hfov_ir = 85.94
    settings = {
        "SettingsVersion": 1.2,
        "SimMode": "Multirotor",
        "PawnPaths": {
            "DefaultQuadrotor": {"PawnBP": "Class'/Game/NUAV/Blueprints/BP_FlyingPawn.BP_FlyingPawn_C'"},
        },
        "CameraDefaults": {
            "CaptureSettings": [
                {
                "ImageType": 0,
                "Width": 640,
                "Height": 480,
                "FOV_Degrees": hfov_color,  # from frog
                "AutoExposureSpeed": 100,
                "MotionBlurAmount": 0
                },
                {
                "ImageType": 7,
                "Width": 640,
                "Height": 480,
                "FOV_Degrees": hfov_ir,
                "AutoExposureSpeed": 100,
                "MotionBlurAmount": 0
                },
                # {
                # "ImageType": 1,
                # "Width": 1920,
                # "Height": 1080,
                # "FOV_Degrees": 90,
                # "AutoExposureSpeed": 100,
                # "MotionBlurAmount": 0
                # },
            ]
        },
        "Vehicles": {}
    }
    for i in range(nb):
        settings["Vehicles"][f"drone_{i}"] = {
            "VehicleType": "PX4Multirotor",
            "UseSerial": False,
            "UseTcp": True,
            "QgcHostIp": "127.0.0.1",
            "QgcPort": 14550,
            "TcpPort": 4560 + i,
            "ControlIp": os.environ["WSL_IP"].rstrip(" "),
            "ControlPort": 14580,
            "LocalHostIp": os.environ["WSL_HOST_IP"],
            "X": 0, "Y": 1.5*i, "Z": 0
            # "Cameras": {
            #     "realsense_down": {
            #         "CaptureSettings": [
            #         {
            #             "ImageType": 0,  # Scene
            #             "Width": 1920,
            #             "Height": 1080
            #         },
            #         {
            #             "ImageType": 7,  # Infrared
            #             "Width": 1920,
            #             "Height": 1080
            #         },
            #         {
            #             "ImageType": 1,  # DepthPlanar
            #             "Width": 1920,
            #             "Height": 1080
            #         }
            #         ],
            #         "Pitch": 1.57
            #     }
            # },
            
        }
    var_result = subprocess.run(["wslvar", "USERPROFILE"], capture_output=True, text=True).stdout
    win_home = subprocess.run(["wslpath", var_result], capture_output=True, text=True).stdout
    win_home = win_home.rstrip('\n')
    airsim_settings = os.path.join(win_home, "Documents", "AirSim", "settings.json")
    with open(airsim_settings, 'w') as outfile:
        json.dump(settings, outfile, indent=4)


if __name__=="__main__":
    main()
