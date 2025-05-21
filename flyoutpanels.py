from qgis.PyQt.QtWidgets import (
    QWidget,
    QDockWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from qgis.utils import iface
from qgis.core import QgsApplication

class CustomPanel(QDockWidget):
    def __init__(self, iface, panels, title):
        super().__init__()
        self.setObjectName(title)
        self.iface = iface
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        for panel in panels:
            self.addPanel(panel)

    def panelState(self, panel):
        if panel.isVisible():
            panel.setVisible(False)
        else:
            panel.setVisible(True)

    def addPanel(self, panel):
        button = QPushButton(panel.windowTitle())
        button.clicked.connect(self.panelState(panel))
        self.layout.addWidget(button)

    def removePanel(self, panel):
        child = self.layout.findChild(QPushButton, panel.windowTitle())
        child.clicked.disconnect(self.panelState)
        self.layout.removeWidget(child)
