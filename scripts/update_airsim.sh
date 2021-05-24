#!/bin/bash
# Useful script for updating AirSim from WSL2
set -e

if [[ -z "$AirSimPath" ]]; then
    echo "Must provide AirSimPath in environment" 1>&2
    exit 1
fi

cd $AirSimPath
git pull
cmd.exe %comspec% /c 'C:\"Program Files (x86)"\"Microsoft Visual Studio"\2019\Community\Common7\Tools\VsDevCmd.bat && clean.cmd && build.cmd'
