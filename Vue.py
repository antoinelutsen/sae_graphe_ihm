import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, pyqtSignal

class VueAccueil(QWidget):
    mode_selectionne = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection du mode")
        self.setMinimumSize(400, 200)
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel("Choisissez un mode :")
        self.btn_creation = QPushButton("Création")
        self.btn_utilisation = QPushButton("Utilisation")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_creation)
        layout.addWidget(self.btn_utilisation)
        self.setLayout(layout)

        self.btn_creation.clicked.connect(lambda: self.mode_selectionne.emit("creation"))
        self.btn_utilisation.clicked.connect(lambda: self.mode_selectionne.emit("utilisation"))



class VuePlanUtilisation(QWidget):
    celluleCliquee = pyqtSignal(int, int)

    def __init__(self, image_path: str, cell_size: int = 8):
        super().__init__()
        self.setWindowTitle("Mode Utilisation")

        self.image_path = image_path
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
        "Fruits et Legumes": {
            "color": QColor(144, 238, 144, 120),
            "cells": {(row, col) for row in range(11, 53) for col in range(32, 52)}
        },
        "Charcuterie LS": {
            "color": QColor(255, 182, 193, 120),
            "cells": {(row, col) for row in range(11, 53) for col in range(28, 32)},  
        },
        "Poissonnerie": {
            "color": QColor(135, 206, 250, 120),
            "cells": {(row, col) for row in range(1, 14) for col in range(0, 17)}
        },
        "Fromage Trad": {
            "color": QColor(255, 255, 153, 120),
            "cells": {(row, col) for row in range(1, 9) for col in range(18, 36)}
        },
        "Surgeles": {
            "color": QColor(173, 216, 230, 120),
            "cells": {(row, col) for row in range(11, 53) for col in range(52, 67)}
        },
        "Epicerie": {
            "color": QColor(240, 230, 140, 120),
            "cells": {(row, col) for row in range(54, 93) for col in range(29, 59)}
        },
        "Eaux": {
            "color": QColor(135, 206, 235, 120),
            "cells": {(row, col) for row in range(54, 93) for col in range(9, 13)}
        },
        "Cave a vins": {
            "color": QColor(199, 21, 133, 120),
            "cells": {(row, col) for row in range(54, 76) for col in range(13, 29)}
        },
        "Textile": {
            "color": QColor(216, 191, 216, 120),
            "cells": {(row, col) for row in range(54, 93) for col in range(59, 102)}
        },
        "Bazar": {
            "color": QColor(255, 215, 0, 120),
            "cells": {(row, col) for row in range(29, 51) for col in range(112, 142)}
        },
        "Entretien": {
            "color": QColor(224, 255, 255, 120),
            "cells": {(row, col) for row in range(15, 29) for col in range(112, 142)}
        },
        "Saisonnier": {
            "color": QColor(176, 224, 230, 120),
            "cells": {(row, col) for row in range(13, 51) for col in range(102, 110)}
        },
        "Parfumerie": {
            "color": QColor(255, 192, 203, 120),
            "cells": {(row, col) for row in range(11, 54) for col in range(88, 102)}
        },
        "Pain / Patisserie": {
            "color": QColor(255, 228, 181, 120),
            "cells": {(row, col) for row in range(11, 15) for col in range(115, 142)}
        },
        "Jus de fruits": {
            "color": QColor(255, 160, 122, 120),
            "cells": {(row, col) for row in range(94, 106) for col in range(6, 34)}
        },
        "Boutique Informatique Telephonie": {
            "color": QColor(100, 149, 237, 120),
            "cells": {(row, col) for row in range(101, 112) for col in range(128, 149)}
        },
        "Ultra Frais": {
            "color": QColor(173, 216, 230, 120),  # bleu clair
            "cells": {(row, col) for row in range(14, 54) for col in range(0, 13)}
        },
        "Bieres": {
            "color": QColor(144, 238, 144, 120),  # vert
            "cells": {(row, col) for row in range(55, 106) for col in range(0, 6)}
        },
        "Alcools": {
            "color": QColor(255, 0, 0, 120),  # rouge
            "cells": {(row, col) for row in range(76, 93) for col in range(13, 18)}
        },
        "Lait + oeufs": {
            "color": QColor(0, 191, 255, 120),  # bleu (deep sky blue)
            "cells": {(row, col) for row in range(24, 53) for col in range(18, 24)}
        },
        "Saucissons": {
            "color": QColor(70, 130, 180, 120),  # bleu (steel blue)
            "cells": {(row, col) for row in range(11, 24) for col in range(19, 24)}
        },
        "Saucisserie": {
            "color": QColor(139, 0, 0, 120),  # rouge foncé (dark red)
            "cells": {(row, col) for row in range(11, 32) for col in range(24, 27)}
        },
        "Volailles": {
            "color": QColor(255, 69, 0, 120),  # rouge (orange red)
            "cells": {(row, col) for row in range(1, 7) for col in range(36, 53)}
        },
        "Boucherie": {
            "color": QColor(220, 20, 60, 120),  # rouge (crimson)
            "cells": {(row, col) for row in range(1, 6) for col in range(54, 83)}
        },
        "Boucherie trad": {
            "color": QColor(178, 34, 34, 120),  # rouge (firebrick)
            "cells": {(row, col) for row in range(4, 10) for col in range(84, 101)}
        },
        "Rotisserie": {
            "color": QColor(255, 0, 0, 120),  # rouge (red)
            "cells": {(row, col) for row in range(4, 10) for col in range(101, 120)}
        },
        "Charcuterie": {
            "color": QColor(255, 165, 0, 120),  # orange
            "cells": {(row, col) for row in range(4, 10) for col in range(120, 141)}
        },
        "Lessives": {
            "color": QColor(148, 0, 211, 120),  # violet (dark violet)
            "cells": {(row, col) for row in range(11, 39) for col in range(142, 147)}
        },
        "Patisserie industrielle / Pain": {
            "color": QColor(255, 140, 0, 120),  # orange (dark orange)
            "cells": {(row, col) for row in range(11, 53) for col in range(67, 71)}
        },
        "Univers Animaux": {
            "color": QColor(255, 255, 0, 120),  # jaune
            "cells": {(row, col) for row in range(11, 53) for col in range(71, 80)}
        },
        "Univers Bebe": {
            "color": QColor(255, 182, 193, 120),  # rose (light pink)
            "cells": {(row, col) for row in range(11, 53) for col in range(80, 88)}
        },
        "Fromage": {
            "color": QColor(255, 182, 193, 120),  # rose (light pink)
            "cells": {(row, col) for row in range(14, 53) for col in range(13, 18)}
        },
        "Sortie": {
            "color": QColor(255, 182, 193, 120),  # rose (light pink)
            "cells": {(row, col) for row in range(105, 106) for col in range(36, 99)}
        }
    }
        
        extension_charcuterie = {(row, col) for row in range(32, 53) for col in range(24, 28)}  
        self.sectors["Charcuterie LS"]["cells"] = self.sectors["Charcuterie LS"]["cells"].union(extension_charcuterie)

        extension_bazar = {(row, col) for row in range(65, 101) for col in range(112, 149)}  
        self.sectors["Bazar"]["cells"] = self.sectors["Bazar"]["cells"].union(extension_bazar)

        extension_bazar2 = {(row, col) for row in range(39, 65) for col in range(142, 149)}  
        self.sectors["Bazar"]["cells"] = self.sectors["Bazar"]["cells"].union(extension_bazar2)

        extension_saisonnier = {(row, col) for row in range(54, 94) for col in range(102, 110)}  
        self.sectors["Saisonnier"]["cells"] = self.sectors["Saisonnier"]["cells"].union(extension_saisonnier)

        extension_saisonnier2 = {(row, col) for row in range(51, 65) for col in range(112, 142)}  
        self.sectors["Saisonnier"]["cells"] = self.sectors["Saisonnier"]["cells"].union(extension_saisonnier2)

        extension_epicerie = {(row, col) for row in range(76, 93) for col in range(22, 29)}  
        self.sectors["Epicerie"]["cells"] = self.sectors["Epicerie"]["cells"].union(extension_epicerie)

        extension_vin = {(row, col) for row in range(76, 93) for col in range(18, 22)}  
        self.sectors["Cave a vins"]["cells"] = self.sectors["Cave a vins"]["cells"].union(extension_vin)

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

    def get_secteurs_et_cases(self):
        return {
            "sectors": {nom: infos["cells"] for nom, infos in self.sectors.items()},
            "inaccessibles": self.inaccessible_cells
        }

class VuePlanCreation(QWidget):
    celluleCliquee = pyqtSignal(int, int)

    def __init__(self, image_path: str, cell_size: int = 8):
        super().__init__()
        self.setWindowTitle("Mode Création")

        self.image_path = image_path
        self.cell_size = cell_size

        self.pixmap_original = QPixmap(self.image_path)
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

        titre = QLabel("Mode Création")
        titre.setStyleSheet("font-size: 16px; font-weight: bold;")
        texte = QLabel("Cliquez sur une case libre pour ajouter un produit à cet emplacement.")
        texte.setWordWrap(True)
        texte.setMaximumHeight(100)
        right_panel.addWidget(titre, stretch=0)
        right_panel.addWidget(texte, stretch=1)

        self.zone_produits = QVBoxLayout()
        scroll_content = QWidget()
        scroll_content.setLayout(self.zone_produits)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        right_panel.addWidget(scroll_area, stretch=4)

        self.bouton_ajout = QPushButton("+ Ajouter un produit")
        self.bouton_ajout.clicked.connect(self.ajouter_champ_produit)
        right_panel.addWidget(self.bouton_ajout, stretch=0)
        self.bouton_sauvegarder = QPushButton("💾 Sauvegarder")
        right_panel.addWidget(self.bouton_sauvegarder, stretch=0)

        self.inaccessible_cells = {(5, 10), (7, 12)}
        self.sectors = {}

        self.dernier_champ = None
        self.ajouter_champ_produit()

        self.show()

    def ajouter_champ_produit(self):
        if self.dernier_champ is not None:
            self.dernier_champ.setDisabled(False)
        champ = QTextEdit()
        champ.setFixedHeight(40)
        champ.textChanged.connect(lambda: self.limiter_texte(champ))
        self.zone_produits.addWidget(champ)
        self.dernier_champ = champ

    def limiter_texte(self, champ):
        texte = champ.toPlainText()
        if len(texte) > 100:
            champ.setPlainText(texte[:100])
            cursor = champ.textCursor()
            cursor.setPosition(100)
            champ.setTextCursor(cursor)

    def afficher_popup(self, titre, message):
        msg = QMessageBox()
        msg.setWindowTitle(titre)
        msg.setText(message)
        msg.exec()

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