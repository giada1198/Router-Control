# Lightware DVI Router Control

![head](/img/head.jpg)

This is a GUI app for cueing [Lightware DVI Router](https://lightware.com/products/mx8x8dvi-hdcp-pro) via serial string, originally developed for [A/B Machines](https://giada1198.github.io/Giada-Portfolio/works/ABMachines), CMU School of Drama MFA Production in 2018.

## Getting Started

### Prerequisites

#### Install Homebrew

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Paste that in a Terminal prompt. Goto [Official Website](https://brew.sh/) to get more information.

#### Install Python 3

```
brew install python3
```

#### Install Dependent Python Libraries

##### [pySerial](https://pyserial.readthedocs.io/en/latest/index.html) and [python-osc](https://pypi.org/project/python-osc/):

```
pip3 install pyserial
pip3 install python-osc
```

### Installation

Downlaod or clone the project:

```
git clone https://github.com/giada1198/Router-Control.git
```

## Running the Tests

### Setup Serial and OSC Ports

#### List Serial Ports

Launch Terminal and type the following command string:

```
python3 -m serial.tools.list_ports
```

#### Setup Serial Port

Goto `main.py` and paste the port connected to the router:

```
# BASIC SETUP
serialPort = '[Paste Here]'
```

#### Setup OSC Port

```
oscPort    = [The Port Value]
```

### Launch the App

Open `click_to_launch.applescript` in built-in [Script Editor](https://en.wikipedia.org/wiki/AppleScript_Editor).

![script-editor](/img/script-editor.jpg)

Click `Compile the Script` and then `Run the Script`. You can save it as an application file, but remember it has to be in the same folder as `main.py` in.

![router-control](/img/router-control.jpg)

### Load Cue List Table

Click `File > Load` and then select `cue_list_sample.csv`.

### OSC Command

Use `/router/launchCue [Cue Number]` to launch cues via OSC.

## Author

* **Giada Sun** - Graduate Student in Video & Media Design at [CMU](https://www.cmu.edu/) - [Website](http://giadasun.com)
