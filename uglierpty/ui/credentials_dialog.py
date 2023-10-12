import sqlite3

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QLineEdit, QPushButton, QDialogButtonBox
from PyQt6.QtCore import Qt

from uglierpty.terminal.widget import SSHTerminalWidget


class CredentialsDialog(QDialog):
    def __init__(self, username =None, password=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Credentials')
        self.parent = parent
        # Initialize layout
        layout = QVBoxLayout()
        self.username = username
        self.password = password
        # Initialize UI components
        self.comboCreds = QComboBox()
        self.checkManual = QCheckBox("Enter Credentials Manually")
        self.textUsername = QLineEdit()
        self.textPassword = QLineEdit()
        self.buttonKeyFile = QPushButton("Select Key File")

        # Initialize Form layout
        formLayout = QFormLayout()
        formLayout.addRow('Saved Credentials:', self.comboCreds)
        formLayout.addRow(self.checkManual)

        # Add initially hidden rows for manual input
        self.manualUsernameRow = formLayout.addRow('Username:', self.textUsername)
        self.manualPasswordRow = formLayout.addRow('Password:', self.textPassword)
        # self.manualKeyFileRow = formLayout.addRow('Key File:', self.buttonKeyFile)

        # Initially hidden
        self.textUsername.setHidden(True)
        self.textPassword.setHidden(True)
        self.buttonKeyFile.setHidden(True)

        # Add Form layout to main layout
        layout.addLayout(formLayout)

        # OK and Cancel buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.buttonBox)

        # Connect signals to slots
        self.checkManual.stateChanged.connect(self.toggle_manual_input)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setLayout(layout)
        self.populate_credentials_combo_box()

    def accept(self):
        if self.checkManual.isChecked():
            self.parent.username = self.textUsername.text()
            self.parent.password = self.textPassword.text()

            # Here, you would also collect the key file information if you need it
        else:
            selected_id = self.comboCreds.currentData()
            self.parent.username, self.parent.password = self.get_credentials_from_db(selected_id)

        # Signal or directly call a function to instantiate SSHWidget

        super(CredentialsDialog, self).accept()

    def get_credentials_from_db(self, cred_id):
        conn = sqlite3.connect('settings.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM creds WHERE id=?", (cred_id,))
        credentials = cursor.fetchone()
        conn.close()
        return credentials if credentials else (None, None)



    def toggle_manual_input(self, state):
        checked = self.checkManual.isChecked()
        print(checked)
        self.textUsername.setVisible(checked)
        self.textPassword.setVisible(checked)
        # self.buttonKeyFile.setVisible( checked)

    def populate_credentials_combo_box(self):
        conn = sqlite3.connect('settings.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id, displayname FROM creds")
        records = cursor.fetchall()
        conn.close()

        for record in records:
            id, displayname = record
            self.comboCreds.addItem(displayname, id)