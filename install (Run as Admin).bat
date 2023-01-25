@echo off
SET scriptpath=%~dp0
cd /d %scriptpath%
xcopy devrestart2 "%windir%\devrestart2" /F /Y /H /I /E
xcopy nssm-2.24\win64\nssm.exe "%windir%\devrestart2\nssm.exe" /Y /H /R /I
%windir%\devrestart2\nssm.exe install "devrestart" "%windir%\devrestart2\devrestart2.exe"
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\devrestart" /v "ErrorControl" /t REG_DWORD /f /d 0
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\devrestart" /v "Start" /t REG_DWORD /f /d 2
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\devrestart\Parameters\AppExit" /ve /f /d "Exit" /t REG_SZ
reg add "HKLM\SYSTEM\CurrentControlSet\Services\devrestart" /v "DisplayName" /t REG_SZ /d "devrestart2 and its sub-services" /f
sc config devrestart displayName= "devrestart2 Handler Windows NT Service"
echo.
echo All pending operations completed, press any key to close this window
echo You may restart your computer for the service to start.
pause >nul
exit /b 0