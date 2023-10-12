from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class SessionContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionEditSession = QAction("Edit", self)
        self.actionAddSession = QAction("Add", self)
        self.actionDeleteSession = QAction("Delete", self)
        self.actionCopySession = QAction("Copy", self)
        self.actionCutSession = QAction("Cut", self)

        self.addAction(self.actionEditSession)
        self.addAction(self.actionAddSession)
        self.addAction(self.actionDeleteSession)
        self.addAction(self.actionCopySession)
        self.addAction(self.actionCutSession)


class FolderContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionAddSession = QAction("Add Session", self)
        self.actionRenameFolder = QAction("Rename Folder", self)
        self.actionDeleteFolder = QAction("Delete Folder", self)
        self.actionPaste = QAction("Paste", self)

        self.addAction(self.actionAddSession)
        self.addAction(self.actionRenameFolder)
        self.addAction(self.actionDeleteFolder)
        self.addAction(self.actionPaste)


class RootContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.actionNewFolder = QAction("New Folder", self)
        self.addAction(self.actionNewFolder)

