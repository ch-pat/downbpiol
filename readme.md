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

# DISCLAIMER
This project is in no way associated with Poste Italiane.

The script is implemented with respect towards the service provider, static waits are included as to not stress the service with too many HTTP requests at a time.

The script simply simulates the normal usage of a browser, and therefore **does not exploit the service provided in any way that is not considered normal use**. In fact it simply replicates routine actions I have always been doing.

Despite all this, there is **no guarantee that the service provider won't punish you for using this script**, and I hold no responsibility whatsoever for your use of the script. You are fully responsible and knowingly take the risk by using this script.

The script might break anytime the BPIOL website updates its layout, or when Firefox updates to a new version.