from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import (
    QToolButton,
    QWidget,
    QStyleOptionToolButton,
    QSizePolicy,
    QStyle,
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
        super().__init__(parent)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setToolTip(text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        option.rect = self.rect()
        self.style().drawPrimitive(QStyle.PE_PanelButtonTool, option, painter, self)
        text_copy = option.text
        icon_copy = option.icon
        option.text = ""
        option.icon = QIcon()
        self.style().drawControl(0, option, painter, self)
        option.text = text_copy
        option.icon = icon_copy
        painter.save()
        fm = self.fontMetrics()
        text_rect = fm.boundingRect(self.text())
        center_x = self.width() / 2
        center_y = self.height() / 2
        painter.translate(center_x, center_y)
        painter.rotate(-90)
        draw_rect = QRect(
            -text_rect.width() // 2,
            -text_rect.height() // 2,
            text_rect.width(),
            text_rect.height()
        )
        painter.setPen(option.palette.buttonText().color())
        painter.setFont(option.font)
        painter.drawText(draw_rect, Qt.AlignCenter, self.text())
        painter.restore()

    def sizeHint(self):
        fm = self.fontMetrics()
        text_w = fm.horizontalAdvance(self.text())
        text_h = fm.height()

        df_size = QToolButton().sizeHint()
        w_hint = max(df_size.height(), text_h + 12)
        h_hint = max(df_size.width(), text_w + 12)
        calculated_size = QSize(w_hint, h_hint)
        return calculated_size

    def minimumSizeHint(self):
        return self.sizeHint()
