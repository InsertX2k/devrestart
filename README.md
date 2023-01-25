# devrestart2
A small command line tool for restarting one or more devices on Windows-based PCs (as of devrestart2)

## What's new in devrestart2?
* Now you can set this service to restart more than one device at once (The maximum number of devices to restart is **unlimited**), you can easily achieve that by modifying the file `Info.ini`.
* Introducing the `WakeUpMonitor` feature, it is a feature that allows the service to run in the background to monitor the power state of your computer and if the PC goes to sleep or hibernate and wakes up from it the service will attempt to restart the device(s) specified in `Info.ini` file

**(This feature can be enabled or disabled by modifying it's appropriate value in `Info.ini`, Everything is explained there)**

## Popular use cases of this tool
You might need to make a service that automates the process of disabling and re-enabling a specific device(s) driver on your computer, for some reason, you might need to do that in order to solve some hardware-related issues, and this tool will be really helpful in situations like these.

## Command Line Syntax
```bat
devrestart2.exe/<filename>.exe (number of attempts needed to restart the device)
```
* `(number of attempts needed to restart the device)` is an ***optional argument*** that can be used to define/describe the number of restart device attempts you want this service to do.

## How to use?
* Download the code in this repository or clone it using `git`
* Compile the file `devrestart.py` using [pyinstaller](https://pypi.org/project/pyinstaller/) or any other compiler you like in one directory mode.
* Download [NSSM](https://nssm.cc/)
* Store both the compiled version of this tool and NSSM in an easy to access directory, such as `C:\test`

Directory structure for `C:\test` must be like:
```
C:\test
│   install (Run as Admin).bat
│
├───devrestart2
│   │   .... (files in root of devrestart2 folder) ...
│   │
│   ├───pywin32_system32
│   │   ... (files in that folder) ...
│   │
│   ...... (other folders and sub-folders and files in the directory devrestart2) ......
│
└───nssm-2.24
    │   ChangeLog.txt
    │   README.txt
    │
    ├───src
    │      ... (files in src folder)
    │
    ├───win32
    │       nssm.exe
    │
    └───win64
            nssm.exe

```
* Enter the device instance path of the device you want to restart it's device driver every time your PC boots up in the file `info.ini`
  * ***To get Device Instance Path you have to log in as a computer administrator first***
  * Open **Device Manager** (<kbd>Win</kbd> + <kbd>X</kbd> and click on **Device Manager**, or search for **Device Manager**)
  * Expand the appropriate section of the problematic device, then right click on it and click **Properties**
  * Go to the **Details** Tab
  * Under **Property**, open that dropdown and choose **Device Instance Path**
  * Copy the text under the **value** label
  * Open the file `info.ini` and make the appropriate changes to it.
  * Save all changes you did to that file.
* Make your changes to the file `install (Run as Admin).bat`, and run it as Administrator after that.
* Restart your computer and enjoy! :)
