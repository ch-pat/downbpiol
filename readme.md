# downbpiol
Tool for downloading CBI and 896 files from the BPIOL service.

Currently a WIP.

### requirements
* geckodriver.exe in the script directory
* selenium must be installed: `python -m pip install selenium`
* a `.credentials` file needs to be present in the script directory containing login information on separate lines:
* * `azienda`
* * `username`
* * `password`
* Sadly, only really works if your account can (for some reason) still **login without app authentication**. After the script works correctly I will start working on a solution.