import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class VuePlan(QWidget):
    def __init__(self, image_path: str, scale_percent: int = 100):
        super().__init__()

        self.setWindowTitle("Affichage plan redimensionné")

        self.image_path = image_path
        self.scale_percent = scale_percent

        self.pixmap_original = QPixmap(self.image_path)
        self.label = QLabel()

        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        new_width = int(screen_width * (self.scale_percent / 100))
        new_height = int(screen_height * (self.scale_percent / 100))

        self.pixmap_scaled = self.pixmap_original.scaled(
            new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
        )

        self.label.setPixmap(self.pixmap_scaled)
        self.label.mousePressEvent = self.get_mouse_position

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.resize(self.pixmap_scaled.width(), self.pixmap_scaled.height())

    def get_mouse_position(self, event):
        pos = event.position().toPoint()
        print(f"Clicked at x={pos.x()}, y={pos.y()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VuePlan("plan.jpg", scale_percent=95)
    window.show()
    sys.exit(app.exec())
