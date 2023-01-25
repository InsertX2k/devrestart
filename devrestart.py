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
from time import sleep
from winevt import EventLog

# initializing colorama
init(autoreset=True)

# declaring a variable containing the text to store in the output log file.
textToStoreInLogFile = ""

# declaring a configparser variable to store the device instance path of the device to restart.
configreader = ConfigParser()
configreader.read("info.ini")

# checking if the monitoring function will remain enabled or not.
if int(configreader["MiscConfiguration"]["RestartDevicesOnWakeUp"]) == 1: # enabled
    wakeUpMonitoringActive = True
    print("info: wake up monitoring function is active [ON]")
elif int(configreader["MiscConfiguration"]["RestartDevicesOnWakeUp"]) == 0: # disabled
    wakeUpMonitoringActive = False
    print("info: wake up monitoring function is inactive [OFF]")
else:
    print(f"{Fore.RED}{Style.BRIGHT}error: invalid value for RestartDevicesOnWakeUp in MiscConfiguration, please check the file info.ini in the current directory, the service will continue with the wake up monitoring function disabled.")
    wakeUpMonitoringActive = False

# getting the Windows Event Log monitoring refresh rate from config file.
try:
    monitoringRefreshRate = int(configreader["MiscConfiguration"]["PowerStateMonitoringRefreshRate"])
except ValueError:
    print(f'{Style.BRIGHT}{Fore.RED}error: expected integer or float in the monitoring refresh rate value but got another data type ({configreader["MiscConfiguration"]["PowerStateMonitoringRefreshRate"]}), which is not usable, the service will stop.')
    raise SystemExit(15)

# log file path
LogFilePath = str(configreader["MiscConfiguration"]["OutputLogFilePath"])
print(f"storing log file in : {LogFilePath}")



def restartDevice():
    """
    Restarts the given device(s) using their InstancePaths defined in the info.ini file in the current directory.
    """
    global textToStoreInLogFile, configreader, LogFilePath, wakeUpMonitoringActive
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    textToStoreInLogFile = f"devrestart2 Service Started at: {now.date()}, {current_time}"
    del current_time, now

    # getting all devices specified in the config file.
    devicenames = configreader["RestartDevice"].keys()
    for device in devicenames:
        textToStoreInLogFile = textToStoreInLogFile + f"\n\nRestarting device : {device} using Built-in pnputil...\n\n"
        turnoffdeviceoutput = getoutput(f'pnputil /disable-device "{configreader["RestartDevice"][device]}"')
        textToStoreInLogFile = textToStoreInLogFile + f"{turnoffdeviceoutput}\n\nTurned off device {device}\nTurning device {device} back on\n\n"
        turnondeviceoutput = getoutput(f'pnputil /enable-device "{configreader["RestartDevice"][device]}"')
        textToStoreInLogFile = textToStoreInLogFile + f"{turnondeviceoutput}\n\nTurned on device {device}\n\n"
        # print(f'{device}: {configreader["RestartDevice"][device]} ')

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    textToStoreInLogFile = textToStoreInLogFile + f"devrestart2 Service Finished execution at: {now.date()}, {current_time}"
    # checking if the wake up monitoring function is active.
    if wakeUpMonitoringActive == True:
        textToStoreInLogFile = textToStoreInLogFile + "\n\nNOTE: The wake up Monitoring function is active, the new device restarts will overwrite the content of this log file\n"
    
    textToStoreInLogFile = textToStoreInLogFile + "\nExiting Service execution with exit code 0\n"
    
    del current_time, now

    print(textToStoreInLogFile)
    with open(LogFilePath, mode='w+', encoding='utf-8') as saveLogFile:
        saveLogFile.write('')
        saveLogFile.write(textToStoreInLogFile)
    saveLogFile.close()
    return None # all done.

# a function to handle computer wake up events (when detected)
def handle_event(action, pContext, event):
    if int(pContext) == 1:
        print(f"System woke up from Sleep or Hibernation power states.")
        restartDevice()
        return None


if __name__ == '__main__':
    if len(argv) == 1:
        restartDevice()
        if wakeUpMonitoringActive == True:
            print("info: wake up monitoring function is active, the service will not stop at this point.")
            while True:
                event_capture = EventLog.Subscribe("System", "Event/System[Task=0][EventID=1][Level=4][Version=3][Keywords='0x8000000000000000']", handle_event)
                sleep(monitoringRefreshRate)
        raise SystemExit(0)
    if len(argv) == 2:
        restartDeviceAttemptCount = int(argv[1])
        print(f"{Style.BRIGHT}{Fore.YELLOW}working: attempting to reboot device(s) mentioned in RestartDevice section in 'info.ini' {restartDeviceAttemptCount} times")
        for currentAttemptIndex in range(restartDeviceAttemptCount):
            restartDevice()
        if wakeUpMonitoringActive == True:
            print("info: wake up monitoring function is active, the service will not stop at this point.")
            while True:
                event_capture = EventLog.Subscribe("System", "Event/System[Task=0][EventID=1][Level=4][Version=3][Keywords='0x8000000000000000']", handle_event)
                sleep(monitoringRefreshRate)
        raise SystemExit(0)
    else:
        print(f"{Style.BRIGHT}{Fore.RED}error: invalid command line usage, syntax is: restartdevice.exe/<filename>.exe (number of device restart attempts)")
        raise SystemExit(2) # exit code 2 is for invalid command line usage.
