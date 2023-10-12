# ui/main_window.py
import sys

from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QSplitter, QStackedWidget, QTextBrowser, QWidget, QVBoxLayout, \
    QLabel, QTabWidget, QFileDialog, QDialog, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from uglierpty.session_manager.session_manager import SessionManager
from uglierpty.terminal.widget import SSHTerminal, SSHTerminalWidget

from uglierpty.ui.creds_widget import CredentialsManagerWidget as Ui_Creds
welcome_html = '''
<style>
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .container {
    text-align: center;
  }

  h1 {
    color: #FF9800;

  }

  p {
    color: #607D8B;
    text-align: left;
  }

  ul {
    color: #4CAF50;
    text-align: left;
    list-style-position: inside;
    padding-left: 0;
  }

  li {
    color: #2196F3;
  }
</style>

<body>
  <div class="container">
    <h1>UglierPTY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h1>
    <p>
      <b>UglierPTY</b> is a <span style="color: #FF9800;">PyQt6-based</span> an even uglier version of PuTTY that provides a user interface for interacting with terminals and managing sessions.
    </p>
    
  </div>
</body>

'''


class MainWindow(QMainWindow):
    def closeEvent(self, event):
        print(f"close Event Fired")
        tabs_to_close = []
        close_confirmed = True
        self.isClosing = True
        # Determine which tabs to close
        for index in range(self.tabs.count()):
            tabs_to_close.append(index)
        # Close the tabs
        print("closing open sessions...")
        for index in reversed(tabs_to_close):  # Reverse to avoid index issues when removing tabs
            self.tabs.setCurrentIndex(index)
            close_confirmed = self.close_tab(index)
            if not close_confirmed:
                event.ignore()
                return
        print(f"time to close the window")
        event.accept()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.isClosing = False

        self.setWindowTitle("SSH Client")
        self.setGeometry(200, 200, 800, 600)
        self.center_on_screen()
        # Menubar setup
        menubar = QMenuBar()
        file_menu = QMenu("File", self)
        options_menu = QMenu("Options", self)
        help_menu = QMenu("Help", self)
        self.isCLosing = False
        # open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(sys.exit)
        settings_action = QAction("Credentials", self)
        settings_action.triggered.connect(self.showSettings)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        load_sessions_action = QAction("Load Sessions", self)
        file_menu.addAction(load_sessions_action)
        load_sessions_action.triggered.connect(self.load_sessions_dialog)

        # file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        options_menu.addAction(settings_action)
        help_menu.addAction(about_action)

        menubar.addMenu(file_menu)
        menubar.addMenu(options_menu)
        menubar.addMenu(help_menu)
        self.setMenuBar(menubar)

        # Vertical Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        # Second number corresponds to the size of self.stack_widget

        # TreeWidget for session management
        self.tree_widget = SessionManager(self)
        self.tree_widget.setHeaderLabel("Sessions")
        self.tree_widget.sessionSelected.connect(self.initialize_session)

        # StackWidget
        self.stack_widget = QStackedWidget()
        text_browser = QTextBrowser()
        text_browser.setHtml(welcome_html)

        tab_area = QWidget()
        tab_layout = QVBoxLayout()

        self.message_label = QLabel("")
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        tab_layout.addWidget(self.tabs)
        tab_layout.addWidget(self.message_label)
        tab_area.setLayout(tab_layout)

        self.stack_widget.addWidget(text_browser)
        self.stack_widget.addWidget(tab_area)

        splitter.addWidget(self.tree_widget)
        splitter.addWidget(self.stack_widget)

        self.setCentralWidget(splitter)
        self.tree_widget.load_sessions_from_yaml("./sessions/sessions.yaml")
        splitter.setSizes([200, 600])

    def center_on_screen(self):
        screen = self.screen()  # get the screen where this widget is displayed
        screen_geometry = screen.geometry()  # get the screen geometry
        center_point = screen_geometry.center()  # find its center point

        frame_geometry = self.frameGeometry()  # get the frame geometry of the main window
        frame_geometry.moveCenter(
            center_point)  # set the center point of frame_geometry to the center point of the screen

        self.move(frame_geometry.topLeft())

    def closeApp(self):
        self.isClosing = True
        self.close()

    def showSettings(self):
        credsapp = Ui_Creds()
        credsapp.show()


    def showAbout(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About")
        layout = QVBoxLayout()
        content = '''<!DOCTYPE html>
<html>
<head>
    <title>UglierPTY - Uglier than UglyPTY</title>
</head>
<body>

<h1>UglierPTY: A Technical Overview</h1>

<h2>Architecture Analysis</h2>

<ol>
    <li>
        <h3>Pyte for Terminal Emulation:</h3>
        <p>Headless screen emulation. Pyte can efficiently parse terminal output and virtually render it.</p>
    </li>
    <li>
        <h3>SQLAlchemy for Credentials Management:</h3>
        <p>This fits well for managing secure user credentials and allows for future scalability.</p>
    </li>
    <li>
        <h3>PyYAML for Configuration:</h3>
        <p>For human-readable session files</p>
    </li>
</ol>

<h2>Modular Design</h2>

<pre>
└───uglierpty
    ├───dialogs
    │   
    ├───session_manager
    │   
    ├───terminal
    │   
    ├───ui
    │   
    ├───utils
</pre>

</body>
</html>

'''
        text_browser = QTextBrowser()
        text_browser.setHtml(content)
        layout.addWidget(text_browser)

        about_dialog.setLayout(layout)
        about_dialog.setFixedSize(400, 400)
        about_dialog.exec()

    def show_disconnect_confirm(self,tab_to_remove):
        msg = QMessageBox(text=f"Session to {tab_to_remove.host} is active, disconnect?", parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok |
                               QMessageBox.StandardButton.Cancel)
        msg.setInformativeText("Disconnect?")
        return msg.exec()

    def close_tab(self, index):
        tab_to_remove = self.tabs.widget(index)  # Get the QWidget from the tab to be closed

        # Check if the session is active, you can implement is_session_active() based on your needs
        if self.is_session_active(tab_to_remove):
            try:

                reply = self.show_disconnect_confirm(tab_to_remove)
                if reply == QMessageBox.StandardButton.Ok:
                    print("closing tab...")
                    if self.isClosing:
                        return True
                    else:
                        self.cleanup(tab_to_remove)
                        self.tabs.removeTab(index)
                else:
                    return False
            except Exception as e:
                print(e)
        # Call your existing cleanup method to properly close the SSH session and perform other teardown activities
        self.cleanup(tab_to_remove)
        self.tabs.removeTab(index)

    def is_session_active(self, tab):
        # Implement your logic to check if the SSH session in the tab is active.
        # For example, you might check whether the SSH channel is open.
        try:
            return not tab.backend.channel.closed
        except:
            return False

    def initialize_session(self, session_data):
        new_tab = SSHTerminal(
            host=session_data['host'],
            user=session_data['username'],
            password=session_data['password'],
            port=session_data['port']
        )
        index =self.tabs.addTab(new_tab, session_data['display_name'])
        tab = self.tabs.widget(index)


    # Inside MainWindow class...

    def add_new_ssh_tab(self, refBinding, username, password):
        host = refBinding.get("host")
        ssh_widget = SSHTerminalWidget(parent=self, host=host, user=username, password=password, port=22)
        # temp_widget = QLabel("hello")
        # Connect the signal from SSHTerminalWidget to a slot in MainWindow
        ssh_widget.ssh_failed_upwards_signal.connect(self.handle_ssh_failure_at_mainwindow)

        tab_index = self.tabs.addTab(ssh_widget, refBinding.get("display_name"))

        self.stack_widget.setCurrentIndex(1)
        self.tabs.setCurrentIndex(tab_index)
        tab = self.tabs.widget(tab_index)
        ssh_widget.tab = tab
        # self.message_label.setText(f"connecting to {host}...")

    def handle_ssh_failure_at_mainwindow(self, error_message):
        # Show dialog that SSH login failed
        self.message_label.setText(f"{error_message}")
        QMessageBox.critical(self, "SSH Error", f"SSH login failed: {error_message}")

        # Find the failing SSH tab and remove it
        current_tab_index = self.tabs.currentIndex()
        active_tab = self.tabs.currentWidget()

        if isinstance(active_tab, SSHTerminalWidget):  # Adjust the type check as needed
            # Perform any cleanup before removing the tab
            self.cleanup(active_tab)
            self.tabs.removeTab(current_tab_index)
        self.message_label.setText(f"")

    def cleanup(self, tab_to_remove):
        tab_to_remove.backend.shutdown()  # Close the SSH session and stop its thread
        # Perform any other cleanup activities here

    def load_sessions_dialog(self):
        # options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Sessions File", "", "YAML Files (*.yaml);;All Files (*)",)
        if filePath:
            self.tree_widget.load_sessions_from_yaml(filePath)


