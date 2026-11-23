@echo off
set MW_MINGW64_LOC=D:\Matlab2023\bin\win64\mingw64
cd /d D:\Desktop\RCESO\simulink
matlab -batch %1 > %2 2>&1
echo MATLAB_EXIT=%ERRORLEVEL%
