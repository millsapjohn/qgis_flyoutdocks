from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtWidgets import QDockWidget, QMainWindow, QAction
from qgis.PyQt.QtCore import Qt, QObject, QEvent, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
import os
from .flyoutpanels import CustomPanel
from .ignoredialog import IgnoreDialog

plugin_icon = QIcon(':/images/themes/default/console/iconHideToolConsole.svg')

class FlyoutDocksPlugin:
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.settings = QgsSettings()
        self.instance = QgsApplication.instance()
        self.initGui()
        
    def initGui(self):
        self.showHideAction = QAction(plugin_icon, 'Show/Hide Dock Widgets')
        self.iface.addPluginToMenu('Manage Dock Widgets', self.showHideAction)
        self.showHideAction.triggered.connect(self.setShowHide)
        self.mw = self.iface.mainWindow()
        self.dock_monitor = DockMonitor(self.mw)
        self.mw.installEventFilter(self.dock_add_monitor)
        self.dock_monitor.dockWidgetAdded.connect(self.processNewDock)
        self.dock_monitor.dockWidgetMoved.connect(self.processMoveDock)
        self.dock_monitor.dockWidgetFloatChanged.connect(self.processFloatDock)
        self.docks = self.mw.findChildren(QDockWidget)
        if not self.hide_docks:
            self.hide_docks = []
        if not self.show_docks:
            self.show_docks = self.docks
        for dock in self.docks:
            dock.isHidden(True)
        self.left_docks = []
        self.right_docks = []
        self.upper_docks = []
        self.lower_docks = []
        for dock in self.docks:
            self.processDock(dock)
        self.loadDocks()
        
    def unload(self):
        self.iface.removePluginMenu('Manage Dock Widgets', self.showHideAction)
        del self.showHideAction
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
        if dock in self.hide_docks:
            pass
        else:
            match self.mw.dockWidgetArea(dock):
                case 1:
                    self.left_docks.append(dock)
                case 2:
                    self.right_docks.append(dock)
                case 4:
                    self.upper_docks.append(dock)
                case 8:
                    self.lower_docks.append(dock)
                case _:
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
        self.docks.append(dock)
        self.processDock(dock)
        self.loadDocks()

    def processMoveDock(self, dock):
        if dock in self.left_docks:
            self.left_docks.remove(dock)
        elif dock in self.right_docks:
            self.right_docks.remove(dock)
        elif dock in self.upper_docks:
            self.upper_docks.remove(dock)
        elif dock in self.lower_docks:
            self.lower_docks.remove(dock)
        else:
            pass
        self.processDock(dock)
        self.loadDocks()

    def processFloatDock(self, dock, level):
        if dock in self.left_docks:
            self.left_docks.remove(dock)
        elif dock in self.right_docks:
            self.right_docks.remove(dock)
        elif dock in self.upper_docks:
            self.upper_docks.remove(dock)
        elif dock in self.lower_docks:
            self.lower_docks.remove(dock)
        else:
            pass
        # TODO: check this
        if level == 0:
            pass
        else:
            self.processDock(dock)
            self.loadDocks()

    def setShowHide(self):
        dialog = IgnoreDialog(self.show_docks, self.hide_docks)
        dialog.exec()
        if dialog.success == True:
            self.show_docks = dialog.show_panels
            self.hide_docks = dialog.hide_panels
            for dock in self.docks:
                self.processDock(dock)
            self.loadDocks()


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
