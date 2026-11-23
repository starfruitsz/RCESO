@echo off
call "D:\VS\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
where cl
if errorlevel 1 (echo CL_STILL_MISSING) else (echo CL_OK)
cd /d D:\Desktop\RCESO\simulink
matlab -batch %1 > %2 2>&1
echo MATLAB_EXIT=%ERRORLEVEL%
