from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QMessageBox, QVBoxLayout, QDialog, QPushButton, QLabel, \
    QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor
from src.view.clickable_label import ClickableLabel


class UIChessboard(QtWidgets.QMainWindow):
    labels = []

    def __init__(self, callback):
        super().__init__()

        self.callback = callback

        self.border_size = None
        self.setWindowTitle("Chess")

        icon = QIcon("assets/chess_icon.png")
        self.setWindowIcon(icon)

        self.setGeometry(100, 100, 850, 800)
        self.setMinimumSize(800, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(0)

        self.create_ui()

    def create_ui(self):
        rows = 8
        cols = 8
        spalten_buchstaben = ["A", "B", "C", "D", "E", "F", "G", "H"]
        zeilen_zahlen = ["8", "7", "6", "5", "4", "3", "2", "1"]  # Reversed for correct order

        # Set the border size
        self.border_size = 20

        small_border_size = 10
        self.grid_layout.setContentsMargins(small_border_size, small_border_size, small_border_size, small_border_size)

        font = QFont()
        font.setPointSize(14)
        font.setWeight(QFont.Weight.Bold)

        for i, letter in enumerate(spalten_buchstaben):
            top_letter_label = QLabel(letter)
            bottom_letter_label = QLabel(letter)

            for label in (top_letter_label, bottom_letter_label):
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(font)
                label.setMargin(0)
                self.grid_layout.addWidget(label, 0 if label == top_letter_label else rows + 1, i + 1, 1, 1)
                label.setStyleSheet("background-color: transparent;")

        for i, number in enumerate(zeilen_zahlen):
            left_number_label = QLabel(number)
            right_number_label = QLabel(number)

            for label in (left_number_label, right_number_label):
                label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                label.setFont(font)
                label.setStyleSheet("background-color: transparent;")

            self.grid_layout.addWidget(left_number_label, i + 1, 0)
            self.grid_layout.addWidget(right_number_label, i + 1, cols + 1)

        self.grid_layout.setContentsMargins(self.border_size, self.border_size, self.border_size, self.border_size)

        # Create the chessboard squares
        for row in range(rows):
            for col in range(cols):
                label = ClickableLabel(self.callback)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                if (row + col) % 2 == 0:
                    soft_white = QColor(255, 255, 255)
                    label.set_highlight_color(soft_white)
                else:
                    grey_color = QColor(155, 155, 155)
                    label.set_highlight_color(grey_color)
                label_name = spalten_buchstaben[col] + zeilen_zahlen[row]
                label.setObjectName(label_name)
                self.grid_layout.addWidget(label, row + 1, col + 1)
                self.labels.append(label)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        marble_pixmap = QPixmap("assets/marble_wallpaper.jpg")
        if marble_pixmap.isNull():
            print("Fehler beim Laden des Marmorhintergrunds.")
        else:
            painter.drawPixmap(self.rect(), marble_pixmap)

        painter.end()

    def reset_ui_chessboard(self):
        for label in self.labels:
            self.grid_layout.removeWidget(label)
            label.deleteLater()

        self.labels.clear()

        self.create_ui()
        self.adjustSize()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        grid_size = min(self.central_widget.width() - self.border_size * 2,
                        self.central_widget.height() - self.border_size * 2)

        label_size = grid_size // 8

        for label in self.labels:
            label.setFixedSize(label_size, label_size)

            if label.pixmap():
                scaled_pixmap = label.pixmap().scaled(QSize(label_size, label_size),
                                                      Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(scaled_pixmap)

        extra_width = self.central_widget.width() - grid_size - 2 * self.border_size

        self.grid_layout.setContentsMargins(extra_width // 2, self.border_size, extra_width // 2, self.border_size)

    def show_checkmate_dialog(self, winning_player, on_new_game, on_close_game):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Schachmatt")
        msg_box.setText(f"{winning_player} hat gewonnen!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Close)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Retry:
            on_new_game()
        else:
            on_close_game()

    def show_promotion_dialog(self, callback, callback1, callback2, pos, team):
        """
        #Zeigt ein Dialogfenster für die Bauernumwandlung an.
        """
        self.promotion_dialog = PromotionDialog(self, callback, callback1, callback2, pos, team)
        self.promotion_dialog.show()

    def show_stalemate_dialog(self, winning_player, on_new_game, on_close_game):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Stalemate!")
        msg_box.setText(f"{winning_player} hat gewonnen!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Close)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Retry:
            on_new_game()
        else:
            on_close_game()


class PromotionDialog(QDialog):

    def __init__(self, parent, callback, callback1, callback2, pos, team):
        super().__init__(parent)
        self.setWindowTitle("Pawn Promotion")
        self.layout = QVBoxLayout(self)
        self.setup_new_piece = callback
        self.update_piece = callback1
        self.update_state_of_game = callback2
        self.team = team
        self.pos = pos
        self.init_ui()

    def init_ui(self):
        team_lowercase = str(self.team.name.lower())
        piece_images = {
            "Queen": f"assets/{team_lowercase}_queen.svg",
            "Rook": f"assets/{team_lowercase}_rook.svg",
            "Bishop": f"assets/{team_lowercase}_bishop.svg",
            "Knight": f"assets/{team_lowercase}_knight.svg"
        }

        message_label = QLabel("Choose one of the pieces: ", self)
        self.layout.addWidget(message_label)

        for piece, image_path in piece_images.items():
            button = QPushButton(self)
            button.setObjectName(piece)
            iconSize = QSize(150, 150)
            button.setIcon(QIcon(QPixmap(image_path)))
            button.setIconSize(iconSize)
            button.clicked.connect(self.on_piece_selected)
            self.layout.addWidget(button)

    def on_piece_selected(self):
        button = self.sender()
        piece_type = button.objectName()

        new_piece = self.setup_new_piece(piece_type, self.team)
        if self.update_piece(new_piece, self.pos):
            self.update_state_of_game()
        self.close()
