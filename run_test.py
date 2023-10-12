from uglierpty.ui.main_window import MainWindow

# __main__.py
from PyQt6.QtWidgets import QApplication
from uglierpty.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("fusion")
    window = MainWindow()
    window.show()
    app.exec()
