import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt,  pyqtSignal

class VuePlan(QWidget):
    celluleCliquee = pyqtSignal(int, int)

    def __init__(self, image_path: str, scale_percent: int = 100, cell_size: int = 8):
        super().__init__()

        self.setWindowTitle("Plan quadrillé avec secteurs par cases")
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

        self.inaccessible_cells = {
            (5, 10), (7, 12)
        }

        # Exemple de secteurs définis par des cases à refaire et compléter
        self.sectors = {
            "Fruits": {
                "color": QColor(255, 200, 200, 120),
                "cells": {(20, col) for col in range(40, 51)}.union({(row, col) for row in range(21, 26) for col in range(50, 56)})
            },
            "Charcuterie": {
                "color": QColor(200, 255, 200, 120),
                "cells": {(row, col) for row in range(10, 20) for col in range(10, 30)}
            },
            "Légumes": {
                "color": QColor(200, 200, 255, 120),
                "cells": {(row, col) for row in range(30, 40) for col in range(60, 70)}
            }
        }

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap_scaled)

        width = self.pixmap_scaled.width()
        height = self.pixmap_scaled.height()

        pen_grid = QPen(QColor(0, 255, 0, 180))
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)

        for x in range(0, width, self.cell_size):
            painter.drawLine(x, 0, x, height)

        for y in range(0, height, self.cell_size):
            painter.drawLine(0, y, width, y)

        brush_black = QColor(0, 0, 0, 255)
        painter.setBrush(brush_black)
        painter.setPen(Qt.PenStyle.NoPen)
        for (row, col) in self.inaccessible_cells:
            rect_x = col * self.cell_size
            rect_y = row * self.cell_size
            painter.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

        # Draw sectors cases with colors
        for sector in self.sectors.values():
            painter.setBrush(QBrush(sector["color"]))
            painter.setPen(Qt.PenStyle.NoPen)
            for (row, col) in sector["cells"]:
                rect_x = col * self.cell_size
                rect_y = row * self.cell_size
                painter.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        col = pos.x() // self.cell_size
        row = pos.y() // self.cell_size
        if (row, col) in self.inaccessible_cells:
            return
        print(f"Clicked at x={pos.x()}, y={pos.y()}")
        print(f"Grid cell clicked: row={row}, col={col}")
        self.celluleCliquee.emit(row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VuePlan("plan.jpg", scale_percent=95, cell_size=8)
    window.show()
    sys.exit(app.exec())
