# PyQt6 SSH Terminal Widget: UglierPTY

## Overview

UglierPTY is a very functional proof-of-concept (POC) application created to construct a fully functional SSH Terminal Widget using PyQt6. This POC is inspired by its sister project, UglyPTY, a full-featured SSH client that utilizes xterm.js. The aim is to offer a similar, if not superior, feature set without relying on browser technologies or JavaScript, resulting in a more streamlined and resource-efficient solution.

This is a work in progress, but feel free to give it a try!
REPO: https://github.com/scottpeterman/UglierPTY

#### A Note About UglyPTY

If your interested in the PyQt6/XTerm.js version of this application take a look here: https://github.com/scottpeterman/UglyPTY

## Features

- Fully functional SSH terminal built with PyQt6
- Credentials manager for easy login
- Portable session files in YAML (Compatible with UglyPTY)
- Terminal history and screen ratio control via pyte
- Terminal screen render via QPaint
- Modular design for easy embedding into other PyQt6 projects
- Pure Python - Free of Web technology (no xterm.js)

## Architecture


- Python 3.x
- PyQt6
- Paramiko
- pyte
- SQLAlchemy
- PyYaml

## Screenshots

Here are some snapshots of Uglier in action:

<div align="center">
  <img src="https://github.com/scottpeterman/UglierPTY/raw/main/screen_shots/htop.png" alt="screen" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglierPTY/raw/main/screen_shots/login.png" alt="screen" width="400px">
  <hr><img src="https://github.com/scottpeterman/UglierPTY/raw/main/screen_shots/creds.png" alt="screen" width="400px">
</div>

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/scottpeterman/UglierPTY
    ```

2. Navigate into the project directory:

    ```bash
    cd UglierPTY
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary entry point for this POC is the `uglierpty.py` script. To launch the application:

If you cloned the repo
```bash
python run_test.py
```

If you installed via PIP
```bash
python -m uglierpty
or 
pythonw -m uglierpty
```


---
# SSH Terminal Flow

<!DOCTYPE html>
<html>
<head>
  <title>SSH Terminal Flow</title>
</head>
<body>

<h1>SSH Terminal Flow</h1>

<pre>
+--------------------+       +-------------------+       +-------------------+       +------------+       +------------------+
| SSHTerminalWidget  |       |    SSHLib Class   |       |  Communication    |       |    pyte    |       | Remote SSH Host  |
|                    |       |                   |       |                   |       |            |       |                  |
|  keyPressEvent()   |------>|     write(data)   |------>|   sendDataToSSH() |------>|            |------>|   Shell Process  |
|                    |       |                   |       |                   |       |            |       |                  |
+--------------------+       +-------------------+       +-------------------+       +------------+       +------------------+
                ^                                       ^                          ^                           ^                     
                |                                       |                          |                           |                             
                |                                       |                          |                           |
                |                                       |                          |                           |
                |                                       |                          |                           |      
+--------------------+       +-------------------+       +-------------------+       +------------+       +------------------+
| SSHTerminalWidget  |       |    SSHLib Class   |       |  Communication    |       |    pyte    |       | Remote SSH Host  |
|                    |       |                   |       |                   |       |            |       |                  |
|    paintEvent()    |&lt;------|      read()       |&lt;------|  receiveDataFromSSH() |&lt;------|   feed()   |&lt;------|   Shell Process  |
|                    |       |                   |       |                   |       | stream.attach(screen) |       |                  |
+--------------------+       +-------------------+       +-------------------+       +------------+       +------------------+
</pre>

<h2>Step-by-Step Explanation:</h2>

<ol>
  <li><strong>Keystroke in SSHTerminalWidget:</strong> The <code>keyPressEvent()</code> function captures the keystroke and sends it to the <code>SSHLib</code> class via <code>write(data)</code>.</li>
  <li><strong>Sending to SSH Channel:</strong> The <code>write()</code> method sends the data through an SSH channel, probably utilizing <code>paramiko.SSHClient</code>. This is done in <code>Communication.sendDataToSSH()</code>.</li>
  <li><strong>SSH to Remote Host:</strong> The keystroke reaches the shell process running on the remote SSH host.</li>
  <li><strong>Remote Host to pyte:</strong> Once the shell process echoes the output, it's read by <code>Communication.receiveDataFromSSH()</code> and fed to pyte's <code>Stream</code> object via <code>feed()</code> in <code>SSHLib.read()</code>.</li>
  <li><strong>pyte to GUI:</strong> The <code>Stream</code> object updates the <code>Screen</code> object, which the <code>SSHTerminalWidget.paintEvent()</code> method uses to draw on the GUI, completing the round trip.</li>
</ol>

</body>
</html>
