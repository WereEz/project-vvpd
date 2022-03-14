from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu, QLabel)


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.unit = 1
        self.tray()
        

    def tray(self):
        self.icon = QIcon("img/icon.png")
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.close = False
        self.show_action = QAction("Показать", self)
        self.quit_action = QAction("Закрыть", self)
        self.hide_action = QAction("Скрыть", self)
        self.hide_in_tray_action = QAction("Скрыть", self)
        self.hide_in_tray_action.triggered.connect(self.hide_in_tray)
        self.show_action.triggered.connect(self.show)
        self.hide_action.triggered.connect(self.hide)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu = QMenu()
        tray_menu.addAction(self.show_action)
        tray_menu.addAction(self.hide_action)
        tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def ui_resize(self):
        self.setFixedSize(int(350*self.unit),int(350*self.unit))  
        self.hedghehog()

    def hedghehog(self):
        pixmap = QPixmap("img/ez.png")
        self.hed_pic = QLabel(self)
        self.hed_pic.setScaledContents(True)
        self.hed_pic.resize(self.width(), self.width())
        self.hed_pic.setPixmap(pixmap)

    def hide_in_tray(self):
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Приложение скрыто в трей",
                QSystemTrayIcon.MessageIcon(1),
                2000
                ) 
                
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
        else:
            context = QMenu(self)
            context.addAction(self.hide_in_tray_action)
            context.addAction(self.quit_action)
            context.exec(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
      self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
      self.dragPos = event.globalPosition().toPoint()
      event.accept()

def main():
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    unit = app.primaryScreen().size().height() / 1000 # unit - одна тысячная от высоты экрана, все размеры умножаются на него
    
    MainWindow = MainWindows()
    MainWindow.unit = unit
    MainWindow.ui_resize()
    MainWindow.setWindowFlags(QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint) # скрытие из панели задач
    MainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()