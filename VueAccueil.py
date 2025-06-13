import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, pyqtSignal

class VueAccueil(QWidget):
    # Interface graphique de la page d'accueil lors du lancement de l'application, permettant de choisir entre les deux modes : création ou utilisation
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
