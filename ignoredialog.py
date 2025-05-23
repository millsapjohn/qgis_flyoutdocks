from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface

class IgnoreDialog(QDialog):
    def __init__(self, show_docks, hide_docks):
        super().__init__()
        self.iface = iface
        self.show_docks = show_docks
        self.hide_docks = hide_docks
        self.success = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manage Panel Visibility')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.docks_layout = QHBoxLayout()
        self.show_layout = QVBoxLayout()
        self.hide_layout = QVBoxLayout()
        self.dock_buttons_layout = QVBoxLayout()
        self.finished_buttons_layout = QHBoxLayout()

        self.show_label = QLabel('Visible Dock Panels')
        self.hide_label = QLabel('Hidden Dock Panels')
        self.show_box = QTableWidget()
        pos = 0
        for dock in self.show_docks:
            self.show_box.insertRow(pos)
            self.show_box.setItem(pos, 0, dock)
            self.show_box.setItem(pos, 1, dock.windowTitle())
            pos += 1
        self.show_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_box.setColumnHidden(0, True)
        self.hide_box = QTableWidget()
        pos = 0
        for dock in self.hide_docks:
            self.hide_box.insertRow(pos)
            self.hide_box.setItem(pos, 0, dock)
            self.hide_box.setItem(pos, 1, dock.windowTitle())
            pos += 1
        self.hide_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hide_box.setColumnHidden(0, True)
        self.show_layout.addWidget(self.show_label)
        self.show_layout.addWidget(self.show_box)
        self.hide_layout.addWidget(self.hide_label)
        self.hide_layout.addWidget(self.hide_box)
        self.hide_button = QPushbutton(QIcon(':/images/themes/default/mActionArrowRight.svg'), '')
        self.hide_button.clicked.connect(self.hideDock)
        self.show_button = QPushButton(QIcon(':/images/themes/default/mActionArrowLeft.svg'), '')
        self.show_button.clicked.connect(self.showDock)
        self.panel_buttons_layout.addWidget(self.show_button)
        self.panel_buttons_layout.addWidget(self.hide_button)

        self.docks_layout.addLayout(self.show_layout)
        self.docks_layout.addLayout(self.dock_buttons_layout)
        self.docks_layout.addLayout(self.hide_layout)
        self.layout.addLayout(self.panels_layout)

        self.ok_button = QPushButton(text='ok')
        self.ok_button.clicked.connect(self.submit_values)
        self.cancel_button = QPushButton(text='Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.finished_buttons_layout.addWidget(self.ok_button)
        self.finished_buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.finished_buttons_layout)

    def showDock(self):
        selection = self.hide_box.currentItem()
        if selection:
            row = self.hide_box.currentRow()
            (dock, name) = (self.hide_box.takeItem(row, 0), self.hide_box.takeItem(row, 1))
            self.hide_box.removeRow(row)
            show_rows = self.show_box.rowCount()
            self.show_box.insertRow(show_rows)
            self.show_box.setItem(show_rows, 0, dock)
            self.show_box.setItem(show_rows, 1, name)
        else:
            pass

    def hideDock(self):
        selection = self.show_box.currentItem()
        if selection:
            row = self.show_box.currentRow()
            (dock, name) = (self.show_box.takeItem(row, 0), self.show_box.takeItem(row, 1))
            self.hide_box.removeRow(row)
            hide_rows = self.hide_box.rowCount()
            self.hide_box.insertRow(hide_rows)
            self.hide_box.setItem(show_rows, 0, dock)
            self.hide_box.setItem(show_rows, 1, name)
        else:
            pass

    def submitValues(self):
        self.hide = []
        self.show = []
        for i in range(self.hide_box.rowCount()):
            self.hide_docks.append(self.hide_box.item(i, 0))
        for i in range(self.show_box.rowCount()):
            self.show_docks.append(self.show_box.item(i, 0))
        self.success = True
        self.close()
