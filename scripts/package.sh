#!/bin/bash

_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $_script_dir
cmd.exe /c 'package.bat %cd%\output ^"^" 4.26'
