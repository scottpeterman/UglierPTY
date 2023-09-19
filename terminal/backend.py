import paramiko
import uuid
import threading
import select
import time
from pyte.screens import Screen, HistoryScreen
from pyte.streams import ByteStream

# Custom Stream class inheriting from pyte's ByteStream
class TermStream(ByteStream):
    def __init__(self, *args, **kwargs):
        super(TermStream, self).__init__(*args, **kwargs)

# Communication class for handling backend SSH connection
class Communication(object):
    def __init__(self):
        self.backend = None  # Backend object (SSHLib)
        self.stop_flag = False  # Flag to stop the thread
        self.thread = threading.Thread(target=self.listen)  # Create a new thread for listening
        self.thread.start()  # Start the thread

    # Sets the backend for the Communication
    def set_backend(self, backend):
        self.backend = backend
        # Restart the thread if it was stopped
        if self.stop_flag:
            self.stop_flag = False
            self.thread = threading.Thread(target=self.listen)
            self.thread.start()

    # Shuts down the Communication and its backend
    def shutdown(self):
        if self.backend:
            self.backend.close()
            self.backend = None
            self.stop()

    # Stop the listener thread
    def stop(self):
        self.stop_flag = True
        if self.thread.is_alive():
            self.thread.join()

    # Main listen loop to handle incoming data
    def listen(self):
        while not self.stop_flag:
            if self.backend:
                try:
                    # Wait for data to read
                    read_ready, _, _ = select.select([self.backend.get_read_wait()], [], [], 1)
                    if read_ready:
                        self.backend.read()  # Read the data
                except:
                    pass
            else:
                time.sleep(1)

# Custom Screen class inheriting from pyte's HistoryScreen
class Canvas(HistoryScreen):
    pass

# Base class for backend types
class BaseBackend(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = Canvas(width, height, history=9999, ratio=.3)  # Initialize screen with Canvas
        self.stream = TermStream(self.screen)  # Initialize stream with custom TermStream
        self.id = str(uuid.uuid4())  # Generate a unique identifier

    def write_to_screen(self, data):
        self.stream.feed(data)  # Feed data to the pyte screen

    def read(self):
        pass

    # Resizes the terminal screen dimensions
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.screen.resize(columns=width, lines=height)

    def connect(self):
        pass

    def get_read_wait(self):
        pass

    def cursor(self):
        return self.screen.cursor

    def close(self):
        pass

# Empty PtyBackend class inheriting from BaseBackend
class PtyBackend(BaseBackend):
    pass

# SSHLib class handling SSH connections
class SSHLib(BaseBackend):
    def __init__(self, width, height, ip, username=None, password=None):
        super(SSHLib, self).__init__(width, height)
        self.ip = ip
        self.username = username
        self.password = password
        self.thread = threading.Thread(target=self.connect)
        self.ssh_client = None
        self.channel = None
        self.thread.start()
        self.listener = Communication()  # Create a listener object

    # Connect to the SSH server
    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.ip, username=self.username, password=self.password)
        self.channel = self.ssh_client.get_transport().open_session()
        self.channel.get_pty(term='xterm', width=self.width, height=self.height)
        self.channel.invoke_shell()
        timeout = 60
        while not self.channel.recv_ready() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        self.channel.resize_pty(width=self.width, height=self.height)
        self.listener.set_backend(self)  # Set this backend as the listener's backend

    # Return the channel to read from
    def get_read_wait(self):
        return self.channel

    # Send data over the SSH channel
    def write(self, data):
        self.channel.send(data)

    # Read from the SSH channel
    def read(self):
        output = self.channel.recv(1024)
        self.write_to_screen(output)  # Write the output to the pyte screen

    # Resize the SSH terminal
    def resize(self, width, height):
        super(SSHLib, self).resize(width, height)
        if self.channel:
            self.channel.resize_pty(width=width, height=height)

    # Close the SSH channel
    def close(self):
        if self.channel.closed:
            return
        else:
            self.listener.shutdown()
