from PyQt5.QtWidgets import QMainWindow, QPushButton, QFrame, QScrollArea, QLabel
from habit.habit_widget import HabitWidget
from to_do.to_do_widget import ToDoWidget, get_shadow_effect
from plant.plant_widget import PlantWidget
from main_window.tab_bar import TabBar
from PyQt5.QtGui import *
from plant.gold_coin import  GoldCoin
from medal.medal_wall import MedalWallFrame
from PyQt5.QtCore import Qt
import ctypes

class HomeWindow(QMainWindow):

    h_width = 1200
    h_height = 700

    h_habit_widget = None
    h_to_do_widget = None
    h_plant_widget = None
    h_medal_widget = None
    h_tab_bar = None
    h_gold_coin=None
    h_statistic = None
    is_in_tray=False

    h_help_button = None
    h_help_window = None

    # 文件地址
    to_do_style_path = 'gui/to_do_widget.qss'
    habit_style_path = 'gui/habit_widget.qss'
    plant_style_path = 'gui/plant_widget.qss'
    medal_style_path = 'gui/medal_widget.qss'

    def __init__(self,statistic):
        super().__init__()
        self.setFixedSize(self.h_width, self.h_height)
        #设置图标
        self.setWindowIcon(QIcon("data/ui/icon/icon.png"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("data/ui/icon/icon.png")

        self.setWindowTitle("Habit Plant")
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.h_gold_coin=GoldCoin()
        self.h_statistic=statistic

        self.h_habit_widget = HabitWidget(self,self.h_gold_coin,self.h_statistic)
        self.h_to_do_widget = ToDoWidget(self,self.h_gold_coin,self.h_statistic)
        self.h_plant_widget = PlantWidget(self,self.h_gold_coin)
        self.h_medal_widget = MedalWallFrame(self,self.h_statistic)
        self.h_tab_bar = TabBar(self)

        self.h_help_button = QPushButton(self)
        self.h_help_window = HelpWindow()

        self.h_help_button.setObjectName("help_button")

        # 信号绑定
        self.h_tab_bar.to_do_button.clicked.connect(self.to_do_widget_tab_clicked)
        self.h_tab_bar.habit_button.clicked.connect(self.habit_widget_tab_clicked)
        self.h_tab_bar.plant_button.clicked.connect(self.plant_widget_tab_clicked)
        self.h_tab_bar.medal_button.clicked.connect(self.medal_widget_tab_clicked)
        self.h_plant_widget.h_farm.add_medal.connect(self.h_medal_widget.h_medal_wall.add_medals)
        self.h_help_button.clicked.connect(self.h_help_window.wake_up)

        # 初始化ui
        self.init_ui()

    def init_ui(self):

        self.show()

        # 设置主窗口透明
        self.border_width = 8
        # 设置 窗口无边框和背景透明 *必须
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # 三个主要窗口的显示与隐藏
        self.habit_widget_tab_clicked()

        # tab_bar布局
        x_space = int((self.h_width-self.h_tab_bar.h_width)/2)
        y_space = int(self.h_height-self.h_tab_bar.h_height-10)
        self.h_tab_bar.move(x_space, y_space)

        self.h_help_button.setGeometry(1060, self.h_tab_bar.geometry().y()+15, 60, 60)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    def to_do_widget_tab_clicked(self):
        self.set_style(self.to_do_style_path)

        self.h_to_do_widget.show()
        self.h_habit_widget.hide()
        self.h_plant_widget.hide()
        self.h_medal_widget.hide()

    def habit_widget_tab_clicked(self):
        self.set_style(self.habit_style_path)

        self.h_to_do_widget.hide()
        self.h_habit_widget.show()
        self.h_plant_widget.hide()
        self.h_medal_widget.hide()

    def plant_widget_tab_clicked(self):
        self.set_style(self.plant_style_path)

        self.h_to_do_widget.hide()
        self.h_habit_widget.hide()
        self.h_plant_widget.show()
        self.h_medal_widget.hide()

    def medal_widget_tab_clicked(self):
        self.set_style(self.medal_style_path)

        self.h_to_do_widget.hide()
        self.h_habit_widget.hide()
        self.h_plant_widget.hide()
        self.h_medal_widget.show()

    def closeEvent(self, event):
        if(self.isVisible()):
            event.ignore()
            self.setVisible(False)
        else:
            self.h_statistic.save_to_local()
            self.h_medal_widget.h_medal_wall.save_to_file()
            event.accept()


class HelpWindow(QFrame):
    path='gui/home_window.QSS'
    h_width=946
    h_height=800
    list_box_width=946
    list_box_height=670
    list_box_frame_width=946
    list_box_frame_height=22046
    button_width=60
    button_height=60
    button = None
    label = None
    list_box=None
    list_box_frame=None


    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.label=QLabel(self)
        self.button = QPushButton(self)
        self.list_box=QScrollArea(self)
        self.list_box_frame=QFrame(self.list_box)
        self.list_box.setWidget(self.list_box_frame)


        self.button.clicked.connect(self.close)
        self.init_ui()

    def wake_up(self):
        self.show()
        self.setWindowModality(Qt.ApplicationModal)

    def init_ui(self):
        self.list_box.setObjectName("help_list_box")
        self.list_box_frame.setObjectName("help_help_list_box")
        self.button.setObjectName("help_button")
        self.label.setObjectName("help_bg")
        self.list_box.setFrameShape(QFrame.NoFrame)

        self.button.setGraphicsEffect(get_shadow_effect(self))

        self.resize(self.h_width,self.h_height)
        self.list_box.resize(self.list_box_width,self.list_box_height)
        self.list_box_frame.resize(self.list_box_frame_width,self.list_box_frame_height)
        self.button.resize(self.button_width,self.button_height)
        self.label.resize(self.h_width,self.h_height)

        self.list_box.move((self.h_width-self.list_box_width)/2,(self.h_height-self.list_box_height)/2-30)
        self.button.move(self.h_width/2-self.button_width/2,self.h_height-self.button_height-20)
        self.set_style(self.path)


    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

