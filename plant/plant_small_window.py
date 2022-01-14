# -*- coding = utf-8 -*-
# @Time : 2021/4/26 11:04
# @Author : MiHao
# @File : plant_small_window.py
# @Software: PyCharm
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt, QTimer, QSize
from PyQt5.Qt import  QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFrame, QSystemTrayIcon, QMenu, QAction

SMALL_BUTTON_X = 50
SMALL_BUTTON_Y = 50

PLANT_X = 300
PLANT_Y = 300

CHAT_BUTTON_X = 230
CHAT_BUTTON_Y = 130

# 垂直间距
H_DISTANCE = 10
# 水平间距
V_DISTANCE = 5

NOTICE_COUNT=3600
UNNOTICE_COUNT=60
SEC_TO_HIDE=20
SEC_TO_SHOW=600


class PlantSmallWindow(QFrame):
    h_statistic=None

    #鼠标位置休息与鼠标位置控件 以及累计鼠标移动数
    last_mouse_pos=None
    mouse = None
    notice_count=0
    unnotice_count=0

    #计时器
    h_computer_timer=None
    h_unfinished_timer=None
    h_show_timer=None
    h_ready_todo_timer=None

    is_in_tray = True
    h_mainwindow=None

    #消息队列
    msg_list=[]

    style_path = 'gui/plant_small_window.qss'

    def __init__(self,statistic,plant):
        super().__init__()
        #设置基础不显示的控件
        self.h_statistic=statistic


        ### 此部分内容已由函数完成
        # # 设置stylesheet
        # self.style_file_path = 'gui/main_style.qss'
        # file = open(self.style_file_path, 'r',encoding='utf-8')
        # style_content = file.read()
        # self.setStyleSheet(style_content)

        # 设置透明窗口
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window
                            |Qt.Tool|Qt.WindowStaysOnTopHint
                            )

        self.desktop = QApplication.desktop()
        height = self.desktop.screenGeometry().height()
        width = self.desktop.screenGeometry().width()
        self.resize(width, height)

        # 植物窗口
        self.plant = DragPlant(self,plant)
        self.plant.move(width/8*6, height/5*3)
        self.plant.setObjectName("small_plant")

        plant_x = self.plant.geometry().x()
        plant_y = self.plant.geometry().y()

        # 浇水按钮
        self.water_button = QPushButton(self)
        self.water_button.setGeometry(plant_x + (self.plant.h_width - SMALL_BUTTON_X)/2, plant_y + self.plant.h_height + H_DISTANCE,
                                      SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.water_button.setObjectName("small_plant_water_button")

        # 聊天按钮 one line
        self.chat_button = ChatButton(self)
        self.chat_button.setGeometry(plant_x+(self.plant.h_width-CHAT_BUTTON_X)/2, plant_y-CHAT_BUTTON_Y,
                                     CHAT_BUTTON_X, CHAT_BUTTON_Y)
        self.chat_button.setObjectName("small_plant_chat_button")

        #计时器用于计算电脑使用多久
        self.h_computer_timer=QTimer(self)
        self.h_computer_timer.timeout.connect(self.long_time_use_computer)
        self.h_computer_timer.start(1000)

        #计时器用于计时要展示多久
        self.h_show_timer=QTimer(self)
        self.h_show_timer.timeout.connect(self.be_hide)

        #计时器用于计时多久需要展示 未完成事项信息
        self.h_unfinished_timer=QTimer(self)
        self.h_unfinished_timer.timeout.connect(self.push_unfinished)
        self.h_unfinished_timer.start(SEC_TO_SHOW*1000)

        #用于循环列表中的属性
        self.h_ready_todo_timer=QTimer(self)
        self.h_ready_todo_timer.timeout.connect(self.show_ready_todo)

        # 绑定控件
        self.plant.init_button(self.water_button, self.chat_button)

        #信号绑定
        self.h_statistic._ready_todo_signal.connect(self.accept_ready_todo)
        self.water_button.clicked.connect(lambda :self.h_mainwindow.show())
        self.plant.clicked.connect(lambda: self.h_mainwindow.show())

        #qss
        self.set_style(self.style_path)
        self.chat_button.hide()
        self.pbMin()

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    def be_hide(self):
        self.chat_button.hide()
        self.h_show_timer.stop()

    def show_low_priority_chat(self,text):
        if(not self.h_show_timer.isActive()):
            self.chat_button.setText(text)
            self.chat_button.show()
            self.h_show_timer.start(SEC_TO_HIDE*1000)
            return True
        return False

    def show_hight_priority_chat(self,text):
        self.chat_button.setText(text)
        self.chat_button.show()
        self.h_show_timer.start(SEC_TO_HIDE * 1000)

    def long_time_use_computer(self):
        now_mouse_pos=QCursor.pos()
        if(self.last_mouse_pos==None):
            self.last_mouse_pos=now_mouse_pos
        else:
            if(self.last_mouse_pos.y()!=now_mouse_pos.y() or self.last_mouse_pos.x()!=now_mouse_pos.x()):
                self.notice_count+=1
                self.last_mouse_pos=now_mouse_pos
                self.unnotice_count=0
            else:
                self.unnotice_count+=1
        if(self.notice_count>=NOTICE_COUNT):
            if(self.show_low_priority_chat("该休息了")):
                self.notice_count=0
        elif(self.unnotice_count==UNNOTICE_COUNT):
            self.notice_count=0

    def push_unfinished(self):
        try:
            todo=''
            myday=''
            habit=''
            if(self.h_statistic.to_do_unfinished_count!=0):
                todo="还有"+str(self.h_statistic.to_do_unfinished_count)+"待办未完成"+'\n'
            if(self.h_statistic.my_day_unfinished_count!=0):
                myday="还有"+str(self.h_statistic.my_day_unfinished_count)+"每日计划未完成"+'\n'
            if(self.h_statistic.habit_unfinished_count!=0):
                habit="还有"+str(self.h_statistic.habit_unfinished_count)+"习惯未完成"

            if(todo=='' and myday=='' and habit==' '):
                self.show_low_priority_chat("已经完成全部任务")
            else:
                self.show_low_priority_chat(todo+myday+habit)
        except Exception as e:
            pass


    def accept_ready_todo(self,list):
        self.msg_list.extend(list)
        self.show_ready_todo()

    def show_ready_todo(self):
        try:
            if((not self.h_ready_todo_timer.isActive()) and len(self.msg_list)>0):
                if(self.msg_list[0]["type"]!=0):
                    a="您的待办"+'\n'+self.msg_list[0]["title"]+'\n'+"还有"+str(self.msg_list[0]["type"])+"分钟到达指定时间"
                else:
                    a = "您的待办" + '\n' + self.msg_list[0]["title"] + '\n' + "已经到达设定时间"
                self.show_hight_priority_chat(a)
                self.h_ready_todo_timer.start(SEC_TO_HIDE*1000+1*1000)
                self.msg_list.pop(0)
            elif(self.h_ready_todo_timer.isActive() and len(self.msg_list)>0):
                if (self.msg_list[0]["type"] != 0):
                    a = "您的待办" + '\n' + self.msg_list[0]["title"] + '\n' + "还有" + str(self.msg_list[0]["type"]) + "分钟到达指定时间"
                else:
                    a = "您的待办" + '\n' + self.msg_list[0]["title"] + '\n' + "已经到达设定时间"
                self.show_hight_priority_chat(a)
                self.msg_list.pop(0)
            elif(len(self.msg_list)==0):
                self.h_ready_todo_timer.stop()
        except Exception as e:
            pass


    def pbMin(self):
        # self.hide()
        menu=QMenu(self)
        close_action=QAction('关闭',menu)
        close_action.triggered.connect(self.close_small_plant)
        menu.addAction(close_action)

        self.mSysTrayIcon = QSystemTrayIcon(self)
        icon = QIcon("data/ui/icon/icon.png")
        self.mSysTrayIcon.setIcon(icon)
        self.mSysTrayIcon.setToolTip("我在这里哦！")
        self.mSysTrayIcon.setContextMenu(menu)
        self.mSysTrayIcon.activated.connect(self.onActivated)
        if(self.is_in_tray is True):
            if(not self.mSysTrayIcon.isVisible()):
                self.mSysTrayIcon.show()
                self.is_in_tray=False

    def onActivated(self, reason):
        if reason == self.mSysTrayIcon.Trigger:
            self.h_mainwindow.show()
            # self.mSysTrayIcon.hide()
            self.is_in_tray=True

    def close_small_plant(self):
        self.mSysTrayIcon.hide()
        self.h_mainwindow.hide()
        self.h_mainwindow.close()
        self.close()


class DragPlant(QPushButton):

    farm_plant = None

    water_button = None
    chat_button = None

    h_width = 300
    h_height = 300

    # timer
    refresh_image_timer = None

    def __init__(self, parent,farm_plant):
        super().__init__(parent)
        self.position = [0, 0]
        self.farm_plant = farm_plant

        self.refresh_image_timer = QTimer()
        self.refresh_image_timer.timeout.connect(self.refresh_plant_image)
        self.refresh_image_timer.start(0.5*1000)

        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width,self.h_height)

    def init_button(self, water_button, chat_button):
        self.water_button = water_button
        self.chat_button = chat_button

    def mousePressEvent(self, e):
        self.position[0] = e.x()
        self.position[1] = e.y()

    def mouseMoveEvent(self, e):
        x = e.x() - self.position[0]
        y = e.y() - self.position[1]

        cor = QPoint(x, y)
        self.move(self.mapToParent(cor))

        plant_x = self.geometry().x()
        plant_y = self.geometry().y()

        # 同步移动
        self.water_button.setGeometry(plant_x + (PLANT_X - SMALL_BUTTON_X) / 2,
                                      plant_y + PLANT_Y + H_DISTANCE,
                                      SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.chat_button.setGeometry(plant_x+(PLANT_X-CHAT_BUTTON_X)/2, plant_y-CHAT_BUTTON_Y,
                                     CHAT_BUTTON_X, CHAT_BUTTON_Y)

    def refresh_plant_image(self):
        # pass
        image_path = self.farm_plant.image_path_generator()
        image_icon = QIcon(image_path)
        self.setIcon(image_icon)
        self.setIconSize(QSize(self.h_width,self.h_height))


class ChatButton(QPushButton):

    button1 = None

    def __init__(self, parent):
        super().__init__(parent)
        self.setProperty('class','chat_font')

        # self.button1 = QPushButton(self)
        # self.button1.setGeometry(CHAT_BUTTON_X/6*5, CHAT_BUTTON_Y/6*5,
        #                          CHAT_BUTTON_X/6, CHAT_BUTTON_Y/6)
        # self.button1.setObjectName("small_plant_chat_button_button1")
        #
        # self.button1.clicked.connect(self.close)

    def wake_up(self):
        self.show()
