from PyQt6.QtWidgets import QApplication
from uglierpty.ui.main_window import MainWindow

app = QApplication([])
app.setStyle("fusion")
window = MainWindow()
window.show()
app.exec()