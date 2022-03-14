from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu, QLabel, QPushButton, QLineEdit)
import threading
import recognition

class InpLine(QLineEdit):
  clicked = QtCore.pyqtSignal()
  def mouseReleaseEvent(self, QMouseEvent):
    if QMouseEvent.button()==QtCore.Qt.MouseButton.LeftButton:
      self.clicked.emit()



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
        self.setFixedSize(int(350*self.unit),int(500*self.unit))  
        self.hedghehog()
        self.inp_bttn()

    def inp_bttn(self):
        self.inp = InpLine(self) #создал новый класс чтобы можно было отслеживать клик по полю ввода, на будущее
        self.btn = QPushButton(self)
        btn_size = int(60*self.unit)
        self.btn.setFixedSize(btn_size,btn_size)
        radius = btn_size//2
        border = int(5*self.unit)
        self.btn.setText("Х")
        self.btn_style = f"""background-color: rgba(255, 255, 255, 0.5);
                    border-radius: {radius}px;
                    border: {border}px solid white;
                    color:  white;"""
        self.btn.setStyleSheet(self.btn_style)
        self.btn.move(int(80*self.unit - self.btn.width()/2),int(370*self.unit))

        self.inp.setFixedSize(int(250*self.unit),btn_size)
        self.inp.move(int(self.width()/2 - self.inp.width()/2),int(370*self.unit))
        self.inp.setStyleSheet(self.btn_style+f"padding-left: {btn_size};")

        self.send_btn = QPushButton(self)
        self.send_btn.setFixedSize(btn_size,btn_size)
        self.send_btn.move(self.inp.width()+self.inp.width()*0.05+btn_size/2,int(365*self.unit))
        self.send_btn.setText("▶")
        self.send_btn.setStyleSheet(f"""font-size: {btn_size+20}px;
                                       background-color: rgba(255, 255, 255, 0.0);
                                        border-radius: {radius}px;
                                        color:  rgba(255, 255, 255, 0.7);""")

        self.thr = threading.Thread(target=self.voice_recognition)
        self.btn.clicked.connect(self.btn_click)

        #self.btn.clicked.connect() // при клике на кнопку !! 
        #self.inp.clicked.connect() // при клике на поле ввода !! 
        #self.send_btn.connect() // при клике на кнопку ввода!!
        
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

    def mousePressEvent(self, event): # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
        else:
            context = QMenu(self)
            context.addAction(self.hide_in_tray_action)
            context.addAction(self.quit_action)
            context.exec(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event): # перетаскивание
      self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
      self.dragPos = event.globalPosition().toPoint()
      event.accept()

    def btn_click(self):
        self.thr.start()
    def voice_recognition(self):
        self.inp.setText("Говорите")
        recognized_text = recognition.google_recognize()
        self.inp.setText(recognized_text)

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