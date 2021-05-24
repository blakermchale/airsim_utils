#!/bin/env python3
import json
import os
import subprocess
from argparse import ArgumentParser
import numpy as np


DEFAULT_PAWN_BP = "Class'/AirSim/Blueprints/BP_FlyingPawn.BP_FlyingPawn_C'"
DEFAULT_NB = 1
DEFAULT_LAT = 47.641468
DEFAULT_LON = -122.140165
DEFAULT_ALT = 122



# https://microsoft.github.io/AirSim/settings/#available-settings-and-their-defaults
def create_settings(pawn_bp=DEFAULT_PAWN_BP, nb=DEFAULT_NB, lat=DEFAULT_LAT, lon=DEFAULT_LON, 
                    alt=DEFAULT_ALT):
    """Generate AirSim settings."""
    hfov_color = 69.39
    hfov_ir = 85.94
    settings = {
        "SettingsVersion": 1.2,
        "SimMode": "Multirotor",
        "PawnPaths": {
            "DefaultQuadrotor": {"PawnBP": pawn_bp},
        },
        "OriginGeopoint": {
            "Latitude": lat,
            "Longitude": lon,
            "Altitude": alt
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

    # Create individual drones
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
            "X": 0, "Y": 1.5*i, "Z": 0,
            "Sensors":{
                "Barometer":{
                    "SensorType": 1,
                    "Enabled": True,
                    "PressureFactorSigma": 0.0001825
                }
            },
            "Parameters": {
                "NAV_RCL_ACT": 0,
                "NAV_DLL_ACT": 0,
                "COM_OBL_ACT": 1,
                "LPE_LAT": lat,
                "LPE_LON": lon
            }
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



def main():
    parser = ArgumentParser()
    parser.add_argument("-pb", "--pawn-bp", default=DEFAULT_PAWN_BP, type=str, help="Path to pawn blueprint.")
    parser.add_argument("-nb", "--number", default=DEFAULT_NB, type=int, help="Number of vehicles to spawn.")
    parser.add_argument("-lat", "--latitude", default=DEFAULT_LAT, type=float, help="Latitude.")
    parser.add_argument("-lon", "--longitude", default=DEFAULT_LON, type=float, help="Latitude.")
    parser.add_argument("-alt", "--altitude", default=DEFAULT_ALT, type=float, help="Longitude.")

    args, _ = parser.parse_known_args()
    create_settings(pawn_bp=args.pawn_bp, nb=args.number, lat=args.latitude, lon=args.longitude, alt=args.altitude)


if __name__=="__main__":
    main()
