from main_window import *
import qdarkstyle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PySide6'))
    window.show()
    sys.exit(app.exec())