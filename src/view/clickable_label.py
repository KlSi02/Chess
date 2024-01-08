import tempfile

from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, pyqtProperty, QPropertyAnimation


class ClickableLabel(QLabel):
    highlight_labels_signal = pyqtSignal(str)
    make_move_signal = pyqtSignal(str, str)
    castling_signal = pyqtSignal(str, str)
    en_passant_signal = pyqtSignal(str, str)
    current_drag_label = None
    original_pixmap = None

    def __init__(self, callback, parent=None):
        super(ClickableLabel, self).__init__(parent)

        self.animation = None
        self.callback = callback

        self.setAcceptDrops(True)
        self._color = QColor(0, 0, 0, 0)
        self.is_pulsing = False
        self.pulsing_color = None
        self.drag_start_position = None
        self.svg_renderer = None
        self.svg_path = ""
        self.update_stylesheet()

    def set_svg(self, svg_path):
        if svg_path:
            self.svg_path = svg_path
            self.svg_renderer = QSvgRenderer(svg_path)
            self.update_pixmap()
        else:
            self.svg_path = ""
            self.svg_renderer = None
            self.setPixmap(QPixmap())

    def update_pixmap(self):
        if self.svg_renderer:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap)
            self.svg_renderer.render(painter)
            painter.end()

            self.setPixmap(pixmap)

    def resizeEvent(self, event):
        super(ClickableLabel, self).resizeEvent(event)
        self.update_pixmap()
        self.update_stylesheet()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.svg_path is not None:
            if self.callback(self.objectName()):
                self.highlight_labels_signal.emit(self.objectName())
                self.drag_start_position = event.position().toPoint()
                ClickableLabel.original_svg_path = self.svg_path
                ClickableLabel.current_drag_label = self
            else:
                return

    def mouseMoveEvent(self, event):
        if not self.drag_start_position:
            return

        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()

        try:
            with open(self.svg_path, "r") as file:
                svg_data = file.read().encode()
            mime_data.setData("image/svg+xml", svg_data)
        except Exception as e:
            print(f"Fehler beim laden der SVG-Datei: {e}")

        drag.setMimeData(mime_data)

        # Erstellen Sie ein Pixmap von SVG
        svg_renderer = QSvgRenderer(self.svg_path)
        preview_pixmap = QPixmap(50, 50)  # Größe der Vorschau
        preview_pixmap.fill(Qt.GlobalColor.transparent)  # Transparenter Hintergrund
        painter = QPainter(preview_pixmap)
        svg_renderer.render(painter)
        painter.end()

        drag.setPixmap(preview_pixmap)
        drag.setHotSpot(event.position().toPoint() - self.rect().topLeft())

        if drag.exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
            self.clear()
        ClickableLabel.current_drag_label = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("image/svg+xml"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("image/svg+xml"):
            event.acceptProposedAction()

            if self.is_pulsing and self.pulsing_color == "green":
                self.make_move_signal.emit(ClickableLabel.current_drag_label.objectName(), self.objectName())
                ClickableLabel.current_drag_label.set_svg("")

                svg_data = event.mimeData().data("image/svg+xml")
                # Speichern der SVG-Daten in einer temporären Datei
                # Sie könnten auch einen anderen Weg finden, um einen Pfad zu den SVG-Daten zu erhalten
                with tempfile.NamedTemporaryFile(delete=False, suffix=".svg", mode="wb") as temp_file:
                    temp_file.write(svg_data)
                    temp_file_path = temp_file.name
                self.set_svg(temp_file_path)

            elif self.is_pulsing and self.pulsing_color == "yellow":
                self.castling_signal.emit(ClickableLabel.current_drag_label.objectName(), self.objectName())
                ClickableLabel.current_drag_label.set_svg("")

                svg_data = event.mimeData().data("image/svg+xml")
                # Speichern der SVG-Daten in einer temporären Datei
                # Sie könnten auch einen anderen Weg finden, um einen Pfad zu den SVG-Daten zu erhalten
                with tempfile.NamedTemporaryFile(delete=False, suffix=".svg", mode="wb") as temp_file:
                    temp_file.write(svg_data)
                    temp_file_path = temp_file.name
                self.set_svg(temp_file_path)

            elif self.is_pulsing and self.pulsing_color == "blue":
                self.en_passant_signal.emit(ClickableLabel.current_drag_label.objectName(), self.objectName())
                ClickableLabel.current_drag_label.set_svg("")

                svg_data = event.mimeData().data("image/svg+xml")
                # Speichern der SVG-Daten in einer temporären Datei
                # Sie könnten auch einen anderen Weg finden, um einen Pfad zu den SVG-Daten zu erhalten
                with tempfile.NamedTemporaryFile(delete=False, suffix=".svg", mode="wb") as temp_file:
                    temp_file.write(svg_data)
                    temp_file_path = temp_file.name
                self.set_svg(temp_file_path)

            else:
                event.ignore()
                if ClickableLabel.current_drag_label:
                    ClickableLabel.current_drag_label.set_svg(ClickableLabel.current_drag_label.svg_path)
                    ClickableLabel.current_drag_label = None

    def set_highlight_color(self, color, alpha=255):
        color.setAlpha(alpha)
        self._color = color
        if self.is_pulsing:
            self.stop_pulsing()
        self.update_stylesheet()

    def set_highlight_color_with_alpha(self, color, alpha):
        self._color = QColor(color.red(), color.green(), color.blue(), alpha)
        self.update_stylesheet()

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update_stylesheet()

    def update_stylesheet(self):
        if self.is_pulsing:
            border_style = "border: 1px solid black;"
        else:
            border_style = ""

        self.setStyleSheet(
            f"background-color: rgba({self._color.red()}, {self._color.green()}, {self._color.blue()}, {self._color.alpha()}); {border_style}")

    def start_pulsing(self, start_color, end_color, duration=1500):
        if not self.is_pulsing:
            self.is_pulsing = True
            # Setzen Sie die Farben für die Animation
            self.animation = QPropertyAnimation(self, b"color")
            self.animation.setDuration(duration)
            self.animation.setStartValue(start_color)
            self.animation.setEndValue(end_color)
            self.animation.setLoopCount(-1)
            self.animation.start()
            self.is_pulsing = True

    def stop_pulsing(self):
        if self.animation is not None and self.is_pulsing:
            self.animation.stop()
            self.is_pulsing = False
