# airsim_utils
General airsim utility files for generating settings and environments. Packages everything for easy 
access and automation with ROS2.

## Setup  
Set the environment variable `AirSimPath` on your Windows side and in WSL2.

### AirSim  
Make sure AirSim is built:
```bash
./update_airsim.sh
```

### Environments  
Run:
```bash
./setup_env.sh $UE4_ENV_PATH
cd $UE4_ENV_PATH
./update_env.sh
```

## Extra
### Packaging  
Run from Unreal environment directory in WSL:  
```bash
./package.sh
```

## Tips  
When adding custom blueprints for vehicles those assets must be added to the `AirSimAssets.umap` world.
This can be done by dragging the blueprint into the world.
