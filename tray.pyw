from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPalette, QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QGroupBox, QWidget, QMainWindow, QSystemTrayIcon, QHBoxLayout, QVBoxLayout,  QFormLayout, QMenu, QLabel, QPushButton, QLineEdit, QScrollArea)
from time import sleep
from settings import SettingsWindow
import json
import threading
import sys
import psutil
import logging
import pyttsx3

import recognition
import functional


class InpLine(QLineEdit):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)


class MainWindows(QMainWindow):
    def __init__(self, unit = 1):
        super().__init__()
        self.rec = False
        self.hand_inp_is_work = False
        self.unit = unit
        self.unit_sett = unit
        self.tray()
        self.init()
        self.answer = False

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
        self.quit_action.triggered.connect(self.quit)
        tray_menu = QMenu()
        tray_menu.addAction(self.show_action)
        tray_menu.addAction(self.hide_action)
        tray_menu.addAction(self.quit_action)
        tray_menu.addAction(self.sett_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def init(self):
        # создал новый класс чтобы можно было отслеживать клик по полю ввода, на будущее
        self.inp = InpLine(self)
        self.btn = QPushButton(self)
        self.send_btn = QPushButton(self)

    def ui_resize(self):
        self.import_prefs()
        self.setFixedSize(int(350*self.unit), int(500*self.unit))
        self.hedghehog()
        self.inp_bttn()

    def quit(self):
        self.close = True
        QApplication.instance().quit()

    def import_prefs(self):
        with open("prefs.json", "r", encoding="utf-8") as read_file:
            prefs = json.load(read_file)
        self.unit = self.unit_sett * prefs["unit"]/100

    def inp_bttn(self):
        self.btn_size = int(60*self.unit)
        self.btn.setFixedSize(self.btn_size, self.btn_size)
        radius = self.btn_size//2
        border = int(0*self.unit)

        self.btn_style = f"""background-color: rgba(0, 0, 0, 0.2);
                    border-radius: {radius}px;
                    border: none;
                    font-size:{int(radius*0.8)}px;
                    color:  white;
                    """
        self.btn.setStyleSheet("background-color: rgba(255, 255, 255, 0.0)")

        btn_ico = QPixmap("img/dark_btn.svg")
        self.btn.setIcon(QIcon(btn_ico))
        self.btn.setIconSize(self.btn.size())

        self.btn.move(int(80*self.unit - self.btn.width()/2),
                      int(self.width()*0.85))

        self.inp.setFixedSize(int(250*self.unit), self.btn_size)
        self.inp.move(int(self.width()/2 - self.inp.width()/2.05),
                      int(self.width()*0.85))
        self.inp.setStyleSheet(
            self.btn_style + f" padding-left: {int(self.btn_size*1.1)};")
        self.inp_hide_thr = threading.Thread(target=self.inp_hide)

        send_btn_ico = QPixmap("img/send_dark_bttn.svg")
        self.send_btn.setIcon(QIcon(send_btn_ico))
        self.send_btn.setIconSize(self.send_btn.size()*1.3)

        self.send_btn.setFixedSize(self.btn_size, self.btn_size)
        self.send_btn.move(int(self.inp.width()+self.inp.width()
                           * 0.08+self.btn_size/2), int(self.width()*0.85))
        self.send_btn.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.0)")
        self.send_btn.hide()

        self.thr = threading.Thread(target=self.voice_recognition)
        self.btn.clicked.connect(self.btn_click)
        self.inp.textEdited.connect(self.hand_inp)
        self.inp.editingFinished.connect(self.open_smth)

        # self.btn.clicked.connect() // при клике на кнопку !!
        # self.inp.clicked.connect() // при клике на поле ввода !!
        self.send_btn.clicked.connect(self.open_smth)

    def hand_inp(self):
        if self.inp.text():
            self.hand_inp_is_work = True
            self.btn.hide()
            self.send_btn.show()
            self.inp.setStyleSheet(
                self.btn_style + f" padding-left: {int(self.btn_size*0.5)};")
        else:
            self.send_btn.hide()
            self.btn.show()
            self.hand_inp_is_work = False
            self.inp.setStyleSheet(
                self.btn_style + f" padding-left: {int(self.btn_size*1.1)};")
            if not self.underMouse():
                self.leaveEvent(QtCore.QEvent.Type.KeyPress)

    def inp_hide(self):
        sleep(1)
        if not self.close:
            if self.hiden:
                self.btn.hide()
                self.inp.hide()
                self.send_btn.hide()

    def enterEvent(self, event):
        self.hiden = False
        self.inp.show()
        if not self.hand_inp_is_work:
            self.btn.show()
        else:
            self.send_btn.show()

    def leaveEvent(self, event):
        if not (self.inp_hide_thr.is_alive() or self.hand_inp_is_work):
            self.hiden = True
            self.inp_hide_thr.start()
            self.inp_hide_thr = threading.Thread(target=self.inp_hide)

    def open_settings(self):
        self.settings = SettingsWindow(self)
        self.settings.unit = self.unit_sett
        self.settings.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.settings.ui_resize()
        self.settings.show()

    def hedghehog(self):
        pixmap = QPixmap("img/ez.png")
        self.hed_pic = QLabel(self)
        self.hed_pic.setScaledContents(True)
        self.hed_pic.resize(int(self.width()*0.8), int(self.width()*0.8))
        self.hed_pic.move(int(0.1*self.width()), 0)
        self.hed_pic.setPixmap(pixmap)
        self.output = QLabel(self)
        self.output.move(int(self.width()*0.4),
                         int(self.hed_pic.height()*0.19))
        QFontDatabase.addApplicationFont('img\BalsamiqSans-Regular.ttf')
        self.output.setFixedSize(int(160*self.unit), int(210*self.unit))
        self.output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.output.setFont(QFont("Balsamiq Sans", int(16*self.unit)))

    def hide_in_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Приложение скрыто в трей",
            QSystemTrayIcon.MessageIcon(1),
            2000
        )

    def default(self):
        self.answer = False
        pixmap = QPixmap("img/ez.png")
        self.hed_pic.setPixmap(pixmap)
        self.output.setText("")

    def answering(self, text):
        self.answer = True
        pixmap = QPixmap("img/mbox.png")

        self.hed_pic.setPixmap(pixmap)
        self.output.setText(text)

    def mousePressEvent(self, event):  # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            if self.answer:
                self.default()

        else:
            context = QMenu(self)
            context.addAction(self.hide_in_tray_action)
            context.addAction(self.quit_action)
            context.addAction(self.sett_action)
            context.exec(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):  # перетаскивание
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()

    def btn_click(self):
        self.thr.start()
        self.thr = threading.Thread(target=self.voice_recognition)

    def open_smth(self):
        command = self.inp.text()
        # запретить редактировать
        with open("commands.json", "r", encoding="utf-8") as read_file:
            commands = json.load(read_file)
        success = functional.execute_command(commands, command)
        if success == 0:
            sleep(1)
            self.inp.setText("Команда не выполнена")
        else:
            tts = pyttsx3.init()
            RU_VOICE_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Anna"
            tts.setProperty('voice', RU_VOICE_ID)
            tts.say(command)
            tts.runAndWait()
            tts.stop()
        print(success)
        sleep(1)
        if isinstance(success, str):
            self.answering(success)
        self.inp.setText("")
        self.hand_inp()
        self.inp.setReadOnly(False)

    def voice_recognition(self):
        self.rec = True  # для отслеживания, что запись идет
        self.inp.setReadOnly(True)
        orig_icon = self.btn.icon()
        btn_ico = QPixmap("img/record.svg")
        self.btn.setIcon(QIcon(btn_ico))

        self.inp.setText("Говорите")
        recognized_text = recognition.google_recognize()
        logging.info(recognized_text)
        self.inp.setText(recognized_text)
        if recognized_text != "Не распознано":
            self.open_smth()
        else:
            sleep(1)
            self.inp.setText("")
        self.btn.setIcon(orig_icon)
        self.rec = False


def main():
    proc_check = 0
    for proc in psutil.process_iter():
        name = proc.name()
        if name == "Voice_assistant.exe":
            proc_check += 1
    if proc_check > 2:
        sys.exit(0)
    logging.basicConfig(filename="log.log", level=logging.INFO)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # unit - одна тысячная от высоты экрана, все размеры умножаются на него
    unit = app.primaryScreen().size().height() / 1000
    MainWindow = MainWindows(unit = unit)
    MainWindow.ui_resize()
    MainWindow.setWindowFlags(QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.WindowStaysOnTopHint |
                              QtCore.Qt.WindowType.FramelessWindowHint)  # скрытие из панели задач
    MainWindow.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
