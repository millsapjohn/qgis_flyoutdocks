from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtWidgets import QDockWidget, QMainWindow, QAction
from qgis.PyQt.QtCore import Qt, QObject, QEvent, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
import os
from .custombar import CustomBar
from .ignoredialog import IgnoreDialog

plugin_icon = QIcon(':/images/themes/default/console/iconHideToolConsole.svg')

# TODO: set a variable to prevent reloading panels at startup


class FlyoutDocksPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.settings = QgsSettings()
        self.instance = QgsApplication.instance()
        self.hide_docks = None
        self.show_docks = None
        self.dock_bars = None
        self.initGui()
        
    def initGui(self):
        self.showHideAction = QAction(plugin_icon, 'Show/Hide Dock Widgets')
        self.iface.addPluginToMenu('Manage Dock Widgets', self.showHideAction)
        self.showHideAction.triggered.connect(self.setShowHide)
        self.mw = self.iface.mainWindow()
        self.dock_monitor = DockMonitor(self.mw)
        self.mw.installEventFilter(self.dock_monitor)
        self.dock_monitor.dockWidgetAdded.connect(self.processNewDock)
        self.dock_monitor.dockWidgetMoved.connect(self.processMoveDock)
        self.docks = self.mw.findChildren(QDockWidget)
        if not self.dock_bars:
            self.dock_bars = []
        if not self.hide_docks:
            self.hide_docks = []
        if not self.show_docks:
            self.show_docks = self.docks
        for dock in self.docks:
            dock.hide()
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
        if self.dock_bars == []:
            continue
        else:
            for bar in self.dock_bars:
                self.mw.removeToolBar(bar)
                del bar
        self.left_bar = CustomBar(self.iface, self.left_docks, 'Left Bar')
        self.mw.addToolbar(Qt.LeftToolBarArea, self.left_bar)
        self.dock_bars.append(self.left_bar)
        self.right_bar = CustomBar(self.iface, self.right_docks, 'Right Bar')
        self.mw.addToolBar(Qt.RightToolBarArea, self.left_bar)
        self.dock_bars.append(self.right_bar)
        self.upper_bar = CustomBar(self.iface, self.upper_docks, 'Upper Bar')
        self.mw.addToolBar(Qt.TopToolBarArea, self.upper_bar)
        self.dock_bars.append(self.upper_bar)
        self.lower_bar = CustomBar(self.iface, self.lower_docks, 'Lower Bar')
        self.mw.addToolBar(Qt.BottomToolBarArea, self.lower_bar)
        self.dock_bars.append(self.lower_bar)

    def processNewDock(self, dock):
        self.docks.append(dock)
        self.processDock(dock)
        match self.mw.dockWidgetArea(dock):
            case 1:
                self.left_bar.addPanel(dock)
            case 2:
                self.right_bar.addPanel(dock)
            case 4:
                self.upper_bar.addPanel(dock)
            case 8:
                self.lower_bar.addPanel(dock)
            case _:
                pass

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
        match self.mw.dockWidgetArea(dock):
            case 1:
                self.left_dock.addPanel(dock)
            case 2:
                self.right_dock.addPanel(dock)
            case 4:
                self.upper_dock.addPanel(dock)
            case 8:
                self.lower_dock.addPanel(dock)
            case _:
                pass

    def setShowHide(self):
        dialog = IgnoreDialog(self.show_docks, self.hide_docks)
        dialog.exec()
        if dialog.success == True:
            self.show_docks = dialog.show_docks
            self.hide_docks = dialog.hide_docks
            for dock in self.docks:
                self.processDock(dock)
            self.loadDocks()


class DockMonitor(QObject):
    
    dockWidgetAdded = pyqtSignal(QDockWidget)
    dockWidgetMoved = pyqtSignal(QDockWidget, Qt.DockWidgetArea)
    
    def eventFilter(self, o, e):
        if e.type() == QEvent.ChildAdded:
            child = e.child()
            if isinstance(o, QMainWindow) and isinstance(child, QDockWidget):
                self.dockWidgetAdded.emit(child)
                child.dockLocationChanged.connect(
                    lambda area, dw=child: self.on_location_changed(dw, area)
                )
                
        return super().eventFilter(o, e)

    def on_location_changed(self, widget, area):
        self.dockWidgetMoved.emit(widget, area)
    
