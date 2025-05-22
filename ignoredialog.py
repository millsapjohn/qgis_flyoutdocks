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
    def __init__(self, show_panels, hide_panels):
        super().__init__()
        self.iface = iface
        self.show_panels = show_panels
        self.hide_panels = hide_panels
        self.success = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manage Panel Visibility')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.panels_layout = QHBoxLayout()
        self.show_layout = QVBoxLayout()
        self.hide_layout = QVBoxLayout()
        self.panel_buttons_layout = QVBoxLayout()
        self.finished_buttons_layout = QHBoxLayout()

        self.show_label = QLabel('Visible Dock Panels')
        self.hide_label = QLabel('Hidden Dock Panels')
        self.show_box = QTableWidget()
        pos = 0
        for panel in self.show_panels:
            self.show_box.insertRow(pos)
            self.show_box.setItem(pos, 0, panel)
            self.show_box.setItem(pos, 1, panel.windowTitle())
            pos += 1
        self.show_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_box.setColumnHidden(0, True)
        self.hide_box = QTableWidget()
        pos = 0
        for panel in self.hide_panels:
            self.hide_box.insertRow(pos)
            self.hide_box.setItem(pos, 0, panel)
            self.hide_box.setItem(pos, 1, panel.windowTitle())
            pos += 1
        self.hide_box.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hide_box.setColumnHidden(0, True)
        self.show_layout.addWidget(self.show_label)
        self.show_layout.addWidget(self.show_box)
        self.hide_layout.addWidget(self.hide_label)
        self.hide_layout.addWidget(self.hide_box)
        self.hide_button = QPushbutton(QIcon(':/images/themes/default/mActionArrowRight.svg'), '')
        self.hide_button.clicked.connect(self.hidePanel)
        self.show_button = QPushButton(QIcon(':/images/themes/default/mActionArrowLeft.svg'), '')
        self.show_button.clicked.connect(self.showPanel)
        self.panel_buttons_layout.addWidget(self.show_button)
        self.panel_buttons_layout.addWidget(self.hide_button)

        self.panels_layout.addLayout(self.show_layout)
        self.panels_layout.addLayout(self.panel_buttons_layout)
        self.panels_layout.addLayout(self.hide_layout)
        self.layout.addLayout(self.panels_layout)

        self.ok_button = QPushButton(text='ok')
        self.ok_button.clicked.connect(self.submit_values)
        self.cancel_button = QPushButton(text='Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.finished_buttons_layout.addWidget(self.ok_button)
        self.finished_buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.finished_buttons_layout)

    def showPanel(self):
        selection = self.hide_box.currentItem()
        if selection:
            row = self.hide_box.currentRow()
            (panel, name) = (self.hide_box.takeItem(row, 0), self.hide_box.takeItem(row, 1))
            self.hide_box.removeRow(row)
            show_rows = self.show_box.rowCount()
            self.show_box.insertRow(show_rows)
            self.show_box.setItem(show_rows, 0, panel)
            self.show_box.setItem(show_rows, 1, name)
        else:
            pass

    def hidePanel(self):
        selection = self.show_box.currentItem()
        if selection:
            row = self.show_box.currentRow()
            (panel, name) = (self.show_box.takeItem(row, 0), self.show_box.takeItem(row, 1))
            self.hide_box.removeRow(row)
            hide_rows = self.hide_box.rowCount()
            self.hide_box.insertRow(hide_rows)
            self.hide_box.setItem(show_rows, 0, panel)
            self.hide_box.setItem(show_rows, 1, name)
        else:
            pass

    def submitValues(self):
        self.hide = []
        self.show = []
        for i in range(self.hide_box.rowCount()):
            self.hide.append(self.hide_box.item(i, 0))
        for i in range(self.show_box.rowCount()):
            self.show.append(self.show_box.item(i, 0))
        self.success = True
        self.close()
