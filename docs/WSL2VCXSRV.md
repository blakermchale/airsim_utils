# WSL2 VcXsrv (by Blake McHale)
## Setup  
1. Download VcXsrv from [here](https://sourceforge.net/projects/vcxsrv/)
2. Add environment variables to `~/.bashrc` in WSL2 terminal  
```bash
export WSL_HOST_IP=$(ipconfig.exe | awk '/WSL/ {getline; getline; getline; getline; print substr($14, 1, length($14)-1)}')
export DISPLAY=$WSL_HOST_IP:0.0
```  
3. Create shortcut for `C:\Program Files\VcXsrv\vcxsrv.exe` on Windows (if default install was not used change file path)  
4. Open properties of `vcxsrv.exe` shortcut by right clicking on executable in file explorer
5. Add the following to `Target` in properties (change file path if necessary)  
```bash
"C:\Program Files\VcXsrv\vcxsrv.exe" :0 -ac -terminate -lesspointer -multiwindow -clipboard -nowgl -dpi auto
```  
## Run  
1. Run the shortcut to `vcxsrv.exe`  
2. Open WSL2 terminal and run GUI program!
