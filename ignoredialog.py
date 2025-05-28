from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QListWidget,
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
        self.docks = self.show_docks + self.hide_docks
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
        self.show_box = QListWidget()
        pos = 0
        for dock in self.show_docks:
            self.show_box.addItem(dock.windowTitle())
        self.show_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hide_box = QListWidget()
        for dock in self.hide_docks:
            self.hide_box.addItem(dock.windowTitle())
        self.hide_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_layout.addWidget(self.show_label)
        self.show_layout.addWidget(self.show_box)
        self.hide_layout.addWidget(self.hide_label)
        self.hide_layout.addWidget(self.hide_box)
        self.hide_button = QPushButton(QIcon(':/images/themes/default/mActionArrowRight.svg'), '')
        self.hide_button.clicked.connect(self.hideDock)
        self.show_button = QPushButton(QIcon(':/images/themes/default/mActionArrowLeft.svg'), '')
        self.show_button.clicked.connect(self.showDock)
        self.dock_buttons_layout.addWidget(self.show_button)
        self.dock_buttons_layout.addWidget(self.hide_button)

        self.docks_layout.addLayout(self.show_layout)
        self.docks_layout.addLayout(self.dock_buttons_layout)
        self.docks_layout.addLayout(self.hide_layout)
        self.layout.addLayout(self.docks_layout)

        self.ok_button = QPushButton(text='Ok')
        self.ok_button.clicked.connect(self.submitValues)
        self.cancel_button = QPushButton(text='Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.finished_buttons_layout.addWidget(self.ok_button)
        self.finished_buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.finished_buttons_layout)

    def showDock(self):
        selection = self.hide_box.currentItem()
        if selection:
            self.hide_box.takeItem(self.hide_box.row(selection))
            self.show_box.addItem(selection.text())
        else:
            pass

    def hideDock(self):
        selection = self.show_box.currentItem()
        if selection:
            self.show_box.takeItem(self.show_box.row(selection))
            self.hide_box.addItem(selection.text())
        else:
            pass

    def submitValues(self):
        self.hide = [self.hide_box.item(row).text() for row in range(self.hide_box.count())]
        self.show = [self.show_box.item(row).text() for row in range(self.show_box.count())]
        for dock in self.docks:
            if dock.windowTitle() in self.hide:
                self.hide_docks.append(dock)
            else:
                self.show_docks.append(dock)
        self.success = True
        self.close()
