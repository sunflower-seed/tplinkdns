# tplinkdns
Selenium driven Python script for remote changing DNS Value of TP-Link routers with their new GUI.

Tested on an Archer VR600v model from TP-Link

## About

Sadly the TP-Link Archer VR600v does not provide remote access despite a telnet shell.
Therefore it is not possible to change DNS Server values on the fly.
Additionally the GUI is heavy JS loaded with security features,
which makes it difficult to access any maybe existing API.

This scripts makes use of selenium webdriver to simply manipulate the router GUI.
It might be suitable for other use cases.

## Requirements

You need a Chrom(ium) Browser installed.
On Debian a Debian Server without Desktop it i will look like this:

```
apt install chromium --no-install-recommends
```

Furthermore you need the chrom(ium)-webdriver:

```
apt install chromium-webdriver
```

Please make shure that you have installed selenium for your Python installation, you might do this in a Python venv.

```
pip install selenium
```

## Usage

Run this script with the desired IP of your DNS Server:

```
./tplinkdns.py "192.168.1.5"
```

## License

GPLv3
