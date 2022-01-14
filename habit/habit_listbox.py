import json
import os
from copy import deepcopy
from datetime import datetime
from os.path import abspath, dirname

from PyQt5.QtWidgets import QPushButton, QFrame, QLabel
from PyQt5.QtCore import QEvent, QDate, QTimer, pyqtSignal

from Controller.date_control import DateController
from main_window.list_box import ListBox
from habit.habit_bar import HabitBar
from functools import partial
from gui.shadow import get_shadow_effect

INCREASE_MONEY=100
week = {
    "0": "Mon",
    "1": "Tue",
    "2": "Wen",
    "3": "Thur",
    "4": "Fri",
    "5": "Sat",
    "6": "Sun"
}

class AddButton(QPushButton):
    _not_add_signal=pyqtSignal()
    h_height=70
    h_width=70
    list_box=None
    h_date=None

    def __init__(self,parent,listbox,date):
        super(AddButton, self).__init__()
        self.setParent(parent)
        self.list_box=listbox
        self.h_date=date
        self.clicked.connect(self.list_box_add)
        self.init_ui()

    def init_ui(self):
       # self.setGraphicsEffect(get_shadow_effect(self))
       self.setObjectName("habit_list_box_add_button")
       # self.setProperty('class','list_box_add_button')
       self.resize(self.h_width, self.h_height)

    def list_box_add(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        if(int(self.h_date.year) !=year or int(self.h_date.month) !=month or int(self.h_date.day) !=day):
            self._not_add_signal.emit()
        else:
            self.list_box.add()



class HabitListBox(ListBox):
    # 存储数据到本地
    data_list = []
    gold_coin = None
    h_statistic=None

    def __init__(self,parent,edit_window,gold_coin,statistic):
        super(HabitListBox,self).__init__(parent,HabitBar.h_width,HabitBar.h_height,edit_window)
        self.gold_coin = gold_coin
        self.h_statistic=statistic
        self.data = {"data": None,
                     "habits": [
                         {
                             "title": None,
                             "content": None,
                             "times": None,
                             "create_date": None,
                             "create_time": None,
                             "finished": None,
                             "week": []
                         }
                     ]
                     }

        # 信号绑定
        self.edit_window.delete_button.clicked.connect(self.delete)
        self.edit_window.save_button.clicked.connect(self.saved)
        self.edit_window.cancel_button.clicked.connect(self.cancle)

        # 初始化ui
        self.init_ui()

    #重载add函数 绑定button里面的其他button的信号
    def add(self):
        try:
            self.bar = HabitBar(self)
            super().add()
            # 将habit_bar与edit_window的信号槽绑定
            self.bar.check_button.clicked.connect(partial(self.compeleted_habit,self.bar))
            self.bar.text_button.clicked.connect(partial(self.edit_window.wake_up, self.bar))
            self.bar.text_button.clicked.emit()
        except Exception:
            pass

    # 本地数据加载添加
    def add_from_local(self, data):
        self.bar = HabitBar(self)
        self.bar.h_title = data["title"]
        self.bar.h_content = data["content"]
        # self.bar.h_tag = data["tag"]
        self.bar.h_times = data["times"]
        self.bar.h_is_finished = data["finished"]
        self.bar.h_week = data["week"]
        self.bar.create_time = data["create_time"]
        self.bar.create_date = data["create_date"]
        # self.bar.h_hour = data["hour"]
        # self.bar.h_minute = data["minute"]
        super().add()
        self.bar.show()
        self.bar_list.append(self.bar)
        #载入数据时刷新打勾状态
        self.bar.check_button.refresh_check_icon()
        #将打卡按钮和金币系统绑定
        self.bar.check_button.clicked.connect(partial(self.compeleted_habit, self.bar))
        # 将habit_bar与edit_window的信号槽绑定
        self.bar.text_button.clicked.connect(partial(self.edit_window.wake_up, self.bar))
        # self.bar.text_button.clicked.emit()
        self.bar.refresh_info()

    def cancle(self):
        try:
            super(HabitListBox, self).cancle()
        except Exception:
            pass

    def saved(self):
        if not self.is_exist(self.bar):
           self.bar_list.append(self.bar)
        self.edit_window.habit_bar.refresh_info()
        self.save_to_local()
        weekday = datetime.now().weekday()
        if self.bar.h_week[str(week[str(weekday)])] is True:
              self.bar.show()
        else:
               self.bar.hide()
               self.bar_list.remove(self.bar)
               self.referesh_list_box()

    # 判断是否已存在列表中
    def is_exist(self, bar):
        for i in self.bar_list:
            if i.create_time == bar.create_time:
                return True
        return False

    #完成每日习惯后 连锁的函数呈现在这里
    def compeleted_habit(self,button):
        try:
            if(button.h_is_finished):
                # 调整按钮状态的部分已经移交给了check_button类，无需在这里完成
                self.gold_coin.increase_t_amount(INCREASE_MONEY)
                self.h_statistic.habit_finished_count+=1
                self.h_statistic.habit_unfinished_count-=1
            else:
                self.gold_coin.decrease_t_amount(INCREASE_MONEY)
                self.h_statistic.habit_finished_count-=1
                self.h_statistic.habit_unfinished_count+=1
            self.save_to_local()
            self.h_statistic.habit_week_info()
        except Exception:
            pass

    def delete(self):
        try:
            super(HabitListBox, self).delete()
        except:
            pass

    def init_ui(self):
        super().init_ui()
        # self.setObjectName('habit_list_box')
        # self.scrollarea_widget_contents.setObjectName("habit_list_box_widget")
        self.resize(self.l_width,self.l_height)

    # 把数据保存到本地
    def save_to_local(self):
        year = self.bar_list[0].create_date["year"]
        month = self.bar_list[0].create_date["month"]
        day = self.bar_list[0].create_date["day"]

        self.data_list.clear()

        # 本地数据载入
        # year = QDate().currentDate().year()
        # month = QDate().currentDate().month()
        # day = QDate().currentDate().day()

        path = "data/habit/" + str(year) + "_" + str(
            month) + "_" + "habit_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)

            for h in local_data:
                if h["data"] == day:
                    self.data_list = h["habits"]
            new_data = {"data": day,
                          "habits": []}

        else:
            local_data = []

        for d in self.data_list[:]:
            if d["create_date"] == {"year": year, "month": month, "day": day}:
                self.data_list.remove(d)

        for t in self.bar_list:
            data = {"title": t.h_title,
                    "content": t.h_content,
                    "times": t.h_times,
                    "create_date": t.create_date,
                    "create_time": t.create_time,
                    "finished": t.h_is_finished,
                    "week": t.h_week
                    }
            self.data_list.append(data)
        new_data["habits"] = self.data_list

        path = "data/habit/" + str(year) + "_" + str(
            month) + "_" + "habit_data.json"

        exist = False
        if os.path.exists(path):
            for h in local_data:
                if h["data"] == day:
                    h["habits"] = self.data_list
                    exist = True
            if not exist is True:
                local_data.append(new_data)
        else:
            local_data_temp = {"data": day,
                          "habits": self.data_list}
            local_data.append(local_data_temp)

        with open(path, "w") as f:
            json.dump(local_data, f)


class PunchInterface(QFrame):
    h_width= 500
    h_height= 500
    space_top = 30
    space_left = 45
    h_edit_window = None
    h_listbox=None
    h_addbutton=None
    h_gold_coin=None
    h_statistic=None
    h_name_label=None
    h_message_box=None

    h_data = None
    h_data_list = None
    h_date=None

    def __init__(self,parent, edit_window,gold_coin,statistic):
        super(PunchInterface, self).__init__()

        self.setParent(parent)

        # 初始化基本控件
        self.h_edit_window = edit_window
        self.h_gold_coin=gold_coin
        self.h_statistic=statistic


        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        self.h_name_label=QLabel(self)
        self.h_listbox=HabitListBox(self, self.h_edit_window,self.h_gold_coin,self.h_statistic)
        self.h_date=DateController(year,month,day)
        self.h_addbutton=AddButton(self, self.h_listbox,self.h_date)
        self.h_message_box=MessageBox(self)

        # 这是滚动区域拖动文本联动滚动条
        self.scroll_bar = self.h_listbox.verticalScrollBar()
        self.h_listbox.installEventFilter(self)
        self.last_time_move = 0

        # 布置界面以及显示
        self.init_ui()

        self.h_addbutton._not_add_signal.connect(lambda :self.h_message_box.wake_up("请在当前日期添加"))

        # 本地数据载入
        path = "data/habit/" + str(year) + "_" + str(
            month) + "_" + "habit_data.json"

        # 补充未启动应用的数据
        if os.path.exists(path):

            with open(path, "r") as f:
                local_data = json.load(f)
            if local_data:
                temp = local_data[len(local_data)-1]
                days = day - temp["data"]
                if days > 0:
                    for i in range(0, days):
                        temp_data = {
                            "data": deepcopy(temp["data"]) + i + 1,
                            "habits": deepcopy(temp["habits"])
                        }
                        for h in temp_data["habits"]:
                            h["finished"] = False
                            h["create_date"] = {"year": year, "month": month, "day": day}
                        local_data.append(temp_data)

            with open(path, "w") as f:
                json.dump(local_data, f)
        else:
            with open(path, "w") as f:
                local_data = []
                json.dump(local_data, f)
            # 假定上个月分有数据
            if local_data:
                old_month = month - 1
                old_year = year
                old_day = self.find_days(old_month, old_year)
                temp2 = None
                if old_month > 0:
                    path2 = path = "data/habit/" + str(old_year) + "_" + str(old_month) + "_" + "habit_data.json"
                    if os.path.exists(path2):
                        with open(path2, "r") as ff:
                            local_data2 = json.load(ff)
                        temp2 = local_data2[len(local_data2) - 1]
                        days2 = old_day - temp2["data"]
                        if days2 > 0:
                            for i in range(0, days2):
                                temp_data2 = {
                                    "data": temp2["data"] + i + 1,
                                    "habits": temp2["habits"]
                                }
                                for h in temp_data2["habits"]:
                                    h["finished"] = False
                                local_data2.append(temp_data2)
                        with open(path2, "w") as ff:
                            json.dump(local_data2, ff)

                for i in range(0, day):
                    temp_data = {
                        "data": i + 1,
                        "habits": temp2["habits"]
                    }
                    for h in temp_data["habits"]:
                        h["finished"] = False
                    local_data.append(temp_data)

        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)
            if local_data:
                temp = local_data[0]
                for h in local_data[:]:
                    if h["data"] == day:
                        self.h_data_list = h["habits"]
                        old_day = temp["data"]
                    temp = h
                if not self.h_data_list is None:
                    self.init_data()

    # 本地数据载入
    def init_data(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        weekday = datetime.now().weekday()
        week = {
            "0" : "Mon",
            "1" : "Tue",
            "2" : "Wen",
            "3" : "Thur",
            "4" : "Fri",
            "5" : "Sat",
            "6" : "Sun"
        }
        weekday = week[str(weekday)]
        for i in self.h_data_list:
            if i["create_date"]["year"] == year and i["create_date"]["month"] == month and i["create_date"]["day"] == day and i["week"][weekday] is True:
                self.h_listbox.add_from_local(i)

    def init_data_by_calendar(self, year, month, day, weekday):
        self.h_date.year=year
        self.h_date.month=month
        self.h_date.day=day
        path = "data/habit/" + str(year) + "_" + str(
             month) + "_" + "habit_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)

                for h in local_data:
                    if h["data"] == day:
                        self.h_data_list = h["habits"]

        self.h_listbox.all_hide()
        self.h_listbox.bar_list.clear()
        self.h_listbox.referesh_list_box()

        week = {
            "0": "Mon",
            "1": "Tue",
            "2": "Wen",
            "3": "Thur",
            "4": "Fri",
            "5": "Sat",
            "6": "Sun"
        }
        weekday = week[str(weekday)]
        if self.h_data_list is not None:
            for i in self.h_data_list:
                if i["create_date"]["year"] == year and i["create_date"]["month"] == month and i["create_date"]["day"] == day and i["week"][weekday] is True:
                    self.h_listbox.add_from_local(i)

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        #设置id
        self.setObjectName('habit_punch_interface_widget')
        #更改大小
        self.resize(self.h_width, self.h_height)
        #移动位置
        self.h_addbutton.move(25,self.h_height-self.h_addbutton.h_height-20)
        self.h_listbox.move(self.space_left, self.space_top)
        self.h_message_box.move(25,self.h_height-self.h_addbutton.h_height-20)

        #name_label样式
        self.h_name_label.resize(250,70)
        self.h_name_label.setObjectName("habit_name_label")
        self.h_name_label.move(25,self.h_height-self.h_addbutton.h_height-20)
        self.h_name_label.setProperty('class','info_font')
        self.h_name_label.setText('          习惯打卡')
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

    def find_days(self, month, year):
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            return 31
        elif month == 4 or month == 6 or month == 9 or month == 9 or month == 11:
            return 30
        elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
            return 29
        else:
            return 28


class MessageBox(QPushButton):

    message_text = None
    width = 250
    high = 70

    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.hide()
        self.resize(self.width, self.high)
        self.setObjectName('plant_bubble')
        self.setProperty('class','bubble_font')
        self.move(150,54)

    def wake_up(self, text):
        self.setText(text)
        self.show()
        QTimer.singleShot(3000, self.close)