"""
A program for automatically enabling and disabling a specific device using it's instance Path.

Copyright (C) 2022 - Ziad Ahmed (Mr.X)
"""
from sys import argv
from configparser import ConfigParser
from datetime import datetime
from subprocess import getoutput
from os import getenv
from colorama import Style, Fore, init

# initializing colorama
init(autoreset=True)

# -----------
systemDrive = getenv('SYSTEMDRIVE')

# -----------
textToStoreInLogFile = ""

# declaring a configparser variable to store the device instance path of the device to restart.
deviceInstancePath = ConfigParser()
deviceInstancePath.read("info.ini")
deviceInstancePath = str(deviceInstancePath["RestartDevice"]["DeviceInstancePath"])
print(deviceInstancePath)

def restartDevice():
    """
    Restarts the given device using it's InstancePath defined in the global variable deviceInstancePath.
    """
    global textToStoreInLogFile, deviceInstancePath, systemDrive
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    textToStoreInLogFile = textToStoreInLogFile + f"\n\nDevice Reboot service, Device instance path: {deviceInstancePath}"
    textToStoreInLogFile = textToStoreInLogFile + f"\nStarted rebooting selected devices at:{now.date()}, {current_time}"
    turnOffCommandOutput = getoutput(f'pnputil /disable-device "{deviceInstancePath}"')
    textToStoreInLogFile = textToStoreInLogFile + f"\n{turnOffCommandOutput}"
    turnOnCommandOutput = getoutput(f'pnputil /enable-device "{deviceInstancePath}"')
    textToStoreInLogFile = textToStoreInLogFile + f"\n{turnOnCommandOutput}"
    textToStoreInLogFile = textToStoreInLogFile + f"\nFinished rebooting selected devices at:{now.date()}, {current_time}"
    textToStoreInLogFile = textToStoreInLogFile + f"\nExiting service execution with exit code 0"
    print(textToStoreInLogFile)
    with open(f'{systemDrive}\device_reboot_service.log', mode='w+', encoding='utf-8') as saveLogFile:
        saveLogFile.write('')
        saveLogFile.write(textToStoreInLogFile)
    saveLogFile.close()
    return None # all done.




if __name__ == '__main__':
    if len(argv) == 1:
        restartDevice()
        raise SystemExit(0)
    if len(argv) == 2:
        restartDeviceAttemptCount = int(argv[1])
        print(f"{Style.BRIGHT}{Fore.YELLOW}working: attempting to reboot device mentioned in 'info.ini' {restartDeviceAttemptCount} times")
        for currentAttemptIndex in range(restartDeviceAttemptCount):
            restartDevice()
        raise SystemExit(0)
    else:
        print(f"{Style.BRIGHT}{Fore.RED}error: invalid command line usage, syntax is: restartdevice.exe/<filename>.exe (number of device restart attempts)")
        raise SystemExit(2) # exit code 2 is for invalid command line usage.
