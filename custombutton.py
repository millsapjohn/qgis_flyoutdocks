from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import (
    QToolButton,
    QWidget,
    QStyleOptionToolButton,
    QSizePolicy,
)
from qgis.PyQt.QtGui import (
    QPainter,
    QTransform,
    QIcon,
    QFontMetrics,
)
from qgis.PyQt.QtCore import (
    Qt,
    QSize,
    QRect,
)


class RotatedButton(QToolButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        text_copy = option.text
        icon_copy = option.icon
        option.text = ""
        option.icon = QIcon()

        self.style().drawControl(self.style().CE_ToolButton, option, painter, self)
        option.text = text_copy
        option.icon = icon_copy

        painter.save()

        center_x = self.width() / 2
        center_y = self.height() / 2

        painter.translate(center_x, center_y)
        painter.rotate(-90)

        fm = self.fontMetrics()
        text_w = fm.horizontalAdvance(self.text())
        text_h = fm.height()

        text_rect = QRect(-text_w / 2, -text_h / 2, text_w, text_h)

        painter.setPen(option.palette.buttonText().color())
        painter.setFont(option.font)

        painter.drawText(text_rect, Qt.AlignCenter, self.text())

        painter.restore()

    def sizeHint(self):
        fm = self.fontMetrics()
        text_w = fm.horizontalAdvance(self.text())
        text_h = fm.height()

        df_size = QToolButton().sizeHint()
        w_hint = max(df_size.height(), text_h + 4)
        h_hint = max(df_size.width(), text_w + 4)
        return QSize(w_hint, h_hint)

    def minimumSizeHint(self):
        return self.sizeHint()
