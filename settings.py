from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPalette, QColor, QFontDatabase, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSlider, QFrame, QScrollArea, QFileDialog, QSizePolicy, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QHBoxLayout, QLineEdit, QWidget, QVBoxLayout)
import sys
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


def restart():
    QtCore.QCoreApplication.quit()
    status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
    print(status)


class Appearance(QWidget):
    def __init__(self, parent=None, unit=1):
        super().__init__()
        self.unit = unit
        self.import_prefs()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.create_slider()
        self.create_buttons()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addStretch()

    def import_prefs(self):
        with open("prefs.json", "r", encoding="utf-8") as read_file:
            self.prefs = json.load(read_file)

    def create_slider(self):
        QFontDatabase.addApplicationFont('img\Pangolin-Regular.ttf')
        QFontDatabase.addApplicationFont('img\BalsamiqSans-Regular.ttf')
        self.handleSize = int(self.width()*0.12)
        self.slider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setFixedHeight(int(80*self.unit))
        self.slider.setFixedWidth(int(400*self.unit*0.7+20))
        self.slider.setMinimum(20)
        self.slider.setMaximum(180)
        self.slider.setSliderPosition(100)
        self.slider.setValue(self.prefs["unit"])
        self.slider.setSingleStep(5)
        self.slider.setTickInterval(5)

        self.slider_label = QLabel(self)
        self.slider_label.setFixedSize(int(180*self.unit), int(40*self.unit))
        self.slider_label.setText("Размер")
        self.slider_label.setFont(QFont("Pangolin", int(24*self.unit)))
        self.slider_label.setStyleSheet(
            "letter-spacing: 0.7em; color: #5C5847;")
        self.slider_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.slider_value = QLabel(self)
        self.slider_value.setFixedSize(int(180*self.unit), int(40*self.unit))
        self.slider_value.setText("%")
        self.slider_value.setFont(QFont("Balsamiq Sans", int(15*self.unit)))
        self.slider_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.slider_value.setStyleSheet(
            "letter-spacing: 0.5em; color: #5C5847;")

        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(
            self.slider_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(
            self.slider, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(
            self.slider_value, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.value_changed(self.prefs["unit"])
        self.slider.valueChanged.connect(self.value_changed)

    def create_buttons(self):
        height = int(self.height()/12)
        self.accept_ico = QPixmap("img/accept.svg")
        self.accept_btn = QPushButton()
        self.accept_btn.setFixedSize(height, height)
        self.accept_btn.setIcon(QIcon(self.accept_ico))
        self.accept_btn.setIconSize(self.accept_btn.size())
        self.accept_btn.setStyleSheet("background-color: transparent;")
        self.main_layout.addSpacing(100)
        self.main_layout.addWidget(
            self.accept_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.accept_btn.clicked.connect(self.accept)

    def accept(self):
        a = {"unit": self.slider.value()}
        with open("prefs.json", "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2, ensure_ascii=False)
        restart()

    def value_changed(self, i):
        self.handleSize = int((i+100)/100*400*self.unit*0.12)
        self.slider_value.setText(f"  {i}%")
        self.slider.setStyleSheet("""QSlider::groove:horizontal {
                                height: 10px;
                                border-radius: 5px; 
                                background-color: #AFAA9B;
                                margin: 0px 10px;
                                position: relative;
                                    top: 30px;}                               
                            QSlider::handle:horizontal {
                                image: url('img/handle.png');
                                position:relative;"""
                                  f"top:-{self.handleSize//2-4}px;"
                                  f"width: {self.handleSize}px;"
                                  f"margin: 0px -10px -{self.handleSize//2} -10px;}}")


class Scripts(QWidget):
    def __init__(self, parent=None, unit=1):
        super().__init__()
        self.delete_ico = QPixmap("img/delete.svg")
        self.edit_ico = QPixmap("img/edit.svg")
        self.folder_ico = QPixmap("img/folder.svg")
        self.add_ico = QPixmap("img/add.svg")
        self.accept_ico = QPixmap("img/accept.svg")
        self.form = QWidget()
        self.unit = unit
        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.addStretch()  # Это добавит пружину, прижимающую виджеты вверх

        super().__init__()

        self.form.setStyleSheet("""QLineEdit {background-color: #e7e6e1;
                                     border-radius: 10%;
                                     padding: 0% 5% 0% 5%;}""")

        self.create_scripts_scroll()
        self.create_actions_scroll()
        self.create_form()

        self.setStyleSheet("""
                            QScrollBar::add-line:vertical {
                            border: none;
                            background: white;
                            }
                            QScrollBar:vertical {
                            width: 10%;
                            background: transparent;
                            }
                            QScrollBar::handle:vertical {
                            background: #65605D;
                            width: 10%;
                            border-radius: 5%;
                            padding: 2px;
                            }
                            QScrollBar::sub-line:vertical {
                            border: none;
                            background: white;
                            }
                            QScrollArea: {border-radius: 10%}""")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scripts_scroll)
        main_layout.addWidget(self.actions_scroll)
        main_layout.addWidget(self.form)
        self.setLayout(main_layout)

    def filling(self):
        for i in reversed(range(self.scripts_lines.count())):
            self.scripts_lines.itemAt(i).widget().setParent(None)

        with open("commands.json", "r", encoding="utf-8") as read_file:
            commands = json.load(read_file)

        self.sites = commands["sites"]
        self.folders = commands["folders"]
        self.complexcommands = commands["complexcommands"]
        for x in self.complexcommands.items():
            self.add_button(x[0])

        layout = QHBoxLayout()
        line = QWidget()
        height = self.height()/10
        line.setFixedHeight(height)
        line.setFixedWidth(self.width()*0.85)
        layout.setContentsMargins(0, 0, 0, 0)

        add_btn = QPushButton()
        add_btn.setFixedSize(height, height)
        add_btn.setIcon(QIcon(self.add_ico))
        add_btn.setStyleSheet("background-color: transparent;")
        add_btn.setIconSize(add_btn.size())
        # add_btn.clicked.connect(self.add_new_action)
        layout.addWidget(add_btn)
        line.setLayout(layout)
        self.scripts_lines.insertWidget(-1, line)

    def filling_actions(self, name):
        self.hide_form()
        self.current_name = name
        for i in reversed(range(self.actions_lines.count())):
            self.actions_lines.itemAt(i).widget().setParent(None)
        for x in self.complexcommands[name]:
            self.add_actions(x)

        layout = QHBoxLayout()
        line = QWidget()
        height = self.height()/10
        line.setFixedHeight(height)
        line.setFixedWidth(self.width()*0.85)
        layout.setContentsMargins(0, 0, 0, 0)

        add_btn = QPushButton()
        add_btn.setFixedSize(height, height)
        add_btn.setIcon(QIcon(self.add_ico))
        add_btn.setStyleSheet("background-color: transparent;")
        add_btn.setIconSize(add_btn.size())
        add_btn.clicked.connect(self.add_new_action)
        layout.addWidget(add_btn)
        line.setLayout(layout)

        self.actions_lines.insertWidget(-1, line)

    def add_new_action(self):
        if "" not in self.complexcommands[self.current_name]:
            self.add_actions("")
            self.complexcommands[self.current_name].append("")

    def create_scripts_scroll(self):
        # Scroll Area which contains the widgets, set as the centralWidget
        self.scripts_scroll = QScrollArea()
        # Widget that contains the collection of Vertical Box
        self.scripts_widget = QWidget()
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.scripts_lines = QVBoxLayout()
        self.scripts_lines.setSpacing(self.height()//50)
        self.scripts_lines.setContentsMargins(
            self.width()//60, self.height()//50, self.width()//50, self.height()//50)
        self.scripts_widget.setLayout(self.scripts_lines)
        self.scripts_widget.setObjectName("main")

        self.scripts_widget.setStyleSheet("""QWidget#main {background-color: #e7e6e1;
                                     border-radius: 10%;}
                                     QLabel { background-color: #FFFFFF;
                                     border-radius: 10%;
                                     padding: 0% 5% 0% 5%;}""")
        self.scripts_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scripts_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scripts_scroll.setWidgetResizable(True)
        self.scripts_scroll.setWidget(self.scripts_widget)
        self.scripts_lines.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def create_actions_scroll(self):
        # Scroll Area which contains the widgets, set as the centralWidget
        self.actions_scroll = QScrollArea()
        # Widget that contains the collection of Vertical Box
        self.actions_widget = QWidget()
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.actions_lines = QVBoxLayout()
        self.actions_lines.setSpacing(self.height()//50)
        self.actions_lines.setContentsMargins(
            self.width()//60, self.height()//50, self.width()//50, self.height()//50)
        self.actions_widget.setLayout(self.actions_lines)
        self.actions_widget.setObjectName("main")

        self.actions_widget.setStyleSheet("""QWidget#main {background-color: #e7e6e1;
                                     border-radius: 10%;}
                                     QLabel { background-color: #FFFFFF;
                                     border-radius: 10%;
                                     padding: 0% 5% 0% 5%;}""")

        self.actions_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.actions_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.actions_scroll.setWidgetResizable(True)
        self.actions_scroll.setWidget(self.actions_widget)
        self.actions_lines.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def create_form(self):
        layout = QHBoxLayout()
        height = int(self.height()/12)
        self.adress = QLineEdit()
        self.adress.setPlaceholderText("Ссылка или путь")

        self.adress.setFixedHeight(height)

        self.directory_btn = QPushButton()
        self.directory_btn.setFixedSize(height, height)
        self.directory_btn.setIcon(QIcon(self.folder_ico))
        self.directory_btn.setStyleSheet("background-color: transparent;")
        self.directory_btn.setIconSize(self.directory_btn.size())
        self.directory_btn.clicked.connect(self.add_adress)

        self.accept_btn = QPushButton()
        self.accept_btn.setFixedSize(height, height)
        self.accept_btn.setIcon(QIcon(self.accept_ico))
        self.accept_btn.setStyleSheet("background-color: transparent;")
        self.accept_btn.setIconSize(self.accept_btn.size())
        self.accept_btn.clicked.connect(self.accept_command)

        layout.addWidget(self.adress)
        layout.addWidget(self.directory_btn)
        layout.addWidget(self.accept_btn)
        self.form.setLayout(layout)

    def accept_command(self):
        adress = self.complexcommands[self.current_name].index(
            self.current_adress)
        self.complexcommands[self.current_name][adress] = self.adress.text()
        self.save()
        self.filling_actions(self.current_name)
        self.current_adress = self.adress.text()

    def save(self):
        a = {"sites": self.sites,
             "folders": self.folders,
             "complexcommands": self.complexcommands}
        with open("commands.json", "w", encoding="utf-8") as f:
            json.dump(a, f, indent=2, ensure_ascii=False)
        for i in reversed(range(self.scripts_lines.count())):
            self.scripts_lines.itemAt(i).widget().setParent(None)
        self.filling()

    def add_adress(self):
        file = str(QFileDialog.getExistingDirectory(self, "Выберите папку"))
        self.adress.setText(file)

    def add_button(self, name):
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
        name.setFixedWidth(self.width()/1.7)

        delete_btn = QPushButton()
        delete_btn.setFixedSize(height, height)
        delete_btn.setIcon(QIcon(self.delete_ico))
        delete_btn.setStyleSheet("background-color: transparent;")
        delete_btn.setIconSize(delete_btn.size())
        #delete_btn.clicked.connect(lambda: self.delete_script(name.text()))

        edit_btn = QPushButton()
        edit_btn.setFixedSize(height, height)
        edit_btn.setIcon(QIcon(self.edit_ico))
        edit_btn.setStyleSheet("background-color: transparent;")
        edit_btn.setIconSize(delete_btn.size())
        edit_btn.clicked.connect(lambda: self.filling_actions(name.text()))

        name.setFont(QFont("Balsamiq Sans", int(11*self.unit)))
        layout.addWidget(name)
        layout.addWidget(delete_btn)
        layout.addWidget(edit_btn)
        line.setLayout(layout)
        self.scripts_lines.insertWidget(0, line)

    def delete_action(self, adress):
        self.complexcommands[self.current_name] = [
            x for x in self.complexcommands[self.current_name] if x != adress]
        self.save()
        self.filling_actions(self.current_name)

    def show_form(self):
        self.accept_btn.show()
        self.adress.show()
        self.directory_btn.show()

    def hide_form(self):
        self.accept_btn.hide()
        self.adress.hide()
        self.directory_btn.hide()

    def add_actions(self, adress):
        layout = QHBoxLayout()
        line = QWidget()
        height = self.height()/10
        line.setFixedHeight(height)
        line.setFixedWidth(self.width()*0.85)
        layout.setContentsMargins(0, 0, 0, 0)

        if isinstance(adress, list):
            adress = ", ".join(adress)
        adress = QLabel(adress)
        adress.setTextInteractionFlags(
            (QtCore.Qt.TextInteractionFlag.TextSelectableByMouse))
        adress.setFixedWidth(self.width()/1.7)

        delete_btn = QPushButton()
        delete_btn.setFixedSize(height, height)
        delete_btn.setIcon(QIcon(self.delete_ico))
        delete_btn.setStyleSheet("background-color: transparent;")
        delete_btn.setIconSize(delete_btn.size())
        delete_btn.clicked.connect(lambda: self.delete_action(adress.text()))

        edit_btn = QPushButton()
        edit_btn.setFixedSize(height, height)
        edit_btn.setIcon(QIcon(self.edit_ico))
        edit_btn.setStyleSheet("background-color: transparent;")
        edit_btn.setIconSize(delete_btn.size())
        edit_btn.clicked.connect(lambda: self.edit_action(adress.text()))

        adress.setFont(QFont("Balsamiq Sans", int(11*self.unit)))
        layout.addWidget(adress)
        layout.addWidget(delete_btn)
        layout.addWidget(edit_btn)
        line.setLayout(layout)
        self.actions_lines.insertWidget(0, line)

    def edit_action(self, adress):
        self.show_form()
        self.current_adress = adress
        self.adress.setText(adress)


class FastAccess(QWidget, ):
    def __init__(self, parent=None, unit=1):
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
        self.lines.setSpacing(self.height()//50)
        self.lines.setContentsMargins(
            self.width()//60, self.height()//50, self.width()//50, self.height()//50)
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
        self.setStyleSheet("""
                            QScrollBar::add-line:vertical {
                            border: none;
                            background: white;
                            }
                            QScrollBar:vertical {
                            width: 10%;
                            background: transparent;
                            }
                            QScrollBar::handle:vertical {
                            background: #65605D;
                            width: 10%;
                            border-radius: 5%;
                            padding: 2px;
                            }
                            QScrollBar::sub-line:vertical {
                            border: none;
                            background: white;
                            }
                            QScrollArea: {border-radius: 10%}""")
        main_layout.addWidget(self.scroll)
        main_layout.addWidget(self.form)
        self.create_form()
        self.setLayout(main_layout)

    def save(self):
        a = {"sites": self.sites,
             "folders": self.folders,
             "complexcommands": self.complexcommands}
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
        self.complexcommands = commands["complexcommands"]
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
        height = int(self.height()/12)
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
    def __init__(self, parent=None):
        super().__init__()
        self.unit = 1
        self.init()
        self.ui_resize()
        self.parent = parent

    def init(self):
        self.max = 0
        self.setWindowTitle("Settings")
        self.background = QWidget(self)
        self.line = QWidget(self)
        self.dragPos = None
        QFontDatabase.addApplicationFont('img\BalsamiqSans-Regular.ttf')
        # местами поменять надо, случайно изначально их перепутал
        self.AppearenceBttn = QPushButton("быстрый\nдоступ", parent=self)
        self.FastAccessBttn = QPushButton("внешний\nвид", parent=self)
        self.ScriptBttn = QPushButton("сценарии", parent=self)
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

        self.stacklayout.addWidget(FastAccess(unit=self.unit))
        self.stacklayout.addWidget(Appearance(parent=self, unit=self.unit))
        self.stacklayout.addWidget(Scripts(unit=self.unit))

        self.widget = QWidget()
        self.widget.setLayout(pagelayout)
        self.setCentralWidget(self.widget)
        button_layout.addWidget(self.FastAccessBttn)
        button_layout.addWidget(self.AppearenceBttn)
        button_layout.addWidget(self.ScriptBttn)
        button_layout.addWidget(self.ExitBttn)

        self.AppearenceBttn.clicked.connect(self.Appearence_clicked)
        self.FastAccessBttn.clicked.connect(self.FastAccess_clicked)
        self.ScriptBttn.clicked.connect(self.Scripts_clicked)
        self.ExitBttn.clicked.connect(self.close)
        style = """border: none;"""
        self.setStyleSheet(style)

        self.line.setFixedHeight(int(self.height()/16))
        self.line.setFixedWidth(self.width())
        self.background.setFixedWidth(self.width())
        self.background.setFixedHeight(self.height())
        self.line.setStyleSheet("background-color: #CFCABC;")
        self.background.setStyleSheet(
            """border-image : url("img/bkg.png") 0 0 0 0 stretch stretch;""")

    def ui_resize(self):
        self.setFixedSize(int(400*self.unit), int(500*self.unit))
        self.tabs()

    def tabs(self):
        self.AppearenceBttn.setMinimumSize(
            int(self.width()/3-self.height()/4), int(self.height()/8))
        self.FastAccessBttn.setMinimumSize(
            int(self.width()/3-self.height()/4), int(self.height()/8))
        self.ScriptBttn.setMinimumSize(
            int(self.width()/3-self.height()/4), int(self.height()/8))

        self.ExitBttn.setFixedSize(
            int(self.height()/8+2), int(self.height()/8))

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
        self.ScriptBttn.setStyleSheet(self.gray_btn)
        self.AppearenceBttn.setFont(QFont("Balsamiq Sans", int(15*self.unit)))
        self.FastAccessBttn.setFont(QFont("Balsamiq Sans", int(15*self.unit)))
        self.ScriptBttn.setFont(QFont("Balsamiq Sans", int(15*self.unit)))
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
                color: #FFFFFF;"""

        leftstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-right-radius: 25%;
                color: #FFFFFF"""

        self.ScriptBttn.setStyleSheet(leftstyle)
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
                border-top-right-radius: 25%;
                color: #5b5847"""

        rightstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-right-radius: 25%;
                color: #FFFFFF"""

        leftstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-right-radius: 25%;
                border-bottom-left-radius: 25%;
                color: #FFFFFF"""

        self.AppearenceBttn.setStyleSheet(style)
        self.FastAccessBttn.setStyleSheet(rightstyle)
        self.ScriptBttn.setStyleSheet(leftstyle)
        self.ExitBttn.setStyleSheet(
            self.close_btn + " border-top-left-radius: 25%;")

    def Scripts_clicked(self):

        self.stacklayout.setCurrentIndex(2)
        self.stacklayout.widget(2).filling()
        style = """background-color: #FFFFFF;
                border: none;
                border-top-left-radius: 25%;
                color: #5b5847"""

        bstyle = """background-color: #CFCABC;
                border: none;
                border-bottom-right-radius: 25%;
                color: #FFFFFF;"""

        leftstyle = """background-color: #CFCABC;
                border: none;
                color: #FFFFFF"""

        self.ScriptBttn.setStyleSheet(style)
        self.FastAccessBttn.setStyleSheet(leftstyle)
        self.AppearenceBttn.setStyleSheet(bstyle)
        self.ExitBttn.setStyleSheet(
            self.close_btn)

    def mousePressEvent(self, event):  # перетаскивание
        if event.buttons() == QtCore.Qt.MouseButton.RightButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):  # перетаскивание
        if self.dragPos != None:
            if event.buttons() == QtCore.Qt.MouseButton.RightButton:
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