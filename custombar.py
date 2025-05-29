from qgis.PyQt.QtWidgets import (
    QToolBar,
    QAction,
    QToolButton,
    QWidget,
    QSizePolicy,
    QDockWidget,
)
from qgis.PyQt.QtGui import (
    QIcon,
)
from qgis.PyQt.QtCore import Qt


button_icon = QIcon(':/themes/default/console/iconHideToolConsole.svg')


class CustomBar(QToolBar):
    def __init__(self, iface, panels, title, parent=None):
        super().__init__(title, parent)
        self.setObjectName(title)
        self.iface = iface
        self.mw = iface.mainWindow()
        self.tb_orientation = self.orientation()
        self.left_spacer = QWidget(self)
        self.left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(self.left_spacer)
        for panel in panels:
            self.addPanel(panel)
        self.right_spacer = QWidget(self)
        self.right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(self.right_spacer)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def panelState(self, panel):
        if panel.isVisible():
            panel.setVisible(False)
        else:
            for dock in self.mw.findChildren(QDockWidget):
                dock.setVisible(False)
            panel.setVisible(True)

    def addPanel(self, panel):
        for action in self.actions():
            if action.text() == panel.windowTitle():
                return
        try:
            action = QAction(button_icon, panel.windowTitle(), self)
            action.triggered.connect(lambda: self.panelState(panel))
            self.addAction(action)
        except Exception as e:
            print(e)

    def removePanel(self, panel):
        for action in self.actions():
            if action.text() == panel.windowTitle():
                self.removeAction(action)
                action.deleteLater()
                break
