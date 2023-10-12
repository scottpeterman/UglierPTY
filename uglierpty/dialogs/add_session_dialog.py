from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class AddSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add SSH Session")

        # Create layout and form
        self.layout = QFormLayout(self)

        # Fields
        self.displayNameLineEdit = QLineEdit(self)
        self.hostLineEdit = QLineEdit(self)
        self.hostPortEdit = QLineEdit(self)
        self.credsidLineEdit = QLineEdit(self)
        self.deviceTypeLineEdit = QLineEdit(self)
        self.modelLineEdit = QLineEdit(self)
        self.serialNumberLineEdit = QLineEdit(self)
        self.softwareVersionLineEdit = QLineEdit(self)
        self.vendorLineEdit = QLineEdit(self)

        # Add rows
        self.layout.addRow("Display Name", self.displayNameLineEdit)
        self.layout.addRow("Host", self.hostLineEdit)
        self.layout.addRow("Port", self.hostPortEdit)
        self.layout.addRow("Credsid", self.credsidLineEdit)
        self.layout.addRow("Device Type", self.deviceTypeLineEdit)
        self.layout.addRow("Model", self.modelLineEdit)
        self.layout.addRow("Serial Number", self.serialNumberLineEdit)
        self.layout.addRow("Software Version", self.softwareVersionLineEdit)
        self.layout.addRow("Vendor", self.vendorLineEdit)

        # Buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addRow(self.buttonBox)
