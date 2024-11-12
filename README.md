# NuggyNet
Hey, we meet again. This is a refresh of the browser, the project started from scratch!
Not much for now!

## New features
The visual refresh is a reimagined version of NuggyNet! Here are some awesome new features:
* Tabs (v3 didn't have them)
* "French" menu (Removed but came back in this version)

> [!IMPORTANT]  
> This app might soon become Mac-only (Apple Silicon) due to the fact that the owner is getting a Mac soon and will make it natively on Xcode without the hell that Python is

> [!NOTE]
> Mac and Linux users, you do your bit by contributing and adding build instructions

# Building
1) Make sure you have Python 3.12.4 installed with "pip"
2) Download code as zip and extract
3) Open CMD window and navigate to extracted zip directory and run command `pip install -r requirements.txt`
4) Run the script to make sure everything works. Once it does, here's the building bit:
5) Run `pip install pyinstaller`
6) In the same directory, run `pyinstaller --onefile --noconsole --icon=icon.ico --add-data="nwin.html:." --add-data="about.png:." app.py`
7) Navigate to the brand new "dist" folder
8) All done

