import copy
import os

from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog
import yaml
import sqlite3



from uglierpty.dialogs.edit_session_dialog import EditSessionDialog
from uglierpty.dialogs.add_session_dialog import AddSessionDialog
from uglierpty.ui.context_menus import SessionContextMenu, FolderContextMenu, RootContextMenu
from uglierpty.ui.credentials_dialog import CredentialsDialog


class SessionManager(QTreeWidget):
    # Define custom signal
    sessionSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SessionManager, self).__init__(parent)
        self.clipboard = None
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.main_window = parent

        # Initialize context menus
        self.sessionContextMenu = SessionContextMenu(self)
        self.folderContextMenu = FolderContextMenu(self)
        self.rootContextMenu = RootContextMenu(self)

        # Connect context menu actions to slots (replace with your methods)
        self.sessionContextMenu.actionEditSession.triggered.connect(self.edit_session)
        self.sessionContextMenu.actionAddSession.triggered.connect(self.add_session)
        self.sessionContextMenu.actionDeleteSession.triggered.connect(self.delete_session)
        self.sessionContextMenu.actionCopySession.triggered.connect(self.copy_session)
        self.sessionContextMenu.actionCutSession.triggered.connect(self.cut_session)
        self.folderContextMenu.actionAddSession.triggered.connect(self.add_session)
        self.folderContextMenu.actionRenameFolder.triggered.connect(self.rename_folder)
        self.folderContextMenu.actionDeleteFolder.triggered.connect(self.delete_folder)
        self.rootContextMenu.actionNewFolder.triggered.connect(self.new_folder)
        self.folderContextMenu.actionPaste.triggered.connect(self.paste)


        # Connect context menu to be shown
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.setHeaderLabel("Sessions")
        # Placeholder sessions
        self.populate_sessions()

        # Connect item selection signal to custom slot
        # self.itemClicked.connect(self.session_clicked)


        self.itemDoubleClicked.connect(self.on_item_double_click)

    def on_item_double_click(self, item):
        if hasattr(item, 'is_leaf_item') and item.is_leaf_item:
            self.username = None
            self.password = None
            dialog = CredentialsDialog(parent=self)
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                # Handle accepted dialog
                # For example, proceed with opening the SSH terminal tab

                self.main_window.add_new_ssh_tab(refBinding=item.refBinding, username=self.username, password=self.password)



    def show_context_menu(self, position):
        try:
            item = self.itemAt(position)
            global_pos = self.viewport().mapToGlobal(position)

            if item:
                if item.is_folder:  # Replace with your logic for folder detection
                    self.folderContextMenu.exec(global_pos)
                else:
                    self.sessionContextMenu.exec(global_pos)
            else:
                self.rootContextMenu.exec(global_pos)
        except Exception as e:
            print(e)
        print("got here onContextMenut")
        # Hide context menus after 50ms
        QTimer.singleShot(50, self.sessionContextMenu.hide)
        QTimer.singleShot(50, self.folderContextMenu.hide)


    def paste(self):
        if not self.clipboard:
            return

        selected_item = self.currentItem()

        if selected_item and hasattr(selected_item, 'is_folder') and selected_item.is_folder:
            clipboard_action = self.clipboard['action']
            clipboard_item = self.clipboard['item'].clone()  # Clone the item

            # Deep copy refBinding from clipboard to new_item
            clipboard_item.refBinding = copy.deepcopy(self.clipboard['item'].refBinding)

            # Copy additional custom attributes
            clipboard_item.is_folder = self.clipboard['item'].is_folder
            clipboard_item.is_leaf_item = self.clipboard['item'].is_leaf_item

            # Check for uniqueness within the selected folder
            is_unique = True
            for child_index in range(selected_item.childCount()):
                child_item = selected_item.child(child_index)
                if clipboard_item.text(0) == child_item.text(0):
                    is_unique = False
                    break  # Exit loop as soon as a duplicate is found

            if is_unique:
                # Append the new_item as a child to the selected folder
                selected_item.addChild(clipboard_item)

                # If the action was 'cut', remove the original item
                if clipboard_action == 'cut':
                    (self.clipboard['item'].parent() or self.invisibleRootItem()).removeChild(self.clipboard['item'])
                # Clear the clipboard
                self.clipboard = None
            else:
                # Show a warning dialog for duplicate names
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setText(f"An item named '{clipboard_item.text(0)}' already exists in this folder.")
                msgBox.setWindowTitle("Duplicate Item")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
                msgBox.exec()



    def cut_session(self):
        selected_item = self.currentItem()
        if selected_item and hasattr(selected_item, 'is_leaf_item') and selected_item.is_leaf_item:
            self.clipboard = {'action': 'cut', 'item': selected_item}

    def copy_session(self):

        selected_item = self.currentItem()
        if selected_item and hasattr(selected_item, 'is_leaf_item') and selected_item.is_leaf_item:
            self.clipboard = {'action': 'copy', 'item': selected_item}

    def populate_sessions(self):
        print()

    # Custom slot
    def session_clicked(self, item):
        session_data = item.data(0, Qt.ItemDataRole.UserRole)
        if session_data:
            username, password = self.get_credentials(session_data['credsid'])
            session_data['username'] = username
            session_data['password'] = password
            self.sessionSelected.emit(session_data)

    def get_credentials(self, credsid):
        conn = sqlite3.connect('settings.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM creds WHERE id=?", (credsid,))
        credentials = cursor.fetchone()
        conn.close()
        return credentials if credentials else (None, None)


    def make_default_sessions(self, passedfile):
        file_path = passedfile
        if passedfile is None:
            file_path = "./sessions/sessions.yaml"
        # Check if the file exists
        if not os.path.exists(file_path):
            # If the directory doesn't exist, create it

            os.makedirs('./sessions')

            # Define the default content
            default_content = [
                {
                    "folder_name": "0 - Linux",
                    "sessions": [
                        {
                            "DeviceType": "Linux",
                            "Model": "NUC",
                            "SerialNumber": "",
                            "SoftwareVersion": "22.04",
                            "Vendor": "Ubuntu",
                            "credsid": "1",
                            "display_name": "Example",
                            "host": "10.0.0.12",
                            "port": "22"
                        }
                    ]
                }
            ]

            # Create the file with the default content
            with open(file_path, 'w') as file:
                yaml.safe_dump(default_content, file)
            return default_content

    def load_sessions_from_yaml(self, yaml_file="./sessions/sessions.yaml"):
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                from uglierpty.utils.db import create_db

        except:
            data = self.make_default_sessions(yaml_file)
        self.current_file = yaml_file

        for folder in data:
            folder_item = QTreeWidgetItem([folder['folder_name']])
            folder_item.is_folder = True
            folder_item.is_leaf_item = False
            self.addTopLevelItem(folder_item)

            for session in folder['sessions']:
                session_item = QTreeWidgetItem([session['display_name']])
                session_item.is_folder = False
                session_item.is_leaf_item = True
                session_item.refBinding = session
                folder_item.addChild(session_item)
                session_item.setData(0, Qt.ItemDataRole.UserRole, session)  # Store session data for later use

        # Placeholder methods for context menu actions

    import yaml

    def save_sessions_to_yaml(self, yaml_file=None):
        if yaml_file is None:
            yaml_file = self.current_file  # Using the file that was initially loaded

        root = self.invisibleRootItem()
        child_count = root.childCount()
        data_to_save = []

        for i in range(child_count):
            folder_item = root.child(i)
            folder_name = folder_item.text(0)

            folder_data = {
                'folder_name': folder_name,
                'sessions': []
            }

            session_count = folder_item.childCount()
            for j in range(session_count):
                session_item = folder_item.child(j)
                session_data = session_item.refBinding  # This holds the metadata for the session

                folder_data['sessions'].append(session_data)

            data_to_save.append(folder_data)

        # Write to YAML file
        with open(yaml_file, 'w') as f:
            yaml.safe_dump(data_to_save, f)

        print(f"Saved sessions to {yaml_file}")

    def edit_session(self):
        selected_item = self.currentItem()
        if not selected_item:
            print("No item selected for editing.")
            return

        edit_dialog = EditSessionDialog(selected_item, self)
        if edit_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Retrieve the updated session details from the dialog
            updated_data = {
                'display_name': edit_dialog.displayNameLineEdit.text(),
                'host': edit_dialog.hostLineEdit.text(),
                'port': edit_dialog.hostPortEdit.text(),
                'credsid': edit_dialog.credsidLineEdit.text(),
                'DeviceType': edit_dialog.deviceTypeLineEdit.text(),
                'Model': edit_dialog.modelLineEdit.text(),
                'SerialNumber': edit_dialog.serialNumberLineEdit.text(),
                'SoftwareVersion': edit_dialog.softwareVersionLineEdit.text(),
                'Vendor': edit_dialog.vendorLineEdit.text(),
            }

            # Update the item's display text in the QTreeWidget
            selected_item.setText(0, updated_data['display_name'])

            # Update the refBinding property with the new session details
            for key, value in updated_data.items():
                if key in selected_item.refBinding:
                    selected_item.refBinding[key] = value

            print("User accepted changes", updated_data)
            self.save_sessions_to_yaml(self.current_file)
        else:
            print("User canceled.")


    def delete_session(self):
        selected_item = self.currentItem()
        if not selected_item or not hasattr(selected_item, 'is_leaf_item') or not selected_item.is_leaf_item:
            print("No session item selected for deletion.")
            return

        parent_folder = selected_item.parent()
        if not parent_folder:
            print("Could not find parent folder.")
            return

        # Confirmation dialog
        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     f"Are you sure you want to delete the session '{selected_item.text(0)}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from the UI
            parent_folder.removeChild(selected_item)

            # Optionally, save the current tree state to your YAML file here.
            self.save_sessions_to_yaml(self.current_file)

            print(f"Deleted session {selected_item.text(0)}")
        else:
            print("Deletion canceled.")

    def add_session(self):
        selected_item = self.currentItem()
        if not selected_item or not selected_item.is_folder:
            print("No folder selected or the selected item is not a folder.")
            return

        add_dialog = AddSessionDialog(self)
        if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Collect the data
            new_data = {
                'display_name': add_dialog.displayNameLineEdit.text(),
                'host': add_dialog.hostLineEdit.text(),
                'port': add_dialog.hostPortEdit.text(),
                'credsid': add_dialog.credsidLineEdit.text(),
                'DeviceType': add_dialog.deviceTypeLineEdit.text(),
                'Model': add_dialog.modelLineEdit.text(),
                'SerialNumber': add_dialog.serialNumberLineEdit.text(),
                'SoftwareVersion': add_dialog.softwareVersionLineEdit.text(),
                'Vendor': add_dialog.vendorLineEdit.text(),
            }

            # Create a new QTreeWidgetItem and populate it
            new_item = QTreeWidgetItem([new_data['display_name']])
            new_item.is_folder = False
            new_item.is_leaf_item = True
            new_item.refBinding = new_data  # Setting the custom property
            selected_item.addChild(new_item)

            # You may want to save the new state
            self.save_sessions_to_yaml(self.current_file)

            print("New session added")
        else:
            print("User canceled.")


    def new_folder(self):
        new_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter new folder name:')

        if ok:
            root = self.invisibleRootItem()

            # Check for folder name uniqueness
            is_unique = True
            for child_index in range(root.childCount()):
                child_item = root.child(child_index)
                if new_name == child_item.text(0):
                    is_unique = False
                    break  # Exit loop as soon as a duplicate is found

            if is_unique:
                # Create and add the new folder
                folder_item = QTreeWidgetItem([new_name])
                folder_item.is_folder = True
                folder_item.is_leaf_item = False
                root.addChild(folder_item)

                # Optionally, save the current tree state to your YAML file here.
                self.save_sessions_to_yaml(self.current_file)
            else:
                # Show a warning dialog for duplicate folder names
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setText(f"A folder named '{new_name}' already exists.")
                msgBox.setWindowTitle("Duplicate Folder")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
                msgBox.exec()

    def rename_folder(self):
        selected_item = self.currentItem()
        if not selected_item or not hasattr(selected_item, 'is_folder') or not selected_item.is_folder:
            print("No folder item selected for renaming.")
            return

        new_name, ok = QInputDialog.getText(self, 'Rename Folder', 'Enter new folder name:', text=selected_item.text(0))

        if ok:

            try:
                selected_item.setText(0, new_name)
                # Optionally, save the current tree state to your YAML file here.
                self.save_sessions_to_yaml(self.current_file)
            except Exception as e:
                print(e)

    def delete_folder(self):
        selected_item = self.currentItem()
        if not selected_item or not hasattr(selected_item, 'is_folder') or not selected_item.is_folder:
            print("No folder item selected for deletion.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     f"Are you sure you want to delete the folder '{selected_item.text(0)}' and all its contents?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            root = self.invisibleRootItem()
            (selected_item.parent() or root).removeChild(selected_item)
            # Optionally, save the current tree state to your YAML file here.
            self.save_sessions_to_yaml(self.current_file)

