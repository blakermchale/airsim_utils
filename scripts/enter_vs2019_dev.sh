#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Must provide path to environment in WSL" 1>&2
    exit 1
fi

cd $1
cmd.exe %comspec% /k 'C:\"Program Files (x86)"\"Microsoft Visual Studio"\2019\Community\Common7\Tools\VsDevCmd.bat'
