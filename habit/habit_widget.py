'''
习惯打卡的weight，整个习惯打卡的窗口布局在这个文件里面完成
'''

from PyQt5.QtWidgets import QWidget
from habit.habit_listbox import PunchInterface
from habit.edit_window import EditWindow
from main_window.tab_widget import TabWidget
from habit.calendar_widget import CalendarWidget

class HabitWidget(TabWidget):
    # 成员组件
    h_list_box = None
    h_edit_window = None
    h_calendar_widget = None
    h_gold_coin=None
    h_statistic=None

    def __init__(self, parent,gold_coin,statistic):
        super().__init__(parent)

        # 添加list_box, edit_window, calendar,以及金币
        self.h_statistic=statistic
        self.h_gold_coin=gold_coin
        self.h_edit_window = EditWindow()
        self.h_list_box = PunchInterface(self, self.h_edit_window,self.h_gold_coin,self.h_statistic)
        self.h_calendar_widget = CalendarWidget(self)

        # 连接list_box 和 calendar
        self.h_calendar_widget.init_list_box(self.h_list_box)

        # 初始化ui
        self.init_ui()

    def init_ui(self):

        self.setObjectName('habit_widget')

        self.h_calendar_widget.move(25,50)
        self.h_list_box.move(650,50)
        self.show()