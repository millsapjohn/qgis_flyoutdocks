from qgis.PyQt.QtWidgets import (
    QToolBar,
    QPushButton,
)
from qgis.PyQt.QtGui import (
    QPainter,
    QColor,
    QFont,
    QFontMetrics
)
from qgis.PyQt.QtCore import (
    Qt, 
    QRect,
    QSize,
)


class CustomBar(QToolBar):
    def __init__(self, iface, panels, title):
        super().__init__()
        self.setObjectName(title)
        self.setWindowTitle(title)
        self.iface = iface
        self.mw = iface.mainWindow()
        for panel in panels:
            self.addPanel(panel)

    def panelState(self, panel):
        if panel.isVisible():
            panel.setVisible(False)
        else:
            panel.setVisible(True)

    def addPanel(self, panel):
        if self.windowTitle() == 'Upper Bar' or self.windowTitle() == 'Lower Bar':
            button = QPushButton(panel.windowTitle())
        else:
            button = VerticalButton(panel.windowTitle())
        button.clicked.connect(lambda: self.panelState(panel))
        self.addWidget(button)

    def removePanel(self, panel):
        child = self.layout.findChild(QPushButton, panel.windowTitle())
        child.clicked.disconnect(self.panelState)
        self.removeWidget(child)


class VerticalButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._default_font = self.font()
        self._palette = self.palette()

    def sizeHint(self):
        metrics = QFontMetrics(self._default_font)
        text_width = metrics.horizontalAdvance(self.text())
        text_height = metrics.height()
        padding = 4
        thickness = 2
        width = text_height + (padding * 2) + (thickness * 2)
        height = text_width + (padding * 2) + (thickness * 2)

        return QSize(width, height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()

        painter.drawRoundedRect(rect, 5, 5)

        painter.save()

        painter.translate(width / 2, height / 2)
        painter.rotate(90)
        painter.translate(-height / 2, -width / 2)

        painter.setPen(Qt.GlobalColor.black)
        text_rect = QRect(0, 0, height, width)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.text())

        painter.restore()
