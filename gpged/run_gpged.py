from PyQt6.QtWidgets import QApplication
from gpged.app import GPGED
import sys

def run_app():
    app = QApplication(sys.argv)
    ex = GPGED()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
