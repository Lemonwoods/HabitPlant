import time

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from habit.habit_bar import TextButton, CheckButton,HabitBar


class ToDoBar(HabitBar):
    # t_title = None
    # t_is_delete = False
    # t_year = None
    # t_month = None
    # t_day = None
    # t_hour = None
    # t_minute = None
    #
    # # 创建时间
    # create_date = {
    #     "year": None,
    #     "month": None,
    #     "day": None
    # }
    # # 创建时间，同时作为id
    # create_time = None
    # # 基础属性
    # h_height = 80
    # h_width = 300
    #
    # # 基础控件
    # text_button = None
    # check_button = None
    #
    # def __init__(self,parent):
    #     super().__init__()
    #     self.setParent(parent)
    #
    #     # 初始化控件
    #     self.text_button = TextButton(self)
    #     self.check_button = CheckButton(self)
    #
    #     self.create_date["year"] = QDate().currentDate().year()
    #     self.create_date["month"] = QDate().currentDate().month()
    #     self.create_date["day"] = QDate().currentDate().day()
    #
    #     self.create_time = time.time()
    #
    #     # 初始化ui
    #     self.init_ui()
    #
    # def init_ui(self):
    #     self.resize(self.h_width, self.h_height)
    #     self.show()

    def __init__(self, parent):
        super().__init__(parent)

        # 初始化ui
        self.init_child_ui()

    def init_child_ui(self):
        self.text_button.setObjectName('to_do_text_button')

    def time_to_describe(self):
        if int(self.h_hour) == 0 and int(self.h_minute) == 0:
            self.h_content = ''
        else:
            self.h_content = f'时间为：{self.h_year}-{self.h_month}-{self.h_day} {self.h_hour}:{self.h_minute}'

    def refresh_info(self):
        self.time_to_describe()
        super().refresh_info()