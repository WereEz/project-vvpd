from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPalette, QColor, QFontDatabase, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFrame, QScrollArea, QFileDialog, QSizePolicy, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QHBoxLayout, QLineEdit, QWidget, QVBoxLayout)
import time
import json
import os
import threading
import recognition
import functional
import requests


def check_site(site_name=""):
    domens = ['.ru', '.com', '.рф', '.net', '.org', '.ru.net', '.pro', '.ua', ]
    if any([domen in site_name for domen in domens]):
        return 1


class Appearance(QWidget):
    def __init__(self, parent=None):
        super().__init__()


class FastAccess(QWidget, ):
    def __init__(self, parent=None, unit = 1):
        super().__init__()
        self.delete_ico = QPixmap("img/delete.svg")
        self.edit_ico = QPixmap("img/edit.svg")
        self.folder_ico = QPixmap("img/folder.svg")
        self.add_ico = QPixmap("img/add.svg")
        self.form = QWidget()
        self.unit = unit
        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.addStretch()  # Это добавит пружину, прижимающую виджеты вверх

        super().__init__()
        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        # Widget that contains the collection of Vertical Box
        self.widget = QWidget()
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.lines = QVBoxLayout()
        self.lines.setSpacing(self.height()/50)
        self.lines.setContentsMargins(
            self.width()/60, self.height()/50, self.width()/50, self.height()/50)
        self.widget.setLayout(self.lines)
        self.widget.setObjectName("main")

        self.widget.setStyleSheet("""QWidget#main {background-color: #e7e6e1;
                                     border-radius: 10%;}
                                     QLabel { background-color: #FFFFFF;
                                     border-radius: 10%;
                                     padding: 0% 5% 0% 5%;}""")

        self.form.setStyleSheet("""QLineEdit {background-color: #e7e6e1;
                                     border-radius: 10%;
                                     padding: 0% 5% 0% 5%;}""")

        self.scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setStyleSheet("border-radius: 10%")
        self.lines.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        main_layout = QVBoxLayout()
        self.setStyleSheet("border-radius: 10%")
        main_layout.addWidget(self.scroll)
        main_layout.addWidget(self.form)
        self.create_form()
        self.setLayout(main_layout)

    def save(self):
        a = {"sites": self.sites,
             "folders": self.folders}
        with open("commands.json", "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2, ensure_ascii=False)
        for i in reversed(range(self.lines.count())):
            self.lines.itemAt(i).widget().setParent(None)
        self.filling()

    def delete(self, i):
        try:
            del self.sites[i]
        except:
            del self.folders[i]
        self.save()

    def filling(self):
        for i in reversed(range(self.lines.count())):
            self.lines.itemAt(i).widget().setParent(None)

        with open("commands.json", "r", encoding="utf-8") as read_file:
            commands = json.load(read_file)

        self.sites = commands["sites"]
        self.folders = commands["folders"]
        for x in self.sites.items():
            self.add_button(x[1], x[0])
        for x in self.folders.items():
            self.add_button(x[1], x[0])

    def add_adress(self):
        file = str(QFileDialog.getExistingDirectory(self, "Выберите папку"))
        self.adress.setText(file)

    def add_command(self):
        name = self.name.text()
        if name:
            name = name.replace(",", " ")
            name = name.replace(".", " ")
            name = name.replace(";", " ")

            name = list(set(name.split(" ")))
            print(name)
            if "" in name:
                name.remove("")
            if all([x.isalpha() for x in name]):
                if (os.path.isfile(self.adress.text()) or os.path.isdir(self.adress.text())):
                    self.folders[self.adress.text()] = name
                elif check_site(self.adress.text()):
                    self.sites[self.adress.text()] = name
                else:
                    return

                self.save()

    def create_form(self):
        layout = QHBoxLayout()
        height = self.height()/12
        self.name = QLineEdit()
        self.adress = QLineEdit()
        self.name.setPlaceholderText("Названия")
        self.adress.setPlaceholderText("Ссылка или путь")

        self.adress.setFixedHeight(height)
        self.name.setFixedHeight(height)

        self.directory_btn = QPushButton()
        self.directory_btn.setFixedSize(height, height)
        self.directory_btn.setIcon(QIcon(self.folder_ico))
        self.directory_btn.setStyleSheet("background-color: transparent;")
        self.directory_btn.setIconSize(self.directory_btn.size())
        self.directory_btn.clicked.connect(self.add_adress)

        self.add_btn = QPushButton()
        self.add_btn.setFixedSize(height, height)
        self.add_btn.setIcon(QIcon(self.add_ico))
        self.add_btn.setStyleSheet("background-color: transparent;")
        self.add_btn.setIconSize(self.add_btn.size())
        self.add_btn.clicked.connect(self.add_command)

        layout.addWidget(self.name)
        layout.addWidget(self.adress)
        layout.addWidget(self.directory_btn)
        layout.addWidget(self.add_btn)
        self.form.setLayout(layout)

    def edit(self, adress):
        self.adress.setText(adress)
        try:
            name = self.sites[adress]
        except:
            name = self.folders[adress]

        if isinstance(name, list):
            name = ", ".join(name)

        self.name.setText(name)

    def add_button(self, name, adress):
        layout = QHBoxLayout()
        line = QWidget()
        height = self.height()/10
        line.setFixedHeight(height)
        line.setFixedWidth(self.width()*0.85)
        layout.setContentsMargins(0, 0, 0, 0)

        if isinstance(name, list):
            name = ", ".join(name)
        name = QLabel(name)
        name.setTextInteractionFlags(
            (QtCore.Qt.TextInteractionFlag.TextSelectableByMouse))
        name.setFixedWidth(self.width()/4)
        adress = QLabel(adress)
        adress.setTextInteractionFlags(
            (QtCore.Qt.TextInteractionFlag.TextSelectableByMouse))

        delete_btn = QPushButton()
        delete_btn.setFixedSize(height, height)
        delete_btn.setIcon(QIcon(self.delete_ico))
        delete_btn.setStyleSheet("background-color: transparent;")
        delete_btn.setIconSize(delete_btn.size())
        delete_btn.clicked.connect(lambda: self.delete(adress.text()))

        edit_btn = QPushButton()
        edit_btn.setFixedSize(height, height)
        edit_btn.setIcon(QIcon(self.edit_ico))
        edit_btn.setStyleSheet("background-color: transparent;")
        edit_btn.setIconSize(delete_btn.size())
        edit_btn.clicked.connect(lambda: self.edit(adress.text()))

        name.setFont(QFont("Balsamiq Sans", int(11*self.unit)))
        adress.setFont(QFont("Balsamiq Sans", int(11*self.unit)))
        layout.addWidget(name)
        layout.addWidget(adress)
        layout.addWidget(delete_btn)
        layout.addWidget(edit_btn)
        line.setLayout(layout)

        # Добавление в начало, с пружиной это прижмет вверх
        self.lines.insertWidget(0, line)
        # self.layout_buttons.addWidget(button)  # Добавление в конец, с пружиной это прижмет вниз


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.unit = 1
        self.init()
        self.ui_resize()

    def init(self):
        self.setWindowTitle("Settings")
        self.background = QWidget(self)
        self.line = QWidget(self)
        QFontDatabase.addApplicationFont('img\BalsamiqSans-Regular.ttf')
        # местами поменять надо, случайно изначально их перепутал
        self.AppearenceBttn = QPushButton("быстрый доступ", parent=self)
        self.FastAccessBttn = QPushButton("внешний вид", parent=self)
        self.ExitBttn = QPushButton(self)
        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        self.stacklayout.setContentsMargins(0, 0, 0, 0)
        pagelayout.setContentsMargins(0, 0, 0, 0)
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        self.stacklayout.addWidget(FastAccess(unit = self.unit))
        self.stacklayout.addWidget(Appearance())

        self.widget = QWidget()
        self.widget.setLayout(pagelayout)
        self.setCentralWidget(self.widget)
        button_layout.addWidget(self.FastAccessBttn)
        button_layout.addWidget(self.AppearenceBttn)
        button_layout.addWidget(self.ExitBttn)

        self.AppearenceBttn.clicked.connect(self.Appearence_clicked)
        self.FastAccessBttn.clicked.connect(self.FastAccess_clicked)
        self.ExitBttn.clicked.connect(self.close)
        style = """border: none;"""
        self.setStyleSheet(style)

        self.line.setFixedHeight(self.height()/16)
        self.line.setFixedWidth(self.width())
        self.background.setFixedWidth(self.width())
        self.background.setFixedHeight(self.height())
        self.line.setStyleSheet("background-color: #CFCABC;")
        self.background.setStyleSheet("""
                                        border-image : url("img/bkg.png") 0 0 0 0 stretch stretch;""")

    def ui_resize(self):
        self.setFixedSize(int(400*self.unit), int(500*self.unit))
        self.tabs()

    def tabs(self):
        self.AppearenceBttn.setMinimumSize(
            self.width()/2-self.height()/4, self.height()/8)
        self.FastAccessBttn.setMinimumSize(
            self.width()/2-self.height()/4, self.height()/8)
        self.ExitBttn.setFixedSize(self.height()/8+2, self.height()/8)
        self.FastAccessBttn.move(self.AppearenceBttn.size().width(), 0)

        exit_ico = QPixmap("img/close.svg")
        self.ExitBttn.setIcon(QIcon(exit_ico))
        self.ExitBttn.setIconSize(self.ExitBttn.size()/2)

        self.gray_btn = """background-color: #CFCABC;
                        border: none;"""
        self.white_btn = """background-color: #FFFFFF;
                        border: none;"""

        self.close_btn = """background-color: #FFFFFF;"""
        self.AppearenceBttn.setStyleSheet(self.gray_btn)
        self.FastAccessBttn.setStyleSheet(self.gray_btn)
        self.AppearenceBttn.setFont(QFont("Balsamiq Sans", int(13*self.unit)))
        self.FastAccessBttn.setFont(QFont("Balsamiq Sans", int(13*self.unit)))
        self.ExitBttn.setStyleSheet(
            self.close_btn + " border-top-left-radius: 25%;")

        self.FastAccess_clicked()

    def FastAccess_clicked(self):

        self.stacklayout.setCurrentIndex(1)
        style = """background-color: #FFFFFF;
                border: none;
                border-top-right-radius: 25%;
                color: #5b5847"""

        bstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-left-radius: 25%;
                border-bottom-right-radius: 25%;
                color: #FFFFFF;"""

        self.FastAccessBttn.setStyleSheet(style)
        self.AppearenceBttn.setStyleSheet(bstyle)
        self.ExitBttn.setStyleSheet(
            self.close_btn + " border-top-left-radius: 25%;")

    def Appearence_clicked(self):
        self.stacklayout.setCurrentIndex(0)
        self.stacklayout.widget(0).filling()

        style = """background-color: #FFFFFF;
                border: none;
                border-top-left-radius: 25%;
                color: #5b5847"""

        bstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-right-radius: 25%;
                color: #FFFFFF"""

        self.AppearenceBttn.setStyleSheet(style)
        self.FastAccessBttn.setStyleSheet(bstyle)
        self.ExitBttn.setStyleSheet(self.close_btn)

    def mousePressEvent(self, event):  # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):  # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(
                self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()


def main():
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # unit - одна тысячная от высоты экрана, все размеры умножаются на него
    unit = app.primaryScreen().size().height() / 1000
    Settings = SettingsWindow()
    Settings.unit = unit
    Settings.ui_resize()
    Settings.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
