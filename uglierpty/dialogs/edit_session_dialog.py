from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox


class EditSessionDialog(QDialog):
    def __init__(self, session_item, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit SSH Session")
        self.session_item = session_item  # The tree item representing the session

        # Create layout and form
        self.layout = QFormLayout(self)

        # Existing fields
        self.displayNameLineEdit = QLineEdit(self)
        self.displayNameLineEdit.setText(self.session_item.refBinding['display_name'])

        self.hostLineEdit = QLineEdit(self)
        self.hostLineEdit.setText(self.session_item.refBinding['host'])

        self.hostPortEdit = QLineEdit(self)
        self.hostPortEdit.setText(self.session_item.refBinding.get('port', '22'))

        self.credsidLineEdit = QLineEdit(self)
        self.credsidLineEdit.setText(str(self.session_item.refBinding['credsid']))

        # New fields for the extended schema
        self.deviceTypeLineEdit = QLineEdit(self)
        self.deviceTypeLineEdit.setText(self.session_item.refBinding.get('DeviceType', ''))

        self.modelLineEdit = QLineEdit(self)
        self.modelLineEdit.setText(self.session_item.refBinding.get('Model', ''))

        self.serialNumberLineEdit = QLineEdit(self)
        self.serialNumberLineEdit.setText(self.session_item.refBinding.get('SerialNumber', ''))

        self.softwareVersionLineEdit = QLineEdit(self)
        self.softwareVersionLineEdit.setText(self.session_item.refBinding.get('SoftwareVersion', ''))

        self.vendorLineEdit = QLineEdit(self)
        self.vendorLineEdit.setText(self.session_item.refBinding.get('Vendor', ''))

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
