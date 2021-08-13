import sys
from PyQt5.QtWidgets import QApplication
from window import DownloaderWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloaderWindow()
    sys.exit(app.exec_())