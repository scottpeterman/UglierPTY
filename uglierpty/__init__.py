welcome_page = '''
<!DOCTYPE html>
<html>
<head>
    <title>PyQt6 SSH Terminal Widget: UglierPTY</title>
</head>
<body>

<h1>PyQt6 SSH Terminal Widget: UglierPTY</h1>

<h2>Overview</h2>
<p>
UglierPTY is a very functional proof-of-concept (POC) application created to construct a fully functional SSH Terminal Widget using PyQt6. This POC is inspired by its sister project, UglyPTY, a full-featured SSH client that utilizes xterm.js. The aim is to offer a similar, if not superior, feature set without relying on browser technologies or JavaScript, resulting in a more streamlined and resource-efficient solution.
</p>
<p>
This is a work in progress, but feel free to give it a try!
<a href="https://github.com/scottpeterman/UglierPTY">REPO</a>
</p>

<h4>A Note About UglyPTY</h4>
<p>
If you're interested in the PyQt6/XTerm.js version of this application, take a look <a href="https://github.com/scottpeterman/UglyPTY">here</a>.
</p>

<h2>Features</h2>
<ul>
    <li>Fully functional SSH terminal built with PyQt6</li>
    <li>Credentials manager for easy login</li>
    <li>Portable session files in YAML (Compatible with UglyPTY)</li>
    <li>Terminal history and screen ratio control via pyte</li>
    <li>Terminal screen render via QPaint</li>
    <li>Modular design for easy embedding into other PyQt6 projects</li>
    <li>Pure Python - Free of Web technology (no xterm.js)</li>
</ul>

<h2>Architecture</h2>
<ul>
    <li>Python 3.x</li>
    <li>PyQt6</li>
    <li>Paramiko</li>
    <li>pyte</li>
    <li>SQLAlchemy</li>
    <li>PyYaml</li>
</ul>


<h2>Installation</h2>
<ol>
    <li>Clone the repository:</li>
    <pre><code>git clone https://github.com/scottpeterman/UglierPTY</code></pre>
    <li>Navigate into the project directory:</li>
    <pre><code>cd UglierPTY</code></pre>
    <li>Install the required Python packages:</li>
    <pre><code>pip install -r requirements.txt</code></pre>
</ol>

<h2>Usage</h2>
<p>
The primary entry point for this POC is the <code>uglierpty.py</code> script. To launch the application:
</p>
<p>If you cloned the repo</p>
<pre><code>python run_test.py</code></pre>
<p>If you installed via PIP</p>
<pre><code>python -m uglierpty</code></pre>
<pre><code>pythonw -m uglierpty</code></pre>

<hr>

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
'''
