import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, pyqtSignal


class VuePlan(QWidget):
    celluleCliquee = pyqtSignal(int, int)

    def __init__(self, image_path: str, scale_percent: int = 100, cell_size: int = 8):
        super().__init__()
        self.setWindowTitle("Plan avec interface détaillée")

        self.image_path = image_path
        self.scale_percent = scale_percent
        self.cell_size = cell_size

        self.pixmap_original = QPixmap(self.image_path)
        screen = QApplication.primaryScreen().availableGeometry()
        new_width = 1200
        new_height = 1000
        self.pixmap_scaled = self.pixmap_original.scaled(
            new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
        )

        main_layout = QHBoxLayout(self)

        self.plan_frame = QFrame()
        self.plan_frame.setMinimumSize(self.pixmap_scaled.size())
        main_layout.addWidget(self.plan_frame)

        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel)

        titre = QLabel("Description")
        titre.setStyleSheet("font-size: 16px; font-weight: bold;")
        texte = QLabel("Bienvenue sur le plan du magasin. Cliquez sur une zone pour voir les produits.")
        texte.setWordWrap(True)
        texte.setMaximumHeight(100)
        right_panel.addWidget(titre, stretch=0)
        right_panel.addWidget(texte, stretch=1)

        self.zone_liste = QVBoxLayout()
        scroll_content = QWidget()
        scroll_content.setLayout(self.zone_liste)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        right_panel.addWidget(scroll_area, stretch=4)

        self.bouton_ajout = QPushButton("+ Ajouter un produit")
        self.bouton_ajout.clicked.connect(self.ajouter_champ_produit)
        right_panel.addWidget(self.bouton_ajout, stretch=0)

        self.inaccessible_cells = {(5, 10), (7, 12)}
        self.sectors = {
            "Fruits": {
                "color": QColor(255, 200, 200, 120),
                "cells": {(20, col) for col in range(40, 51)}
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

        self.info_label = QLabel(self.plan_frame)
        self.info_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid gray;
            padding: 5px;
            font-size: 11px;
        """)
        self.info_label.setWordWrap(True)
        self.info_label.setVisible(False)

        self.show()

    def ajouter_champ_produit(self):
        champ = QTextEdit()
        champ.setFixedHeight(40)
        champ.textChanged.connect(lambda: self.limiter_texte(champ))
        self.zone_liste.addWidget(champ)

    def limiter_texte(self, champ):
        texte = champ.toPlainText()
        if len(texte) > 100:
            champ.setPlainText(texte[:100])
            cursor = champ.textCursor()
            cursor.setPosition(100)
            champ.setTextCursor(cursor)

    def afficher_info_zone(self, texte: str, x: int, y: int):
        self.info_label.setText(texte)
        self.info_label.adjustSize()
        label_width = self.info_label.width()
        label_height = self.info_label.height()
        x = min(x, self.plan_frame.width() - label_width)
        y = min(y, self.plan_frame.height() - label_height)
        self.info_label.move(x, y)
        self.info_label.setVisible(True)

    def cacher_info_zone(self):
        self.info_label.setVisible(False)

    def afficher_produits_secteur(self, secteur: str, produits: list[str], x: int, y: int):
        self.cacher_info_zone()
        texte = f"<b>Secteur : {secteur}</b><br>" + "<br>".join(produits) if produits else f"<b>Secteur : {secteur}</b><br>Aucun produit trouvé"
        self.info_label.setText(texte)
        self.info_label.adjustSize()
        label_width = self.info_label.width()
        label_height = self.info_label.height()
        x = min(x, self.plan_frame.width() - label_width)
        y = min(y, self.plan_frame.height() - label_height)
        self.info_label.move(x, y)
        self.info_label.setVisible(True)

    def vider_produits_secteur(self):
        self.cacher_info_zone()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap_scaled)

        width = self.pixmap_scaled.width()
        height = self.pixmap_scaled.height()

        pen_grid = QPen(QColor(0, 255, 0, 180))
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)
        for x in range(0, width, self.cell_size):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, self.cell_size):
            painter.drawLine(0, y, width, y)

        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        for (row, col) in self.inaccessible_cells:
            painter.drawRect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

        for sector in self.sectors.values():
            painter.setBrush(QBrush(sector["color"]))
            for (row, col) in sector["cells"]:
                painter.drawRect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        col = pos.x() // self.cell_size
        row = pos.y() // self.cell_size
        if (row, col) in self.inaccessible_cells:
            return
        self.celluleCliquee.emit(row, col)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VuePlan("plan.jpg", scale_percent=90, cell_size=8)
    window.show()
    sys.exit(app.exec())
