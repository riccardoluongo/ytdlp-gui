ytdlp-gui is a gui front end for yt-dlp written in python using tkinter.

<h2>SUPPORTED OS</h2>

For now it only works on Windows, but support for other operating systems will be added in the future.

<h2>INSTALLATION</h2>

To install on Windows, download the latest release and run the installer.
During the installation and when you first start the app a cmd window will pop up to install the dependencies, do NOT close it.

On Ubuntu, first install the requirements:
```
apt update
apt install git python3 python3-pip python3-tk ffmpeg
pip install yt_dlp python-dotenv
```
Clone the repository:
```
git clone https://github.com/riccardoluongo/ytdlp-gui/
```
Go in the program folder:
```
cd ytdlp-gui
```
Create a folder for the logs:
```
mkdir Logs
```
Start the program:
```
python3 ytdlp-gui-linux.pyw
```

<h2>CONFIGURATION</h2>

Settings are stored in a .env file that you can open using the "File" menu at the top and clicking on "Modify preferences"
