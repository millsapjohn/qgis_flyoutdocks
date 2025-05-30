from qgis.PyQt.QtWidgets import (
    QToolBar,
    QAction,
    QToolButton,
    QWidget,
    QSizePolicy,
    QDockWidget,
    QWidgetAction,
)
from qgis.PyQt.QtCore import Qt
from .custombutton import RotatedButton


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
        for button in self.findChildren((RotatedButton, QToolButton)):
            if button.text() == panel.windowTitle():
                return
        try:
            action = QAction(panel.windowTitle(), self)
            action.setToolTip(panel.windowTitle())
            button = QToolButton(self)
            button.setText(panel.windowTitle())
            button.setToolButtonStyle(Qt.ToolButtonTextOnly)
            button.setDefaultAction(action)
            button.clicked.connect(lambda: self.panelState(panel))
            self.addWidget(button)
        except Exception as e:
            print(e)

    def removePanel(self, panel):
        remove_action = None
        for action in self.actions():
            if isinstance(action, QWidgetAction):
                widget = action.defaultWidget()
                if isinstance(widget, (RotatedButton, QToolButton)) and widget.text() == panel.windowTitle():
                    remove_action = action
                    break
        if remove_action:
            self.removeAction(remove_action)
            remove_action.deleteLater()
