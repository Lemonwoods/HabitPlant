'''
待办事项与每日计划的页面
'''

from PyQt5.QtWidgets import QWidget
from main_window.tab_widget import TabWidget
from habit.edit_window import *
from to_do.to_do_list_box import ToDoPunchInterface
from to_do.my_day_list_box import MyDayPunchInterface


class ToDoWidget(TabWidget):

    # 基础控件
    h_to_do_list_box = None
    h_to_do_edit_window = None
    h_my_day_list_box = None
    h_my_day_edit_window = None
    h_gold_coin=None
    h_statistic=None

    def __init__(self, parent,gold_coin,statistic):
        super().__init__(parent)

        # 初始化控件
        self.h_gold_coin=gold_coin
        self.h_statistic=statistic
        self.h_to_do_edit_window = ToDoEditWindow()
        self.h_to_do_list_box = ToDoPunchInterface(self, self.h_to_do_edit_window,self.h_gold_coin,self.h_statistic)
        self.h_my_day_edit_window = MyDayEditWindow()
        self.h_my_day_list_box = MyDayPunchInterface(self, self.h_my_day_edit_window,self.h_gold_coin,self.h_statistic)

        self.init_ui()

    def init_ui(self):
        self.setObjectName('to_do_widget')

        self.h_my_day_list_box.move(66,50)
        self.h_to_do_list_box.move(632,50)

        self.show()