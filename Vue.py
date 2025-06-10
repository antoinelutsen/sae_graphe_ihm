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
        "cells": {(row, col) for row in range(13, 49) for col in range(31, 50)}
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
        "cells": {(row, col) for row in range(2, 7) for col in range(19, 34)}
    },
    "Surgeles": {
        "color": QColor(173, 216, 230, 120),
        "cells": {(row, col) for row in range(12, 49) for col in range(50, 63)}
    },
    "Epicerie": {
        "color": QColor(240, 230, 140, 120),
        "cells": {(row, col) for row in range(55, 87) for col in range(28, 57)}
    },
    "Eaux": {
        "color": QColor(135, 206, 235, 120),
        "cells": {(row, col) for row in range(55, 87) for col in range(10, 13)}
    },
    "Cave a vins": {
        "color": QColor(199, 21, 133, 120),
        "cells": {(row, col) for row in range(55, 73) for col in range(13, 27)}
    },
    "Textile": {
        "color": QColor(216, 191, 216, 120),
        "cells": {(row, col) for row in range(55, 87) for col in range(57, 75)}
    },
    "Bazar": {
        "color": QColor(255, 215, 0, 120),
        "cells": {(row, col) for row in range(28, 49) for col in range(112, 134)}
    },
    "Entretien": {
        "color": QColor(224, 255, 255, 120),
        "cells": {(row, col) for row in range(14, 28) for col in range(112, 134)}
    },
    "Saisonnier": {
        "color": QColor(176, 224, 230, 120),
        "cells": {(row, col) for row in range(12, 49) for col in range(97, 101)}
    },
    "Parfumerie": {
        "color": QColor(255, 192, 203, 120),
        "cells": {(row, col) for row in range(12, 49) for col in range(85, 98)}
    },
    "Pain / Patisserie": {
        "color": QColor(255, 228, 181, 120),
        "cells": {(row, col) for row in range(12, 14) for col in range(112, 134)}
    },
    "Jus de fruits": {
        "color": QColor(255, 160, 122, 120),
        "cells": {(row, col) for row in range(94, 100) for col in range(6, 32)}
    },
    "Boutique Informatique Telephonie": {
        "color": QColor(100, 149, 237, 120),
        "cells": {(row, col) for row in range(97, 108) for col in range(123, 141)}
    },
    "Ultra Frais": {
        "color": QColor(173, 216, 230, 120),  # bleu clair
        "cells": {(row, col) for row in range(15, 49) for col in range(2, 13)}
    },
    "Bieres": {
        "color": QColor(144, 238, 144, 120),  # vert
        "cells": {(row, col) for row in range(55, 100) for col in range(3, 6)}
    },
    "Alcools": {
        "color": QColor(255, 0, 0, 120),  # rouge
        "cells": {(row, col) for row in range(73, 88) for col in range(13, 16)}
    },
    "Lait + oeufs": {
        "color": QColor(0, 191, 255, 120),  # bleu (deep sky blue)
        "cells": {(row, col) for row in range(23, 49) for col in range(20, 23)}
    },
    "Saucissons": {
        "color": QColor(70, 130, 180, 120),  # bleu (steel blue)
        "cells": {(row, col) for row in range(12, 23) for col in range(20, 23)}
    },
    "Saucisserie": {
        "color": QColor(139, 0, 0, 120),  # rouge foncé (dark red)
        "cells": {(row, col) for row in range(12, 31) for col in range(22, 25)}
    },
    "Volailles": {
        "color": QColor(255, 69, 0, 120),  # rouge (orange red)
        "cells": {(row, col) for row in range(1, 5) for col in range(35, 50)}
    },
    "Boucherie": {
        "color": QColor(220, 20, 60, 120),  # rouge (crimson)
        "cells": {(row, col) for row in range(1, 5) for col in range(54, 80)}
    },
    "Boucherie trad": {
        "color": QColor(178, 34, 34, 120),  # rouge (firebrick)
        "cells": {(row, col) for row in range(5, 8) for col in range(81, 97)}
    },
    "Rotisserie": {
        "color": QColor(255, 0, 0, 120),  # rouge (red)
        "cells": {(row, col) for row in range(5, 8) for col in range(97, 115)}
    },
    "Charcuterie": {
        "color": QColor(255, 165, 0, 120),  # orange
        "cells": {(row, col) for row in range(5, 8) for col in range(115, 134)}
    },
    "Lessives": {
        "color": QColor(148, 0, 211, 120),  # violet (dark violet)
        "cells": {(row, col) for row in range(12, 37) for col in range(139, 141)}
    },
    "Patisserie industrielle / Pain": {
        "color": QColor(255, 140, 0, 120),  # orange (dark orange)
        "cells": {(row, col) for row in range(12, 49) for col in range(66, 68)}
    },
    "Univers Animaux": {
        "color": QColor(255, 255, 0, 120),  # jaune
        "cells": {(row, col) for row in range(12, 49) for col in range(68, 77)}
    },
    "Univers Bebe": {
        "color": QColor(255, 182, 193, 120),  # rose (light pink)
        "cells": {(row, col) for row in range(12, 49) for col in range(76, 85)}
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
