import os

from PyQt5.QtWidgets import QPushButton, QFrame, QLabel
from PyQt5.QtCore import QEvent, QDate
from main_window.list_box import ListBox
from to_do.to_do_bar import ToDoBar
from functools import partial
import json
from gui.shadow import get_shadow_effect

INCREASE_MONEY=100

class AddButton(QPushButton):
    h_height = 70
    h_width = 70

    def __init__(self, parent, listbox):
        super(AddButton, self).__init__()
        self.setParent(parent)
        self.clicked.connect(listbox.add)
        self.init_ui()

    def init_ui(self):
        # self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName("to_do_list_box_add_button")
        # self.setProperty('class', 'list_box_add_button')
        self.resize(self.h_width, self.h_height)


class CompletedButton(QPushButton):
    h_height = 60
    h_width = 60

    def __init__(self,parent,listbox):
        super().__init__()
        self.setParent(parent)
        self.clicked.connect(listbox.show_finished)
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName('to_do_list_box_show_complete_button')
        self.resize(self.h_width,self.h_height)


class UncompletedButton(QPushButton):
    h_height = 60
    h_width = 60

    def __init__(self,parent,listbox):
        super().__init__()
        self.setParent(parent)
        self.clicked.connect(listbox.show_unfinished)
        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName('to_do_list_box_show_uncomplete_button')
        self.resize(self.h_width,self.h_height)


class ToDoListBox(ListBox):

    # 存储数据到本地
    data_list = []
    #基本控件
    gold_coin=None
    h_statistic=None
    #默认状态是unfininshed （也就是0） finished（也就是1）
    finshed_or_unfinshed=0

    def __init__(self, parent, edit_window,gold_coin,statistic):
        super(ToDoListBox, self).__init__(parent, ToDoBar.h_width, ToDoBar.h_height, edit_window)
        self.gold_coin=gold_coin
        self.h_statistic=statistic
        self.data = {"title": None,
                     "year": None,
                     "month": None,
                     "day": None,
                     "hour": None,
                     "minute": None,
                     "finished": None,
                     "create_date": None,
                     "create_time": None
                     }
        self.edit_window.delete_button.clicked.connect(self.delete)
        self.edit_window.save_button.clicked.connect(self.saved)
        self.edit_window.cancel_button.clicked.connect(self.cancle)
        self.init_ui()
        # self.show()

    def add(self):
        try:
            self.bar = ToDoBar(self)
            # self.bar.refresh_info()
            super().add()
            #绑定金币与打勾按钮
            self.bar.check_button.clicked.connect(partial(self.compeleted_habit,self.bar))
            # 将habit_bar与edit_window的信号槽绑定
            self.bar.text_button.clicked.connect(partial(self.edit_window.wake_up, self.bar))
            self.bar.text_button.clicked.emit()
        except Exception:
            pass

    # 本地数据加载添加
    def add_from_local(self, data):
        self.bar = ToDoBar(self)
        self.bar.h_title = data["title"]
        self.bar.h_year = data["year"]
        self.bar.h_month = data["month"]
        self.bar.h_day = data["day"]
        self.bar.h_hour = data["hour"]
        self.bar.h_minute = data["minute"]
        self.bar.h_is_finished=data["finished"]
        super().add()
        self.bar_list.append(self.bar)
        #载入数据时刷新打勾状态
        self.bar.refresh_info()
        #绑定金币与打勾按钮
        self.bar.check_button.clicked.connect(partial(self.compeleted_habit,self.bar))
        # 将habit_bar与edit_window的信号槽绑定
        self.bar.text_button.clicked.connect(partial(self.edit_window.wake_up, self.bar))
         # self.bar.text_button.clicked.emit()

    def saved(self):
        try:
            if not self.is_exist(self.bar):
                self.bar_list.append(self.bar)
            self.save_to_local()
            self.h_statistic.get_today_todo()
            self.edit_window.to_do_bar.refresh_info()
            self.referesh_status()
        except Exception:
            pass

    def cancle(self):
        try:
            super().cancle()
        except Exception:
            pass

    # 判断是否已存在列表中
    def is_exist(self, bar):
        for i in self.bar_list:
            if i.create_time == bar.create_time:
                return True
        return False

    #完成每日习惯后 增加金币
    def compeleted_habit(self,button):
        try:
            if(button.h_is_finished):
                # 调整按钮状态的部分已经移交给了check_button类，无需在这里完成
                self.gold_coin.increase_t_amount(INCREASE_MONEY)
                self.h_statistic.to_do_finished_count+=1
                self.h_statistic.to_do_unfinished_count -= 1
            else:
                self.gold_coin.decrease_t_amount(INCREASE_MONEY)
                self.h_statistic.to_do_finished_count-=1
                self.h_statistic.to_do_unfinished_count += 1
            self.save_to_local()
            self.referesh_status()
            self.h_statistic.get_today_todo()
        except Exception:
            pass

    def init_ui(self):
        super().init_ui()
        # self.setObjectName("to_do_list_box")

    # 把数据保存到本地
    def save_to_local(self):
        self.data_list.clear()

        for t in self.bar_list:
            data = {"title": t.h_title,
                    "year": t.h_year,
                    "month": t.h_month,
                    "day": t.h_day,
                    "hour": t.h_hour,
                    "minute": t.h_minute,
                    "finished": t.h_is_finished,
                    "create_date": t.create_date,
                    "create_time": t.create_time
                    }
            self.data_list.append(data)

        path = "data/todo/todo_data.json"

        with open(path, "w") as f:
            json.dump(self.data_list, f)

    def delete(self):
        try:
            super(ToDoListBox, self).delete()
            self.referesh_status()
            self.save_to_local()
        except Exception:
            pass

    def show_finished(self):
        i=0
        for button in self.bar_list:
            if(button.h_is_finished):
                if (i == 0):
                    button.move(self.bar_space_left, 0)
                else:
                    button.move(self.bar_space_left, self.bar_height * i + self.two_bar_space * i)
                button.show()
                i+=1
            else:
                button.hide()
        self.scrollarea_widget_contents.resize(self.bar_width + self.bar_space_right,
                                               self.bar_height * i + self.two_bar_space * i)
        self.finshed_or_unfinshed=1

    def show_unfinished(self):
        i = 0
        for button in self.bar_list:
            if (not button.h_is_finished):
                if (i == 0):
                    button.move(self.bar_space_left, 0)
                else:
                    button.move(self.bar_space_left, self.bar_height * i + self.two_bar_space * i)
                button.show()
                i += 1
            else:
                button.hide()
        self.scrollarea_widget_contents.resize(self.bar_width + self.bar_space_right,
                                               self.bar_height * i + self.two_bar_space * i)
        self.finshed_or_unfinshed=0

    def referesh_status(self):
        if(self.finshed_or_unfinshed):
            self.show_finished()
        else:
            self.show_unfinished()


class ToDoPunchInterface(QFrame):
    h_width = 500
    h_height = 500
    space_top = 30
    space_left = 40

    #基础控件
    h_edit_window = None
    h_listbox = None
    h_addbutton = None
    h_gold_coin=None
    h_statistic=None
    h_compelet_button=None
    h_uncompelet_button=None
    h_name_label=None

    h_data = None
    h_data_list = None

    def __init__(self, parent, edit_window,gold_coin,statistic):
        super(ToDoPunchInterface, self).__init__()
        self.setParent(parent)
        #初始化基本控件
        self.h_edit_window = edit_window
        self.h_gold_coin=gold_coin
        self.h_statistic=statistic
        self.h_listbox = ToDoListBox(self, self.h_edit_window,self.h_gold_coin,self.h_statistic)

        self.h_name_label=QLabel(self)
        self.h_addbutton = AddButton(self, self.h_listbox)
        self.h_compelet_button =CompletedButton(self,self.h_listbox)
        self.h_uncompelet_button =UncompletedButton(self,self.h_listbox)

        # 这是滚动区域拖动文本联动滚动条
        self.scroll_bar = self.h_listbox.verticalScrollBar()
        self.h_listbox.installEventFilter(self)
        self.last_time_move = 0

        # 布置界面以及显示
        self.init_ui()

        # 本地数据载入
        path = "data/todo/todo_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                self.h_data_list = json.load(f)
            self.init_data()

    # 本地数据载入
    def init_data(self):
        for i in self.h_data_list:
                self.h_listbox.add_from_local(i)
        self.h_listbox.referesh_status()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.setObjectName("to_do_punch_interface_frame")

        self.resize(self.h_width, self.h_height)
        #控件位置移动
        self.h_listbox.move(self.space_left, self.space_top)
        self.h_addbutton.move(25,self.h_height-self.h_addbutton.h_height-25)
        self.h_compelet_button.move(self.h_width-self.h_compelet_button.h_width-15,self.h_height-self.h_compelet_button.h_height-25)
        self.h_uncompelet_button.move(self.h_width-self.h_uncompelet_button.h_width-self.h_compelet_button.h_width-25,
                                      self.h_height-self.h_uncompelet_button.h_height-25)

        #name_label样式
        self.h_name_label.resize(180,70)
        self.h_name_label.setObjectName("to_do_name_label")
        self.h_name_label.move(25,self.h_height-self.h_addbutton.h_height-25)
        self.h_name_label.setProperty('class','info_font')
        self.h_name_label.setText('          待办')
        self.h_name_label.setGraphicsEffect(get_shadow_effect(self))

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if self.last_time_move == 0:
                self.last_time_move = event.pos().y()

            distance = self.last_time_move - event.pos().y()
            self.scroll_bar.setValue(self.scroll_bar.value() + distance)
            self.last_time_move = event.pos().y()
        elif event.type() == QEvent.MouseButtonRelease:
            self.last_time_move = 0
        return QFrame.eventFilter(self, source, event)
