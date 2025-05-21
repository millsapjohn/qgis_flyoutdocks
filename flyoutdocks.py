from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtWidgets import QDockWidget, QMainWindow
from qgis.PyQt.QtCore import Qt, QObject, QEvent, pyqtSignal
from qgis.utils import iface
import os
from .flyoutpanels import CustomPanel

class FlyoutDocksPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.settings = QgsSettings()
        self.instance = QgsApplication.instance()
        self.initGui()
        
    def initGui(self):
        self.mw = self.iface.mainWindow()
        self.dock_monitor = DockMonitor(self.mw)
        self.mw.installEventFilter(self.dock_add_monitor)
        self.dock_monitor.dockWidgetAdded.connect(self.processNewDock)
        self.dock_monitor.dockWidgetMoved.connect(self.processDockMovement)
        self.dock_monitor.dockWidgetFloatChanged.connect(self.processLevelChange)
        self.docks = self.mw.findChildren(QDockWidget)
        self.left_docks = []
        self.right_docks = []
        self.upper_docks = []
        self.lower_docks = []
        for dock in self.docks:
            self.processDock(dock)
        self.loadDocks()
        
    def unload(self):
        if self.left_dock:
            self.iface.removeDockWidget(self.left_dock)
            del self.left_dock
        if self.right_dock:
            self.iface.removeDockWidget(self.right_dock)
            del self.right_dock
        if self.upper_dock:
            self.iface.removeDockWidget(self.upper_dock)
            del self.upper_dock
        if self.lower_dock:
            self.iface.removeDockWidget(self.lower_dock)
            del self.lower_dock
        if self.mw and self.dock_monitor:
            self.mw.removeEventFilter(self.dock_monitor)

    def processDock(self, dock):
        if self.mw.dockWidgetArea(dock) == 1:
            self.left_docks.append(dock)
        elif self.mw.dockWidgetArea(dock) == 2:
            self.right_docks.append(dock)
        elif self.mw.dockWidgetArea(dock) == 4:
            self.upper_docks.append(dock)
        elif self.mw.dockWidgetArea(dock) == 8:
            self.lower_docks.append(dock)
        else:
            pass

    def loadDocks(self):
        if self.left_dock:
            self.mw.removeDockWidget(self.left_dock)
            del self.left_dock
        if self.right_dock:
            self.mw.removeDockWidget(self.right_dock)
            del self.right_dock
        if self.upper_dock:
            self.mw.removeDockWidget(self.upper_dock)
            del self.upper_dock
        if self.lower_dock:
            self.mw.removeDockWidget(self.lower_dock)
            del self.lower_dock
        if self.left_docks != []:
            self.left_dock = CustomPanel(self.iface, self.left_docks, 'Left Dock')
        if self.left_dock:
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        if self.right_docks != []:
            self.right_dock = CustomPanel(self.iface, self.right_docks, 'Right Dock')
        if self.right_dock:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.left_dock)
        if self.upper_docks != []:
            self.upper_dock = CustomPanel(self.iface, self.upper_panels, 'Upper Dock')
        if self.upper_dock:
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.upper_dock)
        if self.lower_docks != []:
            self.lower_dock = CustomPanel(self.iface, self.lower_docks, 'Lower Dock')
        if self.lower_dock:
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.lower_dock)

    def processNewDock(self, dock):
        self.processDock(dock)


class DockAddMonitor(QObject):
    
    dockWidgetAdded = pyqtSignal(QDockWidget)
    dockWidgetMoved = pyqtSignal(QDockWidget, Qt.DockWidgetArea)
    dockWidgetFloatChanged = pyqtSignal(QDockWidget, bool)
    
    def eventFilter(self, o, e):
        if e.type() == QEvent.ChildAdded:
            child = e.child()
            if isinstance(o, QMainWindow) and isinstance(child, QDockWidget):
                self.dockWidgetAdded.emit(child)
                child.dockLocationChanged.connect(
                    lambda area, child: self.on_location_changed(child, area)
                )
                child.topLevelChanged.connect(
                    lambda level, child: self.on_level_changed(child, level)
                )

        return super().eventFilter(o, e)

    def on_location_changed(self, widget, area):
        self.dockWidgetMoved.emit(widget, area)

    def on_level_changed(self, widget, level):
        self.dockWidgetFloatChanged.emit(widget, level)
