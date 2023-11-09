from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtCore import Qt, QMimeData, QByteArray, QBuffer, QIODevice


class ClickableLabel(QLabel):

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

        self.setAcceptDrops(True)
        self.drag_start_position = None
        self.original_pixmap = None

    def mousePressEvent(self, event):
        print("MousePressEvent")
        if not (event.button() == Qt.LeftButton) and self.pixmap() is not None:
            return
        self.drag_start_position = event.pos()
        self.original_pixmap = self.pixmap().copy()

        drag = QDrag(self)
        mime_data = QMimeData()
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        self.original_pixmap.save(buffer, "PNG")

        mime_data.setData("image/png", byte_array)
        drag.setMimeData(mime_data)

        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.original_pixmap)

        drag.exec()

        self.setPixmap(QPixmap())

    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton and self.pixmap():
            drag = QDrag(self)
            mime_data = QMimeData()
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.original_pixmap.save(buffer, "PNG")
            mime_data.setData("image/png", byte_array)
            drag.setMimeData(mime_data)

            drag.setHotSpot(event.pos() - self.rect().topLeft())

            drag.exec()

    def dragEnterEvent(self, event):
        print("Drag event")
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()
        print("Drop event")
        if event.mimeData().hasFormat("image/png"):
            byte_array = event.mimeData().data("image/png")
            pixmap = QPixmap()
            pixmap.loadFromData(byte_array)
            self.setPixmap(pixmap)

        else:
            return
