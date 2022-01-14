# -*- coding = utf-8 -*-
# @Time : 2021/4/5 15:07
# @Author : MiHao
# @File : edit_window.py
# @Software: PyCharm
import json
import os
from copy import deepcopy

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox, QCheckBox, QListWidget, \
    QListWidgetItem, QInputDialog, QFrame
from PyQt5.QtCore import Qt, QDate, QTime

from gui.shadow import get_shadow_effect
from habit.habit_bar import HabitBar

# 增加连击数按钮(小按钮)
SMALL_BUTTON_X = 40
SMALL_BUTTON_Y = 40
# 取消，保存按钮大小（中按钮）
MIDDLE_BUTTON_X = 50
MIDDLE_BUTTON_Y = 30
# 删除按钮大小（大按钮）
LARGE_BUTTON_X = 120
LARGE_BUTTON_Y = 35
# 周几按钮
WEEK_BUTTON_X = 40
WEEK_BUTTON_Y = 40
# 设置提醒时间按钮
TIME_BUTTON_X = 60
TIME_BUTTON_Y = 60
TIME_INPUT_X = 70
TIME_INPUT_Y = 50
DATE_INPUT_X = 50
DATE_INPUT_Y = 50
MID_LABEL_X = 30
MID_LABEL_Y = 50

# 文本大小
TEXT_X = 200
TEXT_Y = 50
TEXT2_X=170
# 输入框大小
INPUT_X = 400
INPUT_Y = 40
# 水平间距
H_DISTANCE = 20
H_DISTANCE2 = 30
H_DISTANCE3 = 15
H_DISTANCE4 = 5
# 垂直间距
V_DISTANCE = 20
V_DISTANCE2 = 40
V_DISTANCE3 = 30
# 上边距
UP_DISTANCE = 20
# 下边距
DOWN_DISTANCE = 80
# 左边距
LEFT_DISTANCE = 50
# 右边距
RIGHT_DISTANCE = 20
# 水平控件数量
H_NUM = 1
# 垂直控件数量
V_NUM = 6
# 窗口大小
WINDOW_WIDTH = RIGHT_DISTANCE + LEFT_DISTANCE + TEXT_X
WINDOW_HIGH = UP_DISTANCE + DOWN_DISTANCE + (V_NUM - 1) * V_DISTANCE + (
            TEXT_Y + INPUT_Y) * 4 + MIDDLE_BUTTON_Y + LARGE_BUTTON_Y
#
SHADOW_WIDTH = 40

# 习惯打卡
class EditWindow(QFrame):

    habit_bar = None
    window_width = None
    window_high = None
    # 水平控件数量
    h_num = None
    # 垂直控件数量
    v_num = None

    background_label = None

    style_path = 'gui/habit_edit_window.qss'

    def __init__(self):
        super().__init__()
        self.h_num = 1
        self.v_num = 6
        # 设置窗口
        self.window_high = UP_DISTANCE + SMALL_BUTTON_Y/2 + TEXT_Y * 3 + INPUT_Y * 2 + V_DISTANCE * 3 + V_DISTANCE2 * 2 + DOWN_DISTANCE
        self.window_width = RIGHT_DISTANCE + LEFT_DISTANCE + H_DISTANCE2 * 6 + SMALL_BUTTON_X * 7 + SMALL_BUTTON_Y + H_DISTANCE
        self.setFixedSize(self.window_width, self.window_high)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.window_width, self.window_high)
        self.background_label.setObjectName("edit_habit_window_background")

        # 数据存储：标题，内容，标签，次数
        self.title = QLabel()
        self.content = QLabel()
        self.tag = QLabel()
        self.tags = ["生活", "工作", "学习", "锻炼身体"]
        self.times = QLabel()
        self.week = {}

        # UI：标题，内容，标签，次数,天数
        self.title_label = QLabel("标题", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.content_label = QLabel("一句鼓励的话", self)
        self.content_label.setAlignment(Qt.AlignCenter)
        # self.tag_box = QLabel("标签", self)
        # self.times_label = QLabel("连击次数", self)
        self.week_select = QLabel("设置星期", self)
        self.week_select.setAlignment(Qt.AlignCenter)

        # self.tag_box.setObjectName("edit_habit_window_tag_box")
        # self.times_label.setObjectName("edit_habit_window_time_label")

        # 编辑框：标题，内容，标签，次数
        self.title_line_edit = QLineEdit(self)
        self.content_line_edit = QLineEdit(self)
        # self.tag_combo_box = ComboCheckBox(self, self.tags)
        # self.times_line_edit = QLineEdit(self)
        # self.times_line_edit.setText("1")


        # self.tag_combo_box.setObjectName("edit_habit_window_tag_combo_box")
        # self.times_line_edit.setObjectName("edit_habit_window_times_line_edit")

        # 保存，取消，删除按钮
        self.save_button = QPushButton(self)
        self.cancel_button = QPushButton(self)
        self.delete_button = QPushButton(self)

        # 星期选择
        self.week_select_button = CheckWeek(self)
        self.week_select_button.setParent(self)
        # self.week = self.week_select_button.week

        # 加减次数按钮
        # self.add_times_button = QPushButton("+", self)
        # self.cut_times_button = QPushButton("-", self)

        # self.add_times_button.setObjectName("edit_habit_window_add_times_button")
        # self.cut_times_button.setObjectName("edit_habit_window_cut_times_button")

        # 加减标签按钮
        # self.add_tag_button = QPushButton("+", self)
        # self.cut_tag_button = QPushButton("-", self)

        self.init_ui()

    # 编辑页面设计
    def init_ui(self):

        # 控件放置
        self.cancel_button.setGeometry(self.window_width - RIGHT_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                    SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.cancel_button.setGraphicsEffect(get_shadow_effect(self))
        self.delete_button.setGeometry(self.cancel_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                    SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.delete_button.setGraphicsEffect(get_shadow_effect(self))
        self.save_button.setGeometry(self.delete_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                     SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.save_button.setGraphicsEffect(get_shadow_effect(self))

        self.title_label.setGeometry(LEFT_DISTANCE, UP_DISTANCE + SMALL_BUTTON_Y/2,
                                     TEXT_X/2, TEXT_Y)
        self.title_label.setGraphicsEffect(get_shadow_effect(self))
        self.title_line_edit.setGeometry(LEFT_DISTANCE, self.title_label.geometry().y() + TEXT_Y + V_DISTANCE,
                                         INPUT_X, INPUT_Y)
        self.title_line_edit.setGraphicsEffect(get_shadow_effect(self))
        self.content_label.setGeometry(LEFT_DISTANCE, self.title_line_edit.geometry().y() + + INPUT_Y + V_DISTANCE2,
                                       TEXT_X, TEXT_Y)
        self.content_label.setGraphicsEffect(get_shadow_effect(self))
        self.content_line_edit.setGeometry(LEFT_DISTANCE, self.content_label.geometry().y() + TEXT_Y + V_DISTANCE,
                                           INPUT_X, INPUT_Y)
        self.content_line_edit.setGraphicsEffect(get_shadow_effect(self))
        # self.tag_box.setGeometry(LEFT_DISTANCE, self.content_line_edit.geometry().y() + V_DISTANCE + INPUT_Y,
        #                          TEXT_X, TEXT_Y)
        # self.cut_tag_button.setGeometry(LEFT_DISTANCE, self.tag_box.geometry().y() + INPUT_Y,
        #                             SMALL_BUTTON_X, SMALL_BUTTON_Y)
        # self.tag_combo_box.setGeometry(LEFT_DISTANCE, self.tag_box.geometry().y() + INPUT_Y,
        #                                INPUT_X, INPUT_Y)
        # self.add_tag_button.setGeometry(WINDOW_WIDTH - RIGHT_DISTANCE - SMALL_BUTTON_X,
        #                                 self.tag_combo_box.geometry().y(),
        #                                 SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.week_select.setGeometry(LEFT_DISTANCE, self.content_line_edit.geometry().y() + V_DISTANCE2 + INPUT_Y,
                                 TEXT2_X, TEXT_Y)
        self.week_select.setGraphicsEffect(get_shadow_effect(self))
        self.week_select_button.setGeometry(LEFT_DISTANCE, self.week_select.geometry().y() + INPUT_Y + V_DISTANCE,
                                       WEEK_BUTTON_X*7+H_DISTANCE2*6, WEEK_BUTTON_Y)
        self.week_select_button.setGraphicsEffect(get_shadow_effect(self))
        # self.times_label.setGeometry(LEFT_DISTANCE, self.week_select_button.geometry().y() + V_DISTANCE + WEEK_BUTTON_Y,
        #                             TEXT_X, TEXT_Y)
        # self.cut_times_button.setGeometry(LEFT_DISTANCE, self.times_label.geometry().y() + INPUT_Y,
        #                                   SMALL_BUTTON_X, SMALL_BUTTON_Y)
        # self.times_line_edit.setGeometry(self.cut_times_button.geometry().x() + SMALL_BUTTON_X,
        #                                  self.cut_times_button.geometry().y(),
        #                                  INPUT_X - SMALL_BUTTON_X*2, INPUT_Y)
        # self.add_times_button.setGeometry(self.window_width - RIGHT_DISTANCE - SMALL_BUTTON_X,
        #                                  self.times_line_edit.geometry().y(),
        #                                  SMALL_BUTTON_X, SMALL_BUTTON_Y)


        # 编辑框内容修改发出信号
        self.title_line_edit.textChanged[str].connect(self.title_change)
        self.content_line_edit.textChanged[str].connect(self.content_change)
        # self.tag_combo_box.line_edit.textChanged[str].connect(self.tag_change)
        # self.times_line_edit.textChanged[str].connect(self.times_change)

        # 按钮点击发出信号
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        # 需要HabitBar删除bool参数
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.clicked.connect(self.close)
        # self.add_times_button.clicked.connect(self.times_change_add)
        # self.cut_times_button.clicked.connect(self.time_change_cut)
        # self.add_tag_button.clicked.connect(self.tag_change_add)
        # self.cut_tag_button.clicked.connect(self.tag_change_cut)

        # qss
        # self.setObjectName("edit_habit_window_background")
        self.title_label.setProperty("class", "title_two")
        self.content_label.setProperty("class", "title_two")
        self.week_select.setProperty("class", "title_two")
        self.title_label.setObjectName("edit_habit_window_title_label_S")
        self.content_label.setObjectName("edit_habit_window_title_label_L")
        self.week_select.setObjectName("edit_habit_window_title_label_M")

        self.title_line_edit.setProperty("class", "description_two")
        self.content_line_edit.setProperty("class", "description_two")
        self.title_line_edit.setObjectName("edit_habit_window_line_edit")
        self.content_line_edit.setObjectName("edit_habit_window_line_edit")

        self.save_button.setProperty("class", "edit_window_save_button")
        self.cancel_button.setProperty("class", "edit_window_cancel_button")
        self.delete_button.setProperty("class", "edit_window_delete_button")

        self.week_select_button.mon_button.setObjectName("edit_window_mon_button")
        self.week_select_button.tue_button.setObjectName("edit_window_tue_button")
        self.week_select_button.wen_button.setObjectName("edit_window_wen_button")
        self.week_select_button.thur_button.setObjectName("edit_window_thur_button")
        self.week_select_button.fri_button.setObjectName("edit_window_fri_button")
        self.week_select_button.sat_button.setObjectName("edit_window_sat_button")
        self.week_select_button.sun_button.setObjectName("edit_window_sun_button")

        # self.show()

        # 设定qss
        self.set_style(self.style_path)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    # 标题，内容，标签，次数编辑框更改信号槽
    def title_change(self, text):
        self.title.setText(text)

    def content_change(self, text):
        self.content.setText(text)

    # def tag_change(self, text):
    #     self.tag.setText(text)

    # def tag_change_add(self):
    #     text, ok = QInputDialog.getText(self, "添加新标签", "输入标签")
    #     if ok:
    #         self.tag_combo_box.add_check_box2(text)

    # def tag_change_cut(self):

    # def times_change(self, text):
    #     self.times.setText(text)
    #
    # def times_change_add(self):
    #     text = int(self.times_line_edit.text())
    #     self.times_line_edit.setText(str(text + 1))
    #
    # def time_change_cut(self):
    #     text = int(self.times_line_edit.text())
    #     if text >= 2:
    #         self.times_line_edit.setText(str(text - 1))

    def wake_up(self, habit_bar):
        self.habit_bar = habit_bar
        self.title_line_edit.clear()
        self.content_line_edit.clear()
        # self.tag_combo_box.clear()
        # self.tag_combo_box.line_edit.clear()
        # self.tag_combo_box.reset()
        # self.times_line_edit.clear()
        # self.week_select_button.status_clear()

        self.init_buttons()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def init_buttons(self):

        self.title_line_edit.setText(self.habit_bar.h_title)
        self.content_line_edit.setText(self.habit_bar.h_content)
        # self.tag_combo_box.line_edit.setText(self.habit_bar.h_tag)
        # if self.habit_bar.h_times is None:
        #     self.times_line_edit.setText("1")
        # else:
        #     self.times_line_edit.setText(self.habit_bar.h_times)
        # self.week_select_button.week = deepcopy(self.habit_bar.h_week)
        self.week_select_button.week=self.habit_bar.h_week
        self.week_select_button.update_status(self.habit_bar.h_week)


    # 保存按钮信号槽
    def save(self):
        self.habit_bar.h_title = self.title.text()
        self.habit_bar.h_content = self.content.text()
        # self.habit_bar.h_tag = self.tag.text()
        # self.habit_bar.h_times = self.times.text()

        # path = "data/habit/" + "week.json"
        # with open(path, "r") as f:
        #     self.week = json.load(f)

        self.habit_bar.h_week = deepcopy(self.week_select_button.week)
        self.close()

    def delete(self):
        self.habit_bar.h_is_delete=True


#
class EditCheckButton(QPushButton):

    check_status = False

    image_label = None

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.show()

        # 初始化控件
        self.image_label = QLabel(self)

        # self.clicked.connect(self.refresh_check_status)
        self.init_ui()

    def init_ui(self):
        self.image_label.setObjectName('habit_edit_window_selected')
        self.image_label.resize(40,40)
        self.image_label.hide()

    def set_check_status(self, status):
        self.check_status = status
        if self.check_status is True:
            self.image_label.show()
        else:
            self.image_label.hide()

    def refresh_check_status(self):
        if self.check_status is True:
            self.check_status = False
            self.image_label.hide()
        else:
            self.check_status = True
            self.image_label.show()


#
class CheckWeek(QFrame):

    mon_button = None
    tue_button = None
    wen_button = None
    thur_button = None
    fri_button = None
    sat_button = None
    sun_button = None

    week = {"Mon": False,
                 "Tue": False,
                 "Wen": False,
                 "Thur": False,
                 "Fri": False,
                 "Sat": False,
                 "Sun": False}

    def __init__(self, parent):
        super().__init__(parent)

        # 隐藏标题栏
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.mon_button = EditCheckButton(self)
        self.tue_button = EditCheckButton(self)
        self.wen_button = EditCheckButton(self)
        self.thur_button = EditCheckButton(self)
        self.fri_button = EditCheckButton(self)
        self.sat_button = EditCheckButton(self)
        self.sun_button = EditCheckButton(self)

        self.mon_button.setGeometry(0, 0, WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.tue_button.setGeometry(self.mon_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.mon_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.wen_button.setGeometry(self.tue_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.tue_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.thur_button.setGeometry(self.wen_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.wen_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.fri_button.setGeometry(self.thur_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.thur_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.sat_button.setGeometry(self.fri_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.fri_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)
        self.sun_button.setGeometry(self.sat_button.geometry().x() + WEEK_BUTTON_X+H_DISTANCE2, self.sat_button.geometry().y(),
                                    WEEK_BUTTON_X, WEEK_BUTTON_Y)

        # self.mon_status = self.mon_button.check_status
        # self.tue_status = self.tue_button.check_status
        # self.wen_status = self.wen_button.check_status
        # self.thur_status = self.thur_button.check_status
        # self.fri_status = self.fri_button.check_status
        # self.sat_status = self.sat_button.check_status
        # self.sun_status = self.sun_button.check_status

        self.mon_button.clicked.connect(self.mon_status_change)
        self.tue_button.clicked.connect(self.tue_status_change)
        self.wen_button.clicked.connect(self.wen_status_change)
        self.thur_button.clicked.connect(self.thur_status_change)
        self.fri_button.clicked.connect(self.fri_status_change)
        self.sat_button.clicked.connect(self.sat_status_change)
        self.sun_button.clicked.connect(self.sun_status_change)

    def status_clear(self):
        self.week = {"Mon": False,
                "Tue": False,
                "Wen": False,
                "Thur": False,
                "Fri": False,
                "Sat": False,
                "Sun": False}

    def update_status(self,week_list):
        self.mon_button.set_check_status(week_list['Mon'])
        self.tue_button.set_check_status(week_list["Tue"])
        self.thur_button.set_check_status(week_list["Thur"])
        self.wen_button.set_check_status(week_list["Wen"])
        self.fri_button.set_check_status(week_list["Fri"])
        self.sat_button.set_check_status(week_list["Sat"])
        self.sun_button.set_check_status(week_list["Sun"])

    def save_to_local(self):
        path = "data/habit/" + "week.json"
        with open(path, "w") as f:
            json.dump(self.week, f)

    def mon_status_change(self):
        # if self.mon_button.check_status is True:
        #     self.mon_button.check_status = False
        #     # print(self.mon_button.check_status)
        #     self.week["Mon"] = False
        #     print(self.week["Mon"])
        # else:
        #     self.mon_button.check_status = True
        #     # print(self.mon_button.check_status)
        #     self.week["Mon"] = True
        #     print(self.week["Mon"])
        # self.save_to_local()
        self.mon_button.refresh_check_status()
        if self.mon_button.check_status is True:
            self.week["Mon"] = True
        else:
            self.week["Mon"] = False

    def tue_status_change(self):
        # if self.tue_button.check_status is True:
        #     self.tue_button.check_status = False
        #     self.week["Tue"] = False
        # else:
        #     self.tue_button.check_status = True
        #     self.week["Tue"] = True
        # self.save_to_local()
        self.tue_button.refresh_check_status()
        if self.tue_button.check_status is True:
            self.week["Tue"] = True
        else:
            self.week["Tue"] = False

    def wen_status_change(self):
        # if self.wen_button.check_status is True:
        #     self.wen_button.check_status = False
        #     self.week["Wen"] = False
        # else:
        #     self.wen_button.check_status = True
        #     self.week["Wen"] = True
        # self.save_to_local()
        self.wen_button.refresh_check_status()
        if self.wen_button.check_status is True:
            self.week["Wen"] = True
        else:
            self.week["Wen"] = False

    def thur_status_change(self):
        # if self.thur_button.check_status is True:
        #     self.thur_button.check_status = False
        #     self.week["thur"] = False
        # else:
        #     self.thur_button.check_status = True
        #     self.week["thur"] = True
        # self.save_to_local()
        self.thur_button.refresh_check_status()
        if self.thur_button.check_status is True:
            self.week["Thur"] = True
        else:
            self.week["Thur"] = False

    def fri_status_change(self):
        # if self.fri_button.check_status is True:
        #     self.fri_button.check_status = False
        #     self.week["Fri"] = False
        # else:
        #     self.fri_button.check_status = True
        #     self.week["Fri"] = True
        # self.save_to_local()
        self.fri_button.refresh_check_status()
        if self.fri_button.check_status is True:
            self.week["Fri"] = True
        else:
            self.week["Fri"] = False

    def sat_status_change(self):
        # if self.sat_button.check_status is True:
        #     self.sat_button.check_status = False
        #     self.week["Sat"] = False
        # else:
        #     self.fri_button.check_status = True
        #     self.week["Sat"] = True
        # self.save_to_local()
        self.sat_button.refresh_check_status()
        if self.sat_button.check_status is True:
            self.week["Sat"] = True
        else:
            self.week["Sat"] = False

    def sun_status_change(self):
        # if self.sun_button.check_status is True:
        #     self.sun_button.check_status = False
        #     self.week["Sun"] = False
        # else:
        #     self.sun_button.check_status = True
        #     self.week["Sun"] = True
        # self.save_to_local()
        self.sun_button.refresh_check_status()
        if self.sun_button.check_status is True:
            self.week["Sun"] = True
        else:
            self.week["Sun"] = False



# 下拉复选框类
class ComboCheckBox(QComboBox):

    # items 复选框里的初始内容
    def __init__(self, parent, items):
        super(ComboCheckBox, self).__init__(parent)
        self.items = items
        self.row_num = len(self.items)
        self.selected_num = 0
        self.check_box = []

        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)
        self.list_widget = QListWidget()

        self.tag_edit_line = QLineEdit("添加新标签，按enter确认")
        self.check_box.append(self.tag_edit_line)
        item = QListWidgetItem(self.list_widget)
        self.list_widget.setItemWidget(item, self.check_box[0])

        self.tag_edit_line.selectionChanged.connect(self.tag_edit_line.clear)
        self.tag_edit_line.returnPressed.connect(self.add_tag)

        for i in range(0, self.row_num):
            self.add_check_box(i+1)
        for i in range(0, self.row_num):
            self.check_box[i+1].stateChanged.connect(self.show)

        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)
        self.setLineEdit(self.line_edit)

    # 增加复选框内容
    def add_check_box(self, i):
        self.check_box.append(QCheckBox())
        item = QListWidgetItem(self.list_widget)
        self.check_box[i].setText(self.items[i-1])
        self.list_widget.setItemWidget(item, self.check_box[i])
        self.check_box[i].stateChanged.connect(self.show)
        self.tag_edit_line.setText("添加新标签，按enter确认")

    def add_tag(self):
        self.items.append(self.tag_edit_line.text())
        self.row_num = len(self.items)
        self.add_check_box(self.row_num)
        self.check_box[self.row_num-1].stateChanged.connect(self.show)

    # 将勾选内容展示在文本框
    def show(self):
        show = ''
        select_list = self.selected_list()
        self.line_edit.setReadOnly(False)
        self.line_edit.clear()
        for i in select_list:
            show += i + ';'
        self.line_edit.setText(show)
        self.line_edit.setReadOnly(True)

    # 返回复选框选中的内容
    def selected_list(self):
        text_list = []
        for i in range(1, self.row_num+1):
            if self.check_box[i].isChecked():
                text_list.append(self.check_box[i].text())
        self.selected_num = len(text_list)
        return text_list

    # 将所有复选框置为无勾选状态
    def clear(self):
        for i in range(1, self.row_num+1):
            # self.check_box[i].setChecked(False)
            self.check_box[i].setCheckState(Qt.Unchecked)

    def reset(self):
        self.clear()
        self.show()


# 代办日程
class ToDoEditWindow(QFrame):
    window_width = None
    window_high = None
    h_num = None
    v_num = None

    select_datetime = None
    to_do_bar = None

    background_label = None

    style_path = 'gui/to_do_edit_window.qss'

    def __init__(self):
        super().__init__()
        self.h_num = 1
        self.v_num = 4
        self.background_label = QLabel(self)

        self.select_datetime = SelectDateTimeBox(wight=200, high=160, is_hint=False)
        # self.select_dtime.setParent(self)

        # 数据存储：标题
        self.title = QLabel()

        # UI：标题
        self.title_label = QLabel("标题", self)
        self.title_label.setAlignment(Qt.AlignCenter)

        # 编辑框：标题
        self.title_line_edit = QLineEdit(self)

        # 保存，取消，设置时间按钮
        self.save_button = QPushButton(self)
        self.cancel_button = QPushButton(self)
        self.time_button = QPushButton(self)
        self.delete_button = QPushButton(self)

        # 设置时间提醒窗口
        self.time_up = False
        self.select_datetime.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # 设置窗口
        self.window_high = UP_DISTANCE + SMALL_BUTTON_Y / 2 + TEXT_Y + INPUT_Y + V_DISTANCE * 2 + TIME_BUTTON_Y + UP_DISTANCE

        self.window_width = RIGHT_DISTANCE + LEFT_DISTANCE + INPUT_X + SMALL_BUTTON_X
        self.setFixedSize(self.window_width, self.window_high)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)


        self.background_label.setGeometry(0, 0, self.window_width, self.window_high)
        self.background_label.setObjectName("edit_todo_window_background")

        self.init_ui()

    def init_ui(self):

        # 控件放置
        self.cancel_button.setGeometry(self.window_width - RIGHT_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                       SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.cancel_button.setGraphicsEffect(get_shadow_effect(self))
        self.delete_button.setGeometry(self.cancel_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                       SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.delete_button.setGraphicsEffect(get_shadow_effect(self))
        self.save_button.setGeometry(self.delete_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                     SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.save_button.setGraphicsEffect(get_shadow_effect(self))
        self.title_label.setGeometry(LEFT_DISTANCE, UP_DISTANCE + SMALL_BUTTON_Y / 2,
                                     TEXT_X / 2, TEXT_Y)
        self.title_label.setGraphicsEffect(get_shadow_effect(self))
        self.title_line_edit.setGeometry(LEFT_DISTANCE, self.title_label.geometry().y() + TEXT_Y + V_DISTANCE,
                                         INPUT_X, INPUT_Y)
        self.title_line_edit.setGraphicsEffect(get_shadow_effect(self))
        self.time_button.setGeometry(LEFT_DISTANCE, self.title_line_edit.geometry().y()+V_DISTANCE + INPUT_Y,
                                     TIME_BUTTON_X, TIME_BUTTON_Y)
        self.time_button.setGraphicsEffect(get_shadow_effect(self))

        # 编辑框内容修改发出信号
        self.title_line_edit.textChanged[str].connect(self.title_change)

        # 按钮点击发出信号
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        self.time_button.clicked.connect(self.wake_up_time)
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.clicked.connect(self.close)

        # 设置qss
        self.setObjectName("edit_todo_window_background")
        self.title_label.setProperty("class", "title_two")
        self.title_line_edit.setProperty("class", "description_two")
        self.title_label.setObjectName("edit_todo_window_label")
        self.title_line_edit.setObjectName("edit_todo_window_line_edit")

        self.save_button.setProperty("class", "edit_window_save_button")
        self.cancel_button.setProperty("class", "edit_window_cancel_button")
        self.delete_button.setProperty("class", "edit_window_delete_button")
        self.time_button.setProperty("class", "edit_window_time_button")

        # self.show()

        # 设定qss
        self.set_style(self.style_path)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    # 标题编辑框更改信号槽
    def title_change(self, text):
        self.title.setText(text)

    def wake_up(self, button):
        self.to_do_bar = button
        self.title_line_edit.clear()

        self.init_buttons()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def init_buttons(self):
        self.title_line_edit.setText(self.to_do_bar.h_title)

        year = self.to_do_bar.h_year
        month = self.to_do_bar.h_month
        day = self.to_do_bar.h_day
        hour = self.to_do_bar.h_hour
        minute = self.to_do_bar.h_minute
        if year is None:
            self.select_datetime.date_box.reset()
            self.select_datetime.time_box.set_time(0, 0)
        else:
            self.select_datetime.date_box.set_date(year=year, month=month, day=day)
            self.select_datetime.time_box.set_time(hour=hour, minute=minute)

    def save(self):
        self.to_do_bar.h_title = self.title.text()
        self.to_do_bar.h_year = self.select_datetime.date_box.year_box.value_line_edit.text()
        self.to_do_bar.h_month = self.select_datetime.date_box.month_box.value_line_edit.text()
        self.to_do_bar.h_day = self.select_datetime.date_box.day_box.value_line_edit.text()
        self.to_do_bar.h_hour = self.select_datetime.time_box.hour_box.value_line_edit.text()
        self.to_do_bar.h_minute = self.select_datetime.time_box.minute_box.value_line_edit.text()
        self.close()

    def delete(self):
        self.to_do_bar.h_is_delete = True

    def wake_up_time(self):
        self.select_datetime.wake_up()
        # self.setWindowFlags(Qt.Widget)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)


# 我的一天
class MyDayEditWindow(QFrame):
    window_width = None
    window_high = None
    h_num = None
    v_num = None
    select_time = None
    my_day_bar = None

    background_label = None

    style_path = 'gui/my_day_edit_window.qss'

    def __init__(self):
        super().__init__()
        self.h_num = 1
        self.v_num = 6

        self.background_label = QLabel(self)

        # 数据存储：标题
        self.title = QLabel()

        # UI：标题
        self.title_label = QLabel("标题", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.time_label = QLabel("设置时间", self)
        self.time_label.setAlignment(Qt.AlignCenter)

        # 编辑框：标题
        self.title_line_edit = QLineEdit(self)

        # 保存，取消，删除按钮
        self.save_button = QPushButton(self)
        self.save_button.setGraphicsEffect(get_shadow_effect(self))
        self.cancel_button = QPushButton(self)
        self.cancel_button.setGraphicsEffect(get_shadow_effect(self))
        self.delete_button = QPushButton(self)
        self.delete_button.setGraphicsEffect(get_shadow_effect(self))

        self.select_time = SelectTimeBox()
        self.select_time.setParent(self)

        # 设置窗口
        self.window_high = UP_DISTANCE + SMALL_BUTTON_Y / 2 + TEXT_Y * 2 + INPUT_Y + V_DISTANCE + V_DISTANCE2\
                           + self.select_time.high + DOWN_DISTANCE - SHADOW_WIDTH

        self.window_width = RIGHT_DISTANCE + LEFT_DISTANCE + INPUT_X + SMALL_BUTTON_X
        self.setFixedSize(self.window_width, self.window_high)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)


        self.background_label.setGeometry(0, 0, self.window_width, self.window_high)
        self.background_label.setObjectName("edit_myday_window_background")

        self.init_ui()

    def init_ui(self):
        # 控件放置
        self.cancel_button.setGeometry(self.window_width - RIGHT_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                    SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.delete_button.setGeometry(self.cancel_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                    SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.save_button.setGeometry(self.delete_button.geometry().x() - H_DISTANCE - SMALL_BUTTON_X, UP_DISTANCE,
                                     SMALL_BUTTON_X, SMALL_BUTTON_Y)

        self.title_label.setGeometry(LEFT_DISTANCE, UP_DISTANCE + SMALL_BUTTON_Y/2,
                                     TEXT_X/2, TEXT_Y)
        self.title_label.setGraphicsEffect(get_shadow_effect(self))
        self.title_line_edit.setGeometry(LEFT_DISTANCE, self.title_label.geometry().y() + TEXT_Y + V_DISTANCE,
                                         INPUT_X, INPUT_Y)
        self.title_line_edit.setGraphicsEffect(get_shadow_effect(self))
        self.time_label.setGeometry(LEFT_DISTANCE, self.title_line_edit.geometry().y() + + INPUT_Y + V_DISTANCE2,
                                       TEXT_X, TEXT_Y)
        self.time_label.setGraphicsEffect(get_shadow_effect(self))
        self.select_time.move(LEFT_DISTANCE, self.time_label.geometry().y()+TEXT_Y+V_DISTANCE)
        self.select_time.wake_up()

        # 编辑框内容修改发出信号
        self.title_line_edit.textChanged[str].connect(self.title_change)

        # 按钮点击发出信号
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.clicked.connect(self.close)

        # qss
        self.setObjectName("edit_myday_window_background")
        self.title_label.setProperty("class", "title_two")
        self.time_label.setProperty("class", "title_two")
        self.title_label.setObjectName("edit_myday_window_title_label_S")
        self.time_label.setObjectName("edit_myday_window_title_label_L")

        self.title_line_edit.setObjectName("edit_myday_window_line_edit")
        self.title_line_edit.setProperty("class", "description_two")

        self.save_button.setProperty("class", "edit_window_save_button")
        self.cancel_button.setProperty("class", "edit_window_cancel_button")
        self.delete_button.setProperty("class", "edit_window_delete_button")

        self.select_time.hour_box.add_button.setProperty("class", "edit_myday_window_time_add_button")
        self.select_time.minute_box.add_button.setProperty("class", "edit_myday_window_time_add_button")
        self.select_time.hour_box.add_button.setGraphicsEffect(get_shadow_effect(self))
        self.select_time.minute_box.add_button.setGraphicsEffect(get_shadow_effect(self))

        self.select_time.hour_box.cut_button.setProperty("class", "edit_myday_window_time_cut_button")
        self.select_time.minute_box.cut_button.setProperty("class", "edit_myday_window_time_cut_button")
        self.select_time.hour_box.cut_button.setGraphicsEffect(get_shadow_effect(self))
        self.select_time.minute_box.cut_button.setGraphicsEffect(get_shadow_effect(self))

        self.select_time.hour_box.value_line_edit.setProperty("class", "date_two")
        self.select_time.minute_box.value_line_edit.setProperty("class", "date_two")
        self.select_time.hour_box.value_line_edit.setGraphicsEffect(get_shadow_effect(self))
        self.select_time.minute_box.value_line_edit.setGraphicsEffect(get_shadow_effect(self))

        self.select_time.hour_box.value_line_edit.setObjectName("edit_myday_window_time_value_line_edit")
        self.select_time.minute_box.value_line_edit.setObjectName("edit_myday_window_time_value_line_edit")

        self.select_time.mid_label.setProperty("class", "edit_myday_window_time_mid_button")

        # self.show()

        # 设定qss
        self.set_style(self.style_path)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    # 标题编辑框更改信号槽
    def title_change(self, text):
        self.title.setText(text)

    def wake_up(self, button):
        self.my_day_bar = button
        self.title_line_edit.clear()

        self.init_buttons()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def init_buttons(self):

        self.title_line_edit.setText(self.my_day_bar.h_title)

        hour = self.my_day_bar.h_hour
        minute = self.my_day_bar.h_minute

        if hour is None:
            self.select_time.reset()
        else:
            self.select_time.set_time(hour=hour, minute=minute)

    def delete(self):
        self.my_day_bar.h_is_delete = True

    def save(self):
        self.my_day_bar.h_title = self.title.text()
        self.my_day_bar.h_hour = self.select_time.hour_box.value_line_edit.text()
        self.my_day_bar.h_minute = self.select_time.minute_box.value_line_edit.text()
        self.close()


# 双侧增减按钮选择框
class SelectBox(QFrame):

    # 窗口控件大小
    wight = None
    high = None

    # 按钮控件
    add_button = None
    cut_button = None
    button_wight = 80
    button_high = 50

    # 文本框控件
    value = None
    value_line_edit = None
    line_edit_width = 80
    line_edit_high = 50

    # 范围
    min_value = None
    max_value = None

    # 按钮水平or垂直布局, 默认为垂直
    vertical = None

    def __init__(self, vertical=True, weight=100, high=100):
        super().__init__()

        # 隐藏标题栏
        self.setWindowFlag(Qt.FramelessWindowHint)

        weight = TIME_INPUT_X + SHADOW_WIDTH
        high = SMALL_BUTTON_Y * 2 + TIME_INPUT_Y + V_DISTANCE3*2 + SHADOW_WIDTH
        self.setsize(weight, high)

        self.add_button = QPushButton(self)
        self.cut_button = QPushButton(self)
        self.add_button.setProperty("class", "selectbox_add_button")
        self.add_button.setGraphicsEffect(get_shadow_effect(self))

        self.cut_button.setProperty("class", "selectbox_cut_button")
        self.cut_button.setGraphicsEffect(get_shadow_effect(self))

        self.value = QLabel()
        self.value_line_edit = QLineEdit(self)
        self.value_line_edit.setAlignment(Qt.AlignCenter)
        self.value_line_edit.setObjectName("selectbox_value_line_edit")

        self.vertical = vertical

        # self.value_line_edit.setText("8")

        # self.set_range(5, 10)

        self.init_ui()
        self.show()

    def init_ui(self):
        if self.vertical is True:

            self.add_button.setGeometry((self.width()-SMALL_BUTTON_X)/2, 0, SMALL_BUTTON_X, SMALL_BUTTON_Y)
            self.value_line_edit.setGeometry((self.width()-TIME_INPUT_X)/2, self.add_button.geometry().y()+SMALL_BUTTON_Y+V_DISTANCE3,
                                             TIME_INPUT_X, TIME_INPUT_Y)
            self.cut_button.setGeometry((self.width()-SMALL_BUTTON_X)/2, self.value_line_edit.geometry().y()+TIME_INPUT_Y+V_DISTANCE3,
                                        SMALL_BUTTON_X, SMALL_BUTTON_Y)

            self.add_button.clicked.connect(self.add_value)
            self.cut_button.clicked.connect(self.cut_value)
            self.value_line_edit.textChanged[str].connect(self.value_change)

    def resize_value_edit(self, v_width, v_high):

        weight = v_width +SHADOW_WIDTH
        high = SMALL_BUTTON_Y * 2 + v_high + V_DISTANCE3 * 2 +SHADOW_WIDTH
        self.wight = weight
        self.high = high
        self.setFixedSize(self.wight, self.high)

        self.add_button.setGeometry((self.width() - SMALL_BUTTON_X) / 2, 0, SMALL_BUTTON_X, SMALL_BUTTON_Y)
        self.value_line_edit.setGeometry((self.width() - v_width) / 2,
                                         self.add_button.geometry().y() + SMALL_BUTTON_Y + V_DISTANCE3,
                                         v_width, v_high)
        self.cut_button.setGeometry((self.width() - SMALL_BUTTON_X) / 2,
                                    self.value_line_edit.geometry().y() + TIME_INPUT_Y + V_DISTANCE3,
                                    SMALL_BUTTON_X, SMALL_BUTTON_Y)

    def setsize(self, wight, high):
        self.wight = wight
        self.high = high
        self.setFixedSize(self.wight, self.high)

    def add_value(self):
        if not self.value_line_edit.text() == '':
            value = int(self.value_line_edit.text())
        else:
            value = int(self.min_value)
        if value < self.max_value:
            self.value_line_edit.setText(str(value + 1).zfill(2))
        elif value == self.max_value:
            self.value_line_edit.setText(str(self.min_value).zfill(2))

    def cut_value(self):
        if not self.value_line_edit.text() == '':
            value = int(self.value_line_edit.text())
        else:
            value = int(self.max_value)
        if value > self.min_value:
            self.value_line_edit.setText(str(value - 1).zfill(2))
        elif value == self.min_value:
            self.value_line_edit.setText(str(self.max_value).zfill(2))
        value = int(self.value_line_edit.text())

    def value_change(self, text):
        if text == '':
            self.value_line_edit.clear()
            return
        else:
            num = int(text)
        if num <= self.min_value:
            self.value_line_edit.setText(str(self.min_value).zfill(2))
        elif num <= self.max_value and num > self.min_value:
            self.value_line_edit.setText(str(num).zfill(2))
            self.value.setText(str(num).zfill(2))
        else:
            self.reset_value()

    def set_range(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.value_line_edit.setValidator(QIntValidator(min_value, max_value))

    def reset_value(self):
        self.value_line_edit.setText(str(self.max_value))

    def check_range(self, text):
        num = int(text)
        if num > self.max_value:
            self.reset_value()

    # def set_button_size(self, wight, high):
    #     self.button_high = high
    #     self.button_high = wight
    #     self.add_button.resize(self.button_wight, self.button_high)
    #     self.cut_button.resize(self.button_wight, self.button_high)
    #
    # def set_line_edit_size(self, wight, high):
    #     self.line_edit_width = wight
    #     self.line_edit_high = high
    #     self.value_line_edit.resize(self.line_edit_width, self.line_edit_high)


class SelectDateBox(QWidget):

    year_box = None
    month_box = None
    day_box = None

    h_distance1 = 5
    h_distance2 = 35

    # 窗口大小
    wight = None
    high = None

    # 是否隐藏标题栏，默认隐藏
    is_hint = None
    date = QDate()

    def __init__(self, wight=600, high=200, is_hint=True):
        super().__init__()
        wight = TIME_INPUT_X * 1 + self.h_distance1 * 4 + MID_LABEL_X * 2 + DATE_INPUT_X * 2 + SHADOW_WIDTH*3
        high = SMALL_BUTTON_Y * 2 + TIME_INPUT_Y + V_DISTANCE3 * 2 + SHADOW_WIDTH
        self.set_window_size(wight, high)

        # 隐藏标题栏
        self.is_hint = is_hint
        if self.is_hint is True:
            self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.mid_label1 = QPushButton(self)
        self.mid_label1.setEnabled(False)
        self.mid_label2 = QPushButton(self)
        self.mid_label2.setEnabled(False)

        self.year_box = SelectBox()
        self.year_box.setParent(self)
        self.year_box.set_range(1950, 2200)
        self.year_box.value_line_edit.setText(str(self.date.currentDate().year()))
        self.month_box = SelectBox()
        self.month_box.setParent(self)
        self.month_box.set_range(1, 12)
        self.month_box.resize_value_edit(DATE_INPUT_X, DATE_INPUT_Y)
        self.month_box.value_line_edit.setText(str(self.date.currentDate().month()))
        self.day_box = SelectBox()
        self.day_box.setParent(self)
        self.check_day_range()
        self.day_box.resize_value_edit(DATE_INPUT_X, DATE_INPUT_Y)
        self.day_box.value_line_edit.setText(str(self.date.currentDate().day()))


        self.year_box.add_button.setObjectName("SelectDateBox_year_add_button")
        self.year_box.cut_button.setObjectName("SelectDateBox_year_cut_button")
        self.year_box.value_line_edit.setObjectName("SelectDateBox_year_value_line_edit")

        self.month_box.add_button.setObjectName("SelectDateBox_month_add_button")
        self.month_box.cut_button.setObjectName("SelectDateBox_month_cut_button")
        self.month_box.value_line_edit.setObjectName("SelectDateBox_month_value_line_edit")

        self.day_box.add_button.setObjectName("SelectDateBox_day_add_button")
        self.day_box.cut_button.setObjectName("SelectDateBox_day_cut_button")
        self.day_box.value_line_edit.setObjectName("SelectDateBox_day_value_line_edit")

        # self.day_box.set_range(1, 31)

        # self.day_box.value_line_edit.setText(str(self.date.currentDate().day()))
        self.month_change()

        self.init_ui()
        # self.show()

    def init_ui(self):

        self.year_box.move(0, 0)
        self.mid_label1.setGeometry(self.year_box.geometry().x()+TIME_INPUT_X+H_DISTANCE4 +SHADOW_WIDTH,
                                    SMALL_BUTTON_Y + V_DISTANCE3,
                                   MID_LABEL_X, MID_LABEL_Y)
        self.month_box.move(self.mid_label1.geometry().x()+H_DISTANCE4+MID_LABEL_X,
                            0)
        self.mid_label2.setGeometry(self.month_box.geometry().x()+DATE_INPUT_X+H_DISTANCE4 + SHADOW_WIDTH,
                                    SMALL_BUTTON_Y + V_DISTANCE3,
                                   MID_LABEL_X, MID_LABEL_Y)
        self.day_box.move(self.mid_label2.geometry().x()+MID_LABEL_X+H_DISTANCE4,
                            0)

        self.month_box.value_line_edit.textChanged[str].connect(self.month_change)
        self.year_box.value_line_edit.textChanged[str].connect(self.month_change)
        self.day_box.value_line_edit.textChanged[str].connect(self.month_change)

    # 初始化为目前时间
    def reset(self):

        self.year_box.value_line_edit.setText(str(self.date.currentDate().year()))
        self.month_box.value_line_edit.setText(str(self.date.currentDate().month()))
        self.day_box.value_line_edit.setText(str(self.date.currentDate().day()))

    def set_date(self, year, month, day):

        self.year_box.value_line_edit.setText(str(year))
        self.month_box.value_line_edit.setText(str(month))
        self.day_box.value_line_edit.setText(str(day))

    def set_window_size(self, wight, high):
        self.wight = wight
        self.high = high
        self.setFixedSize(wight, high)

    def set_year_range(self, min_value, max_value):
        self.year_box.set_range(min_value, max_value)

    def set_month_range(self, min_value, max_value):
        self.month_box.set_range(min_value, max_value)

    def set_data_range(self, min_value, max_value):
        self.day_box.set_range(min_value, max_value)

    def check_day_range(self):
        month = int(self.month_box.value_line_edit.text())
        year = int(self.year_box.value_line_edit.text())

        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            self.day_box.set_range(1, 31)
        elif month == 4 or month == 6 or month == 9 or month == 9 or month == 11:
            self.day_box.set_range(1, 30)
        elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
            self.day_box.set_range(1, 29)
        else:
            self.day_box.set_range(1, 28)

    def month_change(self):
        if not self.month_box.value_line_edit.text() == '':
            month = int(self.month_box.value_line_edit.text())
        else:
            month = self.date.currentDate().month()
        if not self.year_box.value_line_edit.text() == '':
            year = int(self.year_box.value_line_edit.text())
        else:
            year = self.date.currentDate().year()
        if not self.day_box.value_line_edit.text() == '':
            day = int(self.day_box.value_line_edit.text())
        else:
            day = self.date.currentDate().day()

        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            self.day_box.set_range(1, 31)
        elif month == 4 or month == 6 or month == 9 or month == 9 or month == 11:
            if day > 30:
                self.day_box.value_line_edit.setText("30")
            self.day_box.set_range(1, 30)
        elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
            if day > 29:
                self.day_box.value_line_edit.setText("29")
            self.day_box.set_range(1, 29)
        else:
            if day > 28:
                self.day_box.value_line_edit.setText("28")
            self.day_box.set_range(1, 28)

    def wake_up(self):
        self.show()


class SelectTimeBox(QWidget):
    hour_box = None
    minute_box = None

    # 窗口大小
    wight = None
    high = None

    # 是否隐藏标题栏，默认隐藏
    is_hint = None
    date = QTime()

    def __init__(self, wight=600, high=200, is_hint=True):
        super().__init__()
        wight = TIME_INPUT_X * 2 + H_DISTANCE3 * 2 + MID_LABEL_X + SHADOW_WIDTH*2
        high = SMALL_BUTTON_Y * 2 + TIME_INPUT_Y + V_DISTANCE3 * 2 + SHADOW_WIDTH
        self.set_window_size(wight, high)

        # 隐藏标题栏
        self.is_hint = is_hint
        if self.is_hint is True:
            self.setWindowFlag(Qt.FramelessWindowHint)

        self.mid_label = QPushButton(self)
        self.mid_label.setEnabled(False)

        self.hour_box = SelectBox()
        self.hour_box.setParent(self)
        self.hour_box.set_range(0, 23)
        self.hour_box.value_line_edit.setText(str(self.date.currentTime().hour()))
        # self.hour_box.value_line_edit.setText("00")
        self.minute_box = SelectBox()
        self.minute_box.setParent(self)
        self.minute_box.set_range(0, 59)
        self.minute_box.value_line_edit.setText(str(self.date.currentTime().minute()))
        # self.minute_box.value_line_edit.setText("00")

        self.hour_box.add_button.setObjectName("SelectTimeBox_hour_add_button")
        self.hour_box.cut_button.setObjectName("SelectTimeBox_hour_cut_button")
        self.hour_box.value_line_edit.setObjectName("SelectTimeBox_hour_value_line_edit")

        self.minute_box.add_button.setObjectName("SelectTimeBox_minute_add_button")
        self.minute_box.cut_button.setObjectName("SelectTimeBox_minute_cut_button")
        self.minute_box.value_line_edit.setObjectName("SelectTimeBox_minute_value_line_edit")

        self.init_ui()
        # self.show()

    def reset_h_distance(self, h_distance):
        wight = TIME_INPUT_X * 2 + h_distance * 2 + MID_LABEL_X + SHADOW_WIDTH*2
        high = SMALL_BUTTON_Y * 2 + TIME_INPUT_Y + V_DISTANCE3 * 2 + SHADOW_WIDTH
        self.set_window_size(wight, high)

        self.hour_box.move(0, 0)
        self.mid_label.setGeometry((self.wight - MID_LABEL_X) / 2 , SMALL_BUTTON_Y + V_DISTANCE3,
                                   MID_LABEL_X, MID_LABEL_Y)
        self.minute_box.move(self.mid_label.geometry().x() + h_distance  + MID_LABEL_X, 0)

    def init_ui(self):

        self.hour_box.move(0, 0)
        self.mid_label.setGeometry((self.wight-MID_LABEL_X)/2, SMALL_BUTTON_Y+V_DISTANCE3,
                                   MID_LABEL_X, MID_LABEL_Y)
        self.minute_box.move(self.mid_label.geometry().x()+H_DISTANCE3+MID_LABEL_X, 0)

    def reset(self):
        self.hour_box.value_line_edit.setText(str(self.date.currentTime().hour()))
        self.minute_box.value_line_edit.setText(str(self.date.currentTime().minute()))

    def set_time(self, hour, minute):
        self.hour_box.value_line_edit.setText(str(hour).zfill(2))
        self.minute_box.value_line_edit.setText(str(minute).zfill(2))

    def set_window_size(self, wight, high):
        self.wight = wight
        self.high = high
        self.setFixedSize(wight, high)

    def wake_up(self):
        self.show()


class SelectDateTimeBox(QFrame):
    date_box = None
    time_box = None

    wight = None
    high = None

    # 是否隐藏标题栏，默认隐藏
    is_hint = None

    h_distance1 = 5
    h_distance2 = 35

    background_label = None

    style_path = 'gui/to_do_edit_window.qss'

    def __init__(self, wight=500, high=300, is_hint=True):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)


        # 隐藏标题栏
        self.is_hint = is_hint
        if self.is_hint is True:
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlag(Qt.FramelessWindowHint | Qt.Window)
            # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.background_label = QLabel(self)

        self.date_box = SelectDateBox()
        self.date_box.setParent(self)
        self.time_box = SelectTimeBox()
        self.time_box.setParent(self)
        self.time_box.reset_h_distance(H_DISTANCE4)
        self.time_box.set_time(0, 0)

        wight = self.date_box.wight + self.time_box.wight + LEFT_DISTANCE*3
        high = self.date_box.high + UP_DISTANCE * 2 + V_DISTANCE + TIME_BUTTON_Y
        self.set_window_size(wight, high)
        self.background_label.setGeometry(0, 0, wight, high)
        self.background_label.setObjectName("edit_todo_window_select_date_background")

        self.check_button = QPushButton(self)
        self.check_button.clicked.connect(self.close)
        self.init_ui()

    def init_ui(self):
        # 设定id
        # self.setObjectName("edit_todo_window_select_date_background")
        self.date_box.year_box.add_button.setProperty("class", "edit_todo_window_date_add_button")
        self.date_box.month_box.add_button.setProperty("class", "edit_todo_window_date_add_button")
        self.date_box.day_box.add_button.setProperty("class", "edit_todo_window_date_add_button")
        self.time_box.hour_box.add_button.setProperty("class", "edit_todo_window_date_add_button")
        self.time_box.minute_box.add_button.setProperty("class", "edit_todo_window_date_add_button")

        self.date_box.year_box.cut_button.setProperty("class", "edit_todo_window_date_cut_button")
        self.date_box.month_box.cut_button.setProperty("class", "edit_todo_window_date_cut_button")
        self.date_box.day_box.cut_button.setProperty("class", "edit_todo_window_date_cut_button")
        self.time_box.hour_box.cut_button.setProperty("class", "edit_todo_window_date_cut_button")
        self.time_box.minute_box.cut_button.setProperty("class", "edit_todo_window_date_cut_button")

        self.date_box.year_box.value_line_edit.setProperty("class", "date_two")
        self.date_box.month_box.value_line_edit.setProperty("class", "date_two")
        self.date_box.day_box.value_line_edit.setProperty("class", "date_two")
        self.time_box.hour_box.value_line_edit.setProperty("class", "date_two")
        self.time_box.minute_box.value_line_edit.setProperty("class", "date_two")

        self.date_box.year_box.value_line_edit.setObjectName("edit_todo_window_date_value_line_edit_L")
        self.date_box.month_box.value_line_edit.setObjectName("edit_todo_window_date_value_line_edit")
        self.date_box.day_box.value_line_edit.setObjectName("edit_todo_window_date_value_line_edit")
        self.time_box.hour_box.value_line_edit.setObjectName("edit_todo_window_date_value_line_edit_L")
        self.time_box.minute_box.value_line_edit.setObjectName("edit_todo_window_date_value_line_edit_L")

        self.date_box.mid_label1.setProperty("class", "edit_todo_window_date_mid_button")
        self.date_box.mid_label2.setProperty("class", "edit_todo_window_date_mid_button")

        self.time_box.mid_label.setProperty("class", "edit_todo_window_time_mid_button")

        self.check_button.setProperty("class", "edit_todo_window_date_check_button")

        self.date_box.move(LEFT_DISTANCE, UP_DISTANCE)
        self.time_box.move(self.date_box.geometry().x()+self.date_box.wight+LEFT_DISTANCE, UP_DISTANCE)
        self.check_button.setGeometry((self.wight-TIME_BUTTON_X)/2, self.date_box.geometry().y()+self.date_box.high+V_DISTANCE,
                                      TIME_BUTTON_X, TIME_BUTTON_Y)
        self.check_button.setGraphicsEffect(get_shadow_effect(self))


        # 设定qss
        self.set_style(self.style_path)

    def set_style(self, path):
        file = open(path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    def set_window_size(self, wight, high):
        self.wight = wight
        self.high = high
        self.setFixedSize(wight, high)

    def wake_up(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.show()