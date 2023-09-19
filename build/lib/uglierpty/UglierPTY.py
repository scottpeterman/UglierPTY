import sys
import traceback
from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QPushButton

# Importing SSHTerminal from your custom module
from uglierpty.terminal.widget import SSHTerminal

# Function to show a dialog for collecting credentials
def get_credentials():
    dialog = QDialog()  # Creating a new QDialog instance
    dialog.setWindowTitle('Enter Credentials')  # Setting the window title

    layout = QFormLayout()  # Using a form layout for the dialog

    # Creating QLineEdit widgets for host, user, and password
    host_edit = QLineEdit()
    user_edit = QLineEdit()
    password_edit = QLineEdit()
    password_edit.setEchoMode(QLineEdit.EchoMode.Password)  # Password should be hidden

    # Adding the widgets to the form layout
    layout.addRow('Host:', host_edit)
    layout.addRow('Username:', user_edit)
    layout.addRow('Password:', password_edit)

    submit_button = QPushButton('Submit')  # Create a submit button
    layout.addRow(submit_button)  # Add the submit button to the layout

    dialog.setLayout(layout)  # Set the layout for the dialog

    # Define action when submit button is clicked
    def on_submit():
        dialog.accept()

    # Connect button click to the action
    submit_button.clicked.connect(on_submit)

    # Show the dialog and wait for user action
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return host_edit.text(), user_edit.text(), password_edit.text()
    else:
        return None, None, None  # Return None if user cancels or closes the dialog

# Main function where the application starts
def main():
    app = QApplication(sys.argv)  # Initialize the application
    app.setStyle("fusion")  # Set the style

    host, user, password = get_credentials()  # Get credentials from user

    if host and user and password:  # Proceed only if we have valid credentials
        win = SSHTerminal(host=host, user=user, password=password)  # Create terminal window
        win.show()  # Show the terminal window
        win.message_label.show()  # Show message label (if applicable)
        win.setWindowTitle(f"Uglier SSH")
        try:
            app.exec()  # Run the main event loop of the application

            # Close and clean up after event loop exits
            if win.term.backend and win.term.backend.channel:
                win.term.backend.listener.stop()
                if not win.term.backend.channel.closed:
                    win.term.backend.listener.shutdown()

            win.term.backend = None  # Clear the terminal backend
            app.quit()  # Quit the application
            app = None  # Remove the app instance
            print("Application closing")

        except Exception as e:
            print(f"App exec exception: {e}")  # Print any exceptions that occur
            traceback.print_exc()
    else:
        print("Cancelled by user")  # If user cancelled the credential dialog

# Start the application
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Closing exception: {e}")
        traceback.print_exc()  # Print full traceback for unhandled exceptions
