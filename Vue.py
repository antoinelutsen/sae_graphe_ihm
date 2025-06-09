import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt

class VuePlan(QWidget):
    def __init__(self, image_path: str, scale_percent: int = 100, cell_size: int = 8):
        super().__init__()

        self.setWindowTitle("Plan quadrillé redimensionné")
        self.image_path = image_path
        self.scale_percent = scale_percent
        self.cell_size = cell_size

        self.pixmap_original = QPixmap(self.image_path)

        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        new_width = int(screen_width * (self.scale_percent / 100))
        new_height = int(screen_height * (self.scale_percent / 100))

        self.pixmap_scaled = self.pixmap_original.scaled(
            new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
        )

        self.setFixedSize(self.pixmap_scaled.size())

        # Define inaccessible cells as set of (row, col) en gros ligne puis colonne
        # Exemple : [(0,0), (1,3), (5,10), ...]
        self.inaccessible_cells = {
            (5, 10), (7, 12)  # à adapter toi-même
        }

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap_scaled)

        pen = QPen(QColor(0, 255, 0, 180))
        pen.setWidth(1)
        painter.setPen(pen)

        width = self.pixmap_scaled.width()
        height = self.pixmap_scaled.height()

        # Draw grid
        for x in range(0, width, self.cell_size):
            painter.drawLine(x, 0, x, height)

        for y in range(0, height, self.cell_size):
            painter.drawLine(0, y, width, y)

        # Draw inaccessible cells in opaque black
        brush_color = QColor(0, 0, 0, 255)
        painter.setBrush(brush_color)
        painter.setPen(Qt.PenStyle.NoPen)

        for (row, col) in self.inaccessible_cells:
            rect_x = col * self.cell_size
            rect_y = row * self.cell_size
            painter.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        col = pos.x() // self.cell_size
        row = pos.y() // self.cell_size
        if (row, col) in self.inaccessible_cells:
            # Click ignored on inaccessible cell
            return
        print(f"Clicked at x={pos.x()}, y={pos.y()}")
        print(f"Grid cell clicked: row={row}, col={col}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VuePlan("plan.jpg", scale_percent=95, cell_size=8)
    window.show()
    sys.exit(app.exec())
