from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu)


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.icon = QIcon("img/icon.png")
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)

        show_action = QAction("Показать", self)
        quit_action = QAction("Закрыть", self)
        hide_action = QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Приложение скрыто в трей",
            QSystemTrayIcon.MessageIcon(1),
            2000
        )


def main():
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    MainWindow = MainWindows()
    # скрытие из панели задач
    MainWindow.setWindowFlags(QtCore.Qt.WindowType.Tool)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
