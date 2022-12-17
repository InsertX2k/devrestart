@echo off
SET scriptpath=%~dp0
cd /d %scriptpath%
xcopy devrestart "%windir%\devrestart" /F /Y /H /I
xcopy nssm-2.24\win64\nssm.exe "%windir%\devrestart\nssm.exe" /Y /H /R /I
%windir%\devrestart\nssm.exe install "onboard_controller_fix" "%windir%\devrestart\devrestart.exe"
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\onboard_controller_fix" /v "ErrorControl" /t REG_DWORD /f /d 0
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\onboard_controller_fix" /v "Start" /t REG_DWORD /f /d 2
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\onboard_controller_fix\Parameters\AppExit" /ve /f /d "Exit" /t REG_SZ
echo.
echo All pending operations completed, press any key to close this window
pause >nul
exit /b 0