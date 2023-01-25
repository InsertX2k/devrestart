# devrestart2
A small command line tool for restarting one or more devices on Windows-based PCs (as of devrestart2)

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
* Enter the device instance path of the device you want to restart it's device driver every time your PC boots up in the file `info.ini`
  * ***To get Device Instance Path you have to log in as a computer administrator first***
  * Open **Device Manager** (<kbd>Win</kbd> + <kbd>X</kbd> and click on **Device Manager**, or search for **Device Manager**)
  * Expand the appropriate section of the problematic device, then right click on it and click **Properties**
  * Go to the **Details** Tab
  * Under **Property**, open that dropdown and choose **Device Instance Path**
  * Copy the text under the **value** label
  * Open the file `info.ini` and make the appropriate changes to it.
  * Save all changes you did to that file.
* Make your changes to the file `install (Run as Admin).bat` if necessary, and run it as Administrator after that.
* Restart your computer and enjoy! :)
