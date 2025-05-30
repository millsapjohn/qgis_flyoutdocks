from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtWidgets import QToolBar, QDockWidget, QMainWindow, QAction
from qgis.PyQt.QtCore import Qt, QObject, QEvent, pyqtSignal, QTimer
from qgis.PyQt.QtGui import QIcon
from .custombar import CustomBar
from .ignoredialog import IgnoreDialog
import pickle
from os import path

plugin_icon = QIcon(':/images/themes/default/console/iconHideToolConsole.svg')

# TODO: set a variable to prevent reloading panels at startup


class FlyoutDocksPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.settings = QgsSettings()
        self.instance = QgsApplication.instance()
        profilepath = path.dirname(self.instance.qgisUserDatabaseFilePath())
        pluginpath = path.join(profilepath, 'python/plugins/FlyoutDocks')
        self.hide_path = path.join(pluginpath, 'hide.pkl')
        if path.exists(self.hide_path):
            with open(self.hide_path, 'rb') as f:
                self.hide_docks_names = pickle.load(f)
        else:
            self.hide_docks_names = []
        self.show_docks_names = []
        self.dock_bars = []
        self.hide_docks = []
        self.show_docks = []
        self.left_docks = []
        self.right_docks = []
        self.upper_docks = []
        self.lower_docks = []
        self.docks = []
        self.left_bar = None
        self.right_bar = None
        self.upper_bar = None
        self.lower_bar = None
        self.mw = self.iface.mainWindow()
        QTimer.singleShot(20000, self.initGui)

    def initGui(self):
        current_opt = self.mw.dockOptions()
        new_opt = current_opt & ~QMainWindow.AllowNestedDocks
        new_opt = new_opt & ~QMainWindow.AllowTabbedDocks
        self.mw.setDockOptions(new_opt)
        self.showHideAction = QAction(plugin_icon, 'Show/Hide Dock Widgets')
        self.iface.addPluginToMenu('Manage Dock Widgets', self.showHideAction)
        self.showHideAction.triggered.connect(self.setShowHide)
        self.dock_monitor = DockMonitor(self.mw)
        self.mw.installEventFilter(self.dock_monitor)
        self.dock_monitor.dockWidgetAdded.connect(self.processNewDock)
        self.dock_monitor.dockWidgetMoved.connect(self.processMoveDock)
        self.initialLoadDocks()

    def initialLoadDocks(self):
        self.docks = self.mw.findChildren(QDockWidget)
        for dock in self.docks:
            if dock.windowTitle() in self.hide_docks_names:
                continue
            else:
                if dock.windowTitle() not in self.show_docks_names:
                    self.show_docks_names.append(dock.windowTitle())
        self.hide_docks.clear()
        self.show_docks.clear()
        for dock in list(self.docks):
            try:
                dock.dockLocationChanged.disconnect()
            except TypeError:
                pass
            dock.dockLocationChanged.connect(
                lambda area, dw=dock: self.dock_monitor.on_location_changed(dw, area)
            )
            current_area = self.mw.dockWidgetArea(dock)
            if current_area != Qt.NoDockWidgetArea:
                self.mw.removeDockWidget(dock)
                self.mw.addDockWidget(current_area, dock)
            if dock.windowTitle() in self.hide_docks_names:
                if dock not in self.hide_docks:
                    self.hide_docks.append(dock)
            elif dock.windowTitle() in self.show_docks_names:
                if dock not in self.show_docks:
                    self.show_docks.append(dock)
        self.left_docks.clear()
        self.right_docks.clear()
        self.upper_docks.clear()
        self.lower_docks.clear()
        for dock in self.docks:
            self.processDockPlacement(dock)
        self.loadDocks()

    def unload(self):
        self.iface.removePluginMenu('Manage Dock Widgets', self.showHideAction)
        for dock in self.docks:
            try:
                dock.dockLocationChanged.disconnect()
            except TypeError:
                pass
        for bar in list(self.mw.findChildren(QToolBar)):
            if isinstance(bar, CustomBar):
                self.mw.removeToolBar(bar)
                bar.deleteLater()
        self.showHideAction.deleteLater()
        if self.mw and self.dock_monitor:
            self.mw.removeEventFilter(self.dock_monitor)

    def processDockPlacement(self, dock):
        if dock in self.hide_docks:
            return
        current_area = self.mw.dockWidgetArea(dock)
        match current_area:
            case Qt.LeftDockWidgetArea:
                if dock not in self.left_docks:
                    self.left_docks.append(dock)
            case Qt.RightDockWidgetArea:
                if dock not in self.right_docks:
                    self.right_docks.append(dock)
            case Qt.TopDockWidgetArea:
                if dock not in self.upper_docks:
                    self.upper_docks.append(dock)
            case Qt.BottomDockWidgetArea:
                if dock not in self.lower_docks:
                    self.lower_docks.append(dock)
            case _:
                pass

    def loadDocks(self):
        for bar in list(self.mw.findChildren(QToolBar)):
            if isinstance(bar, CustomBar):
                self.mw.removeToolBar(bar)
                bar.deleteLater()
        self.dock_bars.clear()
        self.left_bar = None
        self.right_bar = None
        self.upper_bar = None
        self.lower_bar = None
        if self.left_docks:
            self.left_bar = CustomBar(self.iface, self.left_docks, 'Left Bar', self.mw)
            self.mw.addToolBar(Qt.LeftToolBarArea, self.left_bar)
            self.dock_bars.append(self.left_bar)
            self.left_bar.show()
        if self.right_docks:
            self.right_bar = CustomBar(self.iface, self.right_docks, 'Right Bar', self.mw)
            self.mw.addToolBar(Qt.RightToolBarArea, self.right_bar)
            self.dock_bars.append(self.right_bar)
            self.right_bar.show()
        if self.upper_docks:
            self.upper_bar = CustomBar(self.iface, self.upper_docks, 'Upper Bar', self.mw)
            self.mw.addToolBar(Qt.TopToolBarArea, self.upper_bar)
            self.dock_bars.append(self.upper_bar)
            self.upper_bar.show()
        if self.lower_docks:
            self.lower_bar = CustomBar(self.iface, self.lower_docks, 'Lower Bar', self.mw)
            self.mw.addToolBar(Qt.BottomToolBarArea, self.lower_bar)
            self.dock_bars.append(self.lower_bar)
            self.lower_bar.show()

    def processNewDock(self, dock):
        if dock not in self.docks:
            self.docks.append(dock)
        if dock.windowTitle() not in self.hide_docks_names and dock not in self.show_docks:
            self.show_docks.append(dock)
            self.show_docks_names.append(dock.windowTitle())
        try:
            dock.dockLocationChanged.disconnect()
        except TypeError:
            pass
        dock.dockLocationChanged.connect(
            lambda area, dw=dock: self.dock_monitor.on_location_changed(dw, area)
        )
        if dock.windowTitle() in self.hide_docks_names:
            if dock not in self.hide_docks:
                self.hide_docks.append(dock)
        elif dock.windowTitle() in self.show_docks_names:
            if dock not in self.show_docks:
                dock.hide()
        else:
            if dock not in self.show_docks:
                self.show_docks.append(dock)
        self._updateDockPlacement(dock)
        with open(self.hide_path, 'wb') as f:
            pickle.dump([d.windowTitle() for d in self.hide_docks], f)

    def processMoveDock(self, dock):
        self._updateDockPlacement(dock)

    def _updateDockPlacement(self, dock):
        old_area = None
        if dock in self.left_docks:
            self.left_docks.remove(dock)
            old_area = Qt.LeftDockWidgetArea
            if self.left_bar:
                self.left_bar.removePanel(dock)
        elif dock in self.right_docks:
            self.right_docks.remove(dock)
            old_area = Qt.RightDockWidgetArea
            if self.right_bar:
                self.right_bar.removePanel(dock)
        elif dock in self.upper_docks:
            self.upper_docks.remove(dock)
            old_area = Qt.TopDockWidgetArea
            if self.upper_bar:
                self.upper_bar.removePanel(dock)
        elif dock in self.lower_docks:
            self.lower_docks.remove(dock)
            old_area = Qt.BottomDockWidgetArea
            if self.lower_bar:
                self.lower_bar.removePanel(dock)

        curr_area = self.mw.dockWidgetArea(dock)
        
        if dock in self.hide_docks:
            return

        if curr_area == Qt.LeftDockWidgetArea:
            if dock not in self.left_docks:
                self.left_docks.append(dock)
            if self.left_bar:
                self.left_bar.addPanel(dock)
        elif curr_area == Qt.RightDockWidgetArea:
            if dock not in self.right_docks:
                self.right_docks.append(dock)
            if self.right_bar:
                self.right_bar.addPanel(dock)
        elif curr_area == Qt.TopDockWidgetArea:
            if dock not in self.upper_docks:
                self.upper_docks.append(dock)
            if self.upper_bar:
                self.upper_bar.addPanel(dock)
        elif curr_area == Qt.BottomDockWidgetArea:
            if dock not in self.lower_docks:
                self.lower_docks.append(dock)
            if self.lower_bar:
                self.lower_bar.addPanel(dock)

    def setShowHide(self):
        dialog = IgnoreDialog(self.show_docks_names, self.hide_docks_names)
        dialog.exec()
        if dialog.success is True:
            self.show_docks_names = dialog.show_docks_names
            self.hide_docks_names = dialog.hide_docks_names
            with open(self.hide_path, 'wb') as f:
                pickle.dump(self.hide_docks_names, f)
            self.show_docks.clear()
            self.hide_docks.clear()
            for dock in self.docks:
                if dock.windowTitle() in self.show_docks_names:
                    self.show_docks.append(dock)
                else:
                    self.hide_docks.append(dock)
            self.left_docks.clear()
            self.right_docks.clear()
            self.upper_docks.clear()
            self.lower_docks.clear()
            for dock in self.docks:
                self.processDockPlacement(dock)
            self.loadDocks()


class DockMonitor(QObject):

    dockWidgetAdded = pyqtSignal(QDockWidget)
    dockWidgetMoved = pyqtSignal(QDockWidget, Qt.DockWidgetArea)

    def eventFilter(self, o, e):
        if e.type() == QEvent.ChildAdded:
            child = e.child()
            if isinstance(o, QMainWindow) and isinstance(child, QDockWidget):
                self.dockWidgetAdded.emit(child)
                
        return super().eventFilter(o, e)

    def on_location_changed(self, widget, area):
        self.dockWidgetMoved.emit(widget, area)
