import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt

class VuePlan(QWidget):
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

        self.sectors = {
    "Fruits et Legumes": {
        "color": QColor(144, 238, 144, 120),
        "cells": {(row, col) for row in range(13, 48) for col in range(31, 49)}
    },
    "Charcuterie": {
        "color": QColor(255, 182, 193, 120),
        "cells": {(row, col) for row in range(13, 48) for col in range(28, 30)},
        "cells2": {(row, col) for row in range(31, 48) for col in range(23, 24)}
    },
    "Poissonnerie": {
        "color": QColor(135, 206, 250, 120),
        "cells": {(row, col) for row in range(2, 12) for col in range(2, 13)}
    },
    "Fromage": {
        "color": QColor(255, 255, 153, 120),
        "cells": {(row, col) for row in range(2, 6) for col in range(19, 33)}
    },
    "Viandes / Boucherie": {
        "color": QColor(255, 99, 71, 120),
        "cells": {(row, col) for row in range(1, 8) for col in range(35, 115)}
    },
    "Surgeles": {
        "color": QColor(173, 216, 230, 120),
        "cells": {(row, col) for row in range(12, 49) for col in range(50, 63)}
    },
    "Epicerie": {
        "color": QColor(240, 230, 140, 120),
        "cells": {(row, col) for row in range(40, 55) for col in range(20, 35)}
    },
    "Boissons / Eaux": {
        "color": QColor(135, 206, 235, 120),
        "cells": {(row, col) for row in range(40, 50) for col in range(10, 20)}
    },
    "Cave a vins": {
        "color": QColor(199, 21, 133, 120),
        "cells": {(row, col) for row in range(40, 50) for col in range(5, 10)}
    },
    "Textile": {
        "color": QColor(216, 191, 216, 120),
        "cells": {(row, col) for row in range(25, 35) for col in range(40, 55)}
    },
    "Bazar": {
        "color": QColor(255, 215, 0, 120),
        "cells": {(row, col) for row in range(20, 55) for col in range(60, 75)}
    },
    "Entretien / Produits menagers": {
        "color": QColor(224, 255, 255, 120),
        "cells": {(row, col) for row in range(15, 20) for col in range(65, 75)}
    },
    "Saisonnier": {
        "color": QColor(176, 224, 230, 120),
        "cells": {(row, col) for row in range(35, 45) for col in range(55, 70)}
    },
    "Parfumerie / Beauté": {
        "color": QColor(255, 192, 203, 120),
        "cells": {(row, col) for row in range(25, 30) for col in range(50, 60)}
    },
    "Pain / Patisserie": {
        "color": QColor(255, 228, 181, 120),
        "cells": {(row, col) for row in range(15, 20) for col in range(40, 50)}
    },
    "Jus de fruits": {
        "color": QColor(255, 160, 122, 120),
        "cells": {(row, col) for row in range(55, 60) for col in range(5, 15)}
    },
    "Boutique / Telephonie": {
        "color": QColor(100, 149, 237, 120),
        "cells": {(row, col) for row in range(60, 65) for col in range(75, 80)}
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VuePlan("plan.jpg", scale_percent=95, cell_size=8)
    window.show()
    sys.exit(app.exec())
