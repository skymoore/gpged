from PyQt6.QtWidgets import QApplication
from .app import GPGED
import sys

def main():
    app = QApplication(sys.argv)
    ex = GPGED()
    sys.exit(app.exec())
