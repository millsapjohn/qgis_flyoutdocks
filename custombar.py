from qgis.PyQt.QtWidgets import (
    QToolBar,
    QPushButton,
)
from qgis.utils import iface
from qgis.core import QgsApplication

class CustomBar(QToolBar):
    def __init__(self, iface, panels, title):
        super().__init__()
        self.setObjectName(title)
        self.setWindowTitle(title)
        self.iface = iface
        self.mw = iface.mainWindow()
        for panel in panels:
            self.addPanel(panel)

    def panelState(self, panel):
        if panel.isVisible():
            panel.setVisible(False)
        else:
            panel.setVisible(True)

    def addPanel(self, panel):
        button = QPushButton(panel.windowTitle())
        # TODO: set button orientation to vertical
        button.clicked.connect(lambda: self.panelState(panel))
        self.layout.addWidget(button)

    def removePanel(self, panel):
        child = self.layout.findChild(QPushButton, panel.windowTitle())
        child.clicked.disconnect(self.panelState)
        self.layout.removeWidget(child)
