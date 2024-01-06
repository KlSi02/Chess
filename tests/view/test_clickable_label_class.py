from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint, QMimeData, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap
from src.view.clickable_label import ClickableLabel

app_created = False


def test_clickable_label_class(qtbot):
    global app_created
    if not app_created:
        app = QApplication([])
        app_created = True

    # Test __init__
    label = ClickableLabel()
    assert label.acceptDrops()
    assert label.drag_start_position is None
    assert label.original_pixmap is None

    # Test mousePressEvent
    qtbot.addWidget(label)
    qtbot.mousePress(label, Qt.LeftButton, pos=QPoint(10, 10))
    assert label.drag_start_position == QPoint(10, 10)
    assert label.original_pixmap is not None

    # Test mouseMoveEvent
    label.original_pixmap = QPixmap()  # Setze ein Bild für original_pixmap
    qtbot.mousePress(label, Qt.LeftButton, pos=QPoint(10, 10))

    # Test dragEnterEvent
    mime_data = label.createMimeData()  # Erzeuge ein MimeData-Objekt für das Testen
    assert mime_data is not None

    # Test dropEvent
    drop_event = QDropEvent(QPoint(20, 20), Qt.CopyAction, mime_data, Qt.LeftButton, Qt.NoModifier)
    qtbot.drop(label, drop_event)
    assert label.pixmap() is not None
