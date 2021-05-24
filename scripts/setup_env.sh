#!/bin/bash
# Sets up useful files for building AirSim with custom environment

_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [[ -z "$1" ]]; then
    echo "Must provide path to environment in WSL" 1>&2
    exit 1
fi
cd $1
rm package.bat clean.bat GenerateProjectFiles.bat
wget https://raw.githubusercontent.com/microsoft/AirSim/master/Unreal/Environments/Blocks/package.bat
wget https://raw.githubusercontent.com/microsoft/AirSim/master/Unreal/Environments/Blocks/clean.bat
wget https://raw.githubusercontent.com/microsoft/AirSim/master/Unreal/Environments/Blocks/GenerateProjectFiles.bat
cp $_script_dir/update_from_git.bat ./
cp $_script_dir/update_env.sh ./
cp $_script_dir/package.sh ./

# Setup project
./update_env.sh
python $_script_dir/add_plugin.py -p $1
