@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
where cl >nul 2>&1 && echo CL_ON_PATH || echo CL_MISSING
cd /d D:\Desktop\RCESO\simulink
matlab -batch %1 > %2 2>&1
echo MATLAB_EXIT=%ERRORLEVEL%
