from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPalette, QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QGroupBox, QWidget, QMainWindow, QSystemTrayIcon, QHBoxLayout, QVBoxLayout,  QFormLayout, QMenu, QLabel, QPushButton, QLineEdit, QScrollArea)
from time import sleep
import json
import threading
import sys

import recognition
import functional

class InpLine(QLineEdit):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button()==QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)
      



class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rec = False
        self.hand_inp_is_work = False
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
        self.sett_action = QAction("Настройки", self)
        self.sett_action.triggered.connect(self.open_settings)
        self.hide_in_tray_action.triggered.connect(self.hide_in_tray)
        self.show_action.triggered.connect(self.show)
        self.hide_action.triggered.connect(self.hide)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu = QMenu()
        tray_menu.addAction(self.show_action)
        tray_menu.addAction(self.hide_action)
        tray_menu.addAction(self.quit_action)
        tray_menu.addAction(self.sett_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def ui_resize(self):
        self.setFixedSize(int(350*self.unit),int(500*self.unit))  
        self.hedghehog()
        self.inp_bttn()

    def inp_bttn(self):
        
        self.inp = InpLine(self) #создал новый класс чтобы можно было отслеживать клик по полю ввода, на будущее
        self.btn = QPushButton(self)
        self.btn_size = int(60*self.unit)
        self.btn.setFixedSize(self.btn_size,self.btn_size)
        radius = self.btn_size//2
        border = int(0*self.unit)

        self.btn_style = f"""background-color: rgba(0, 0, 0, 0.2);
                    border-radius: {radius}px;
                    border: none;
                    color:  white;
                    """
        self.btn.setStyleSheet("background-color: rgba(255, 255, 255, 0.0)") 


        btn_ico = QPixmap("img/dark_btn.svg") 
        self.btn.setIcon(QIcon(btn_ico))
        self.btn.setIconSize(self.btn.size())

        self.btn.move(int(80*self.unit - self.btn.width()/2),self.width()*0.85)

        self.inp.setFixedSize(int(250*self.unit),self.btn_size)
        self.inp.move(int(self.width()/2 - self.inp.width()/2.05),self.width()*0.85)
        self.inp.setStyleSheet(self.btn_style + f" padding-left: {int(self.btn_size*1.1)};")
        self.inp_hide_thr = threading.Thread(target=self.inp_hide)
        
        
        self.send_btn = QPushButton(self)
        send_btn_ico = QPixmap("img/send_dark_bttn.svg") 
        self.send_btn.setIcon(QIcon(send_btn_ico))
        self.send_btn.setIconSize(self.send_btn.size()*1.3)

        self.send_btn.setFixedSize(self.btn_size,self.btn_size)
        self.send_btn.move(self.inp.width()+self.inp.width()*0.08+self.btn_size/2,self.width()*0.85)
        self.send_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0.0)") 
        self.send_btn.hide()

        self.thr = threading.Thread(target=self.voice_recognition)
        self.btn.clicked.connect(self.btn_click)
        self.inp.textEdited.connect(self.hand_inp)
        self.inp.editingFinished.connect(self.open_smth)

        #self.btn.clicked.connect() // при клике на кнопку !! 
        #self.inp.clicked.connect() // при клике на поле ввода !! 
        self.send_btn.clicked.connect(self.open_smth) 
        



        
    def hand_inp(self):
        if self.inp.text():
            self.hand_inp_is_work = True
            self.btn.hide()
            self.send_btn.show()
            self.inp.setStyleSheet(self.btn_style + f" padding-left: {int(self.btn_size*0.5)};")
        else:
            self.btn.show()
            self.send_btn.hide()
            self.hand_inp_is_work = False
            self.inp.setStyleSheet(self.btn_style + f" padding-left: {int(self.btn_size*1.1)};")
            if not self.underMouse():
                self.leaveEvent(QtCore.QEvent.Type.KeyPress)
        


    def inp_hide(self):
        sleep(1)

        if self.hiden:
            self.inp.hide()
            self.btn.hide()
            self.send_btn.hide()

    def enterEvent(self, event):
        self.hiden = False
        self.inp.show()
        if not self.hand_inp_is_work:
            self.btn.show()
        else:
            self.send_btn.show()
        
    def leaveEvent(self, event):
        if not (self.inp_hide_thr.is_alive() or self.inp.text()):
            self.hiden = True
            self.inp_hide_thr.start()
            self.inp_hide_thr = threading.Thread(target=self.inp_hide)

    def open_settings(self):
        self.sett = settings()
        self.sett.unit = self.unit
        self.sett.ui_resize()
        self.sett.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) #
        self.sett.show()


    def hedghehog(self):
        pixmap = QPixmap("img/ez.png")
        self.hed_pic = QLabel(self)
        self.hed_pic.setScaledContents(True)
        self.hed_pic.resize(self.width()*0.8, self.width()*0.8)
        self.hed_pic.move(0.1*self.width(),0)
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
            context.addAction(self.sett_action)
            context.exec(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event): # перетаскивание
      self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
      self.dragPos = event.globalPosition().toPoint()
      event.accept()

    def btn_click(self):
        self.thr.start()
        self.thr = threading.Thread(target=self.voice_recognition)
        

    
    def open_smth(self):
        command = self.inp.text()
         #запретить редактировать
        with open("commands.json", "r", encoding = "utf-8") as read_file:
                commands = json.load(read_file)
        success = functional.execute_command(commands, command)
        if success == 0:
            self.inp.setText("Команда не выполнена")
            sleep(1)
        self.inp.setText("")
        self.hand_inp()
        self.inp.setReadOnly(False)

    def voice_recognition(self):
        self.rec = True #для отслеживания, что запись идет
        self.inp.setReadOnly(True)
        orig_icon = self.btn.icon() 
        btn_ico = QPixmap("img/record.svg") 
        self.btn.setIcon(QIcon(btn_ico))

        self.inp.setText("Говорите")
        recognized_text = recognition.google_recognize()
        self.inp.setText(recognized_text)
        if recognized_text != "Не распознано":
            self.open_smth()
        else:
            sleep(1)
            self.inp.setText("")
        self.btn.setIcon(orig_icon)
        self.rec = False



    
class settings(QMainWindow):
    def __init__(self):
        super().__init__()

        

    def ui_resize(self):
        self.setFixedSize(int(645*self.unit),int(795*self.unit))  
        self.buttons()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labels()
        self.scroll_area()
        self.setStyleSheet("""QMainWindow {background-color: #ffffff;}""")


    def buttons(self):
        self.close_bttn = QPushButton(self)
        self.close_bttn_size = int(55*self.unit)
        self.close_bttn.setFixedSize(self.close_bttn_size,self.close_bttn_size)
        self.close_bttn.move(int(645*self.unit-self.close_bttn_size),int(5*self.unit)) 
        self.close_bttn.setStyleSheet("background-color: rgba(255, 255, 255, 0.0)") 
        close_ico = QPixmap("img/close.svg") 
        self.close_bttn.setIcon(QIcon(close_ico))
        self.close_bttn.setIconSize(self.close_bttn.size())
        self.close_bttn.clicked.connect(self.hide) 

    def labels(self):

        QFontDatabase.addApplicationFont('img\Pangolin-Regular.ttf')
        QFontDatabase.addApplicationFont('img\BalsamiqSans-Regular.ttf')
        self.add_name = QLabel(self)
        self.add_name.setText("Быстрый доступ")
        self.add_name.setFont(QFont("Pangolin", int(40*self.unit)))
        self.add_name.adjustSize()
        self.add_name.setStyleSheet("color: #5C5847")
        self.add_name.move(int( self.width()/2 - self.add_name.width()/2),int(20*self.unit))

    def mousePressEvent(self, event): # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.RightButton:
            self.dragPos = event.globalPosition().toPoint()

    def load_comm(self):
        with open("commands.json", "r", encoding = "utf-8") as read_file:
                commands = json.load(read_file)
        self.sites = commands["sites"]
        self.folders = commands["folders"]

    
    def mouseMoveEvent(self, event): # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.RightButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def click(self, i):
        try:
            del self.sites[self.help[i][0]]
        except:
            del self.folders[self.help[i][0]]
        a = {"sites": self.sites, 
            "folders":self.folders}
        with open("commands.json", "w", encoding = "utf-8") as f:
                json.dump(a, f, indent = 2, ensure_ascii=False)
        self.scroll_area()

    def scroll_area(self):
        wid = QWidget(self)
        
        self.load_comm()
        formLayer = QFormLayout()
        groupBox = QGroupBox()
        nameList = []
        adressList = []
        delete_bttns = []
        delete_ico = QPixmap("img/delete.svg") 

        self.help = list(self.sites.items()) + list(self.folders.items() )


        for i in range(len(self.help)):
            layout2 = QHBoxLayout()
            
            
            text = self.help[i][1]
            if isinstance(text, list):
                text = ", ".join(text)
            name = QLabel(str(text))
            name.setFont(QFont("Balsamiq Sans", int(17*self.unit)))
            name.adjustSize()
            name.setTextInteractionFlags((QtCore.Qt.TextInteractionFlag.TextSelectableByMouse))
            nameList.append(name)

            adress = QLabel(str(self.help[i][0]))
            adress.setFont(QFont("Balsamiq Sans", int(17*self.unit)))
            adress.adjustSize()
            adress.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            adressList.append(adress)
            button = QPushButton()
            button.clicked.connect(lambda state, x=i: self.click(x))
            button.setFixedSize(int(45 * self.unit),int(45 * self.unit))
            button.setIcon(QIcon(delete_ico))
            button.setIconSize(button.size())
            delete_bttns.append(button)
            
            layout2.addWidget(nameList[i])
            layout2.addWidget(adressList[i])
            layout2.addWidget(delete_bttns[i])
            formLayer.addRow(layout2)

        groupBox.setMaximumWidth(int(self.width()*0.88))
        groupBox.setLayout(formLayer)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        #scroll.setWidgetResizable(True)
        scroll.setFixedHeight(int(self.height()*0.8))
        scroll.setFixedWidth(int(self.width()*0.88))
        
        
        scroll.setStyleSheet("""QGroupBox { border-radius: 10px;}
                                QScrollArea {
                                border: none;
                                border-radius: 10%;
                                background-color: #e7e6e1;}
                                QLabel {
                                    background-color: #ffffff;
                                    border-radius: 10%;
                                    padding: 3px;
                                    margin: 3px;
                                }
                                QPushButton { background-color: rgba(255,255,255,0);}
                                """)
        

        
        
        wid.setFixedSize(scroll.size())
        layout = QVBoxLayout()
        wid.move(int( self.width()/2 - wid.width()/2),int(100*self.unit))
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(scroll)
        wid.setLayout(layout)
        wid.hide()
        wid.show()

        
def main():
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
