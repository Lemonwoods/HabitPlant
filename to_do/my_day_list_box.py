import os
from os.path import abspath,dirname
from PyQt5.QtWidgets import QPushButton, QFrame,QLabel
from PyQt5.QtCore import QEvent, QDate, Qt, QTimer
from PyQt5.Qt import pyqtSignal
from Controller.date_control import DateController
from main_window.list_box import ListBox
from to_do.my_day_bar import MyDayBar
from functools import partial
from habit.calendar_widget import CalendarWidget
import json
from gui.shadow import get_shadow_effect

INCREASE_MONEY=100

class AddButton(QPushButton):
    _not_add_signal=pyqtSignal()
    h_height = 70
    h_width = 70
    list_box=None
    h_date=None

    def __init__(self, parent, listbox,date):
        super(AddButton, self).__init__()
        self.setParent(parent)
        self.list_box=listbox
        self.h_date=date
        self.clicked.connect(self.refresh_add)
        self.init_ui()

    def init_ui(self):
        # self.setGraphicsEffect(get_shadow_effect(self))

        self.setObjectName("my_day_list_box_add_button")
        # self.setProperty('class', 'list_box_add_button')
        self.resize(self.h_width, self.h_height)

    def refresh_add(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        if(int(self.h_date.year) !=year or int(self.h_date.month) !=month or int(self.h_date.day) !=day):
            self._not_add_signal.emit()
        else:
            self.list_box.add()


class ShowCalendarButton(QPushButton):
    h_height = 60
    h_width = 60
    def __init__(self,parent,list_box):
        super().__init__()
        self.setParent(parent)
        self.clicked.connect(list_box.show_calendar)
        self.init_ui()
    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))
        self.setObjectName("my_day_list_box_show_calendar_button")
        # self.setProperty('class', 'list_box_add_button')
        self.resize(self.h_width, self.h_height)


class MyDayListBox(ListBox):
    # 存储数据到本地
    data_list = []
    #基本控件
    gold_coin=None
    h_statistic=None
    h_calendar=None
    h_calendar_widget=None

    def __init__(self, parent, edit_window,gold_coin,statistic):
        super(MyDayListBox, self).__init__(parent, MyDayBar.h_width, MyDayBar.h_height, edit_window)
        self.gold_coin=gold_coin
        self.h_statistic=statistic
        self.h_calendar_widget=MyDayCalendar()
        self.h_calendar=self.h_calendar_widget.calendar
        self.data = {"data": None,
                     "mydays": [
                         {
                             "title": None,
                             "hour": None,
                             "minute": None,
                             "create_date": None,
                             "create_time": None,
                             "finished": None
                        }
                     ]
                     }
        self.edit_window.delete_button.clicked.connect(self.delete)
        self.edit_window.save_button.clicked.connect(self.saved)
        self.edit_window.cancel_button.clicked.connect(self.cancle)

        #初始化ui
        self.init_ui()

    def add(self):
        try:
            self.bar = MyDayBar(self)
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
        self.bar = MyDayBar(self)
        self.bar.h_title = data["title"]
        self.bar.h_hour = data["hour"]
        self.bar.h_minute = data["minute"]
        self.bar.create_time = data["create_time"]
        self.bar.create_date = data["create_date"]
        self.bar.h_is_finished = data["finished"]
        super().add()
        self.bar.show()
        self.bar_list.append(self.bar)
        #绑定金币与打勾按钮
        self.bar.check_button.clicked.connect(partial(self.compeleted_habit,self.bar))
        # 将habit_bar与edit_window的信号槽绑定
        self.bar.text_button.clicked.connect(partial(self.edit_window.wake_up, self.bar))
        # self.bar.text_button.clicked.emit()
        self.bar.refresh_info()
        self.refresh_sort()

    # 判断是否已存在列表中
    def is_exist(self, bar):
        for i in self.bar_list:
            if i.create_time == bar.create_time:
                return True
        return False

    def saved(self):
        try:
            if not self.is_exist(self.bar):
                self.bar_list.append(self.bar)
            self.save_to_local()
            #刷新list_box 并且重新显示
            self.sort_by_time()
            self.referesh_list_box()
            self.edit_window.my_day_bar.refresh_info()
            self.bar.show()
        except Exception:
            pass

    def refresh_sort(self):
        self.sort_by_time()
        self.referesh_list_box()

    #按时间整理
    def sort_by_time(self):
        n = len(self.bar_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if(self.compare_time(self.bar_list[j],self.bar_list[j+1])):
                    self.bar_list[j],self.bar_list[j+1]=self.bar_list[j+1],self.bar_list[j]

    #左边晚于右边返回正确
    def compare_time(self,bar1,bar2):
        if(int(bar1.h_hour) > int(bar2.h_hour)):
            return True
        elif(int(bar1.h_hour)==int(bar2.h_hour) and int(bar1.h_minute) >= int(bar2.h_minute)):
            return True
        return  False

    def cancle(self):
        try:
            super().cancle()
        except:
            pass

    def delete(self):
        try:
            super().delete()
            self.save_to_local()
        except Exception:
            pass

    #完成每日习惯后 增加金币
    def compeleted_habit(self,button):
        try:
            if(button.h_is_finished):
                # 调整按钮状态的部分已经移交给了check_button类，无需在这里完成
                self.gold_coin.increase_t_amount(INCREASE_MONEY)
                self.h_statistic.my_day_finished_count+=1
                self.h_statistic.my_day_unfinished_count-=1
            else:
                self.gold_coin.decrease_t_amount(INCREASE_MONEY)
                self.h_statistic.my_day_finished_count-=1
                self.h_statistic.my_day_unfinished_count+=1
            self.save_to_local()
            self.h_statistic.my_day_week_info()
        except Exception:
            pass

    def show_calendar(self):
        self.h_calendar_widget.show()

    def init_ui(self):
        super().init_ui()
        # self.setObjectName("my_day_list_box")

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

        new_data = {"data": day,
                    "mydays": []}

        path = "data/myday/" + str(year) + "_" + str(month) + "_" + "myday_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)

            for h in local_data:
                if h["data"] == day:
                    self.data_list = h["mydays"]
            new_data = {"data": day,
                          "mydays": []}
        else:
            local_data = []

        # 删除今日数据
        for d in self.data_list[:]:
            if d["create_date"] == {"year": year, "month": month, "day": day}:
                self.data_list.remove(d)

        # 存入今日数据
        for t in self.bar_list:
            data = {"title": t.h_title, "hour": t.h_hour,
                    "minute": t.h_minute,
                    "create_date": t.create_date,
                    "create_time": t.create_time,
                    "finished": t.h_is_finished
                    }
            self.data_list.append(data)

        new_data["mydays"] = self.data_list

        path = "data/myday/" + str(year) + "_" + str(month) + "_" + "myday_data.json"

        exist = False
        if os.path.exists(path):
            for h in local_data:
                if h["data"] == day:
                    h["mydays"] = self.data_list
                    exist = True
            if not exist is True:
                local_data.append(new_data)
        else:
            local_data_temp = {"data": day,
                          "mydays": self.data_list}
            local_data.append(local_data_temp)

        with open(path, "w") as f:
            json.dump(local_data, f)


class MyDayPunchInterface(QFrame):
    h_width = 500
    h_height = 500
    space_top = 30

    space_left = 40

    #基本控件
    h_edit_window = None
    h_listbox = None
    h_addbutton = None
    h_show_calendar_button=None
    h_gold_coin=None
    h_statistic=None
    h_name_label=None

    m_data = None
    h_data_list = None
    h_message_box=None

    h_date=None

    def __init__(self, parent, edit_window,gold_coin,statistic):
        super(MyDayPunchInterface, self).__init__()
        self.setParent(parent)
        #基本控件初始化
        self.h_edit_window = edit_window
        self.h_gold_coin=gold_coin
        self.h_statistic=statistic


        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()

        self.h_name_label=QLabel(self)
        self.h_listbox = MyDayListBox(self, self.h_edit_window,self.h_gold_coin,self.h_statistic)
        self.h_date=DateController(year,month,day)
        self.h_addbutton = AddButton(self, self.h_listbox,self.h_date)
        self.h_show_calendar_button=ShowCalendarButton(self,self.h_listbox)
        self.h_message_box=MessageBox(self)


        self.h_listbox.h_calendar.init_list_box(self)
        self.h_addbutton._not_add_signal.connect(lambda :self.h_message_box.wake_up("请在当前日期添加"))

        # 这是滚动区域拖动文本联动滚动条
        self.scroll_bar = self.h_listbox.verticalScrollBar()
        self.h_listbox.installEventFilter(self)
        self.last_time_move = 0

        # 布置界面以及显示
        self.init_ui()

        # 本地数据载入


        path = "data/myday/" + str(year) + "_" + str(month) + "_" + "myday_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)
            if local_data:
                temp = local_data[0]
                for h in local_data[:]:
                    if h["data"] == day:
                        self.h_data_list = h["mydays"]
                        old_day = temp["data"]
                    temp = h
                if not self.h_data_list is None:
                    self.init_data()

    # 本地数据载入
    def init_data(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        for i in self.h_data_list:
            if i["create_date"]["year"] == year and i["create_date"]["month"] == month and i["create_date"]["day"] == day:
                self.h_listbox.add_from_local(i)

    def init_data_by_calendar(self, year, month, day, weekday):
        self.h_date.year=year
        self.h_date.month=month
        self.h_date.day=day
        path = "data/myday/" + str(year) + "_" + str(
            month) + "_" + "myday_data.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)

                for h in local_data:
                    if h["data"] == day:
                        self.h_data_list = h["mydays"]

        self.h_listbox.all_hide()
        self.h_listbox.bar_list.clear()
        self.h_listbox.referesh_list_box()


        if(self.h_data_list !=None):
            for i in self.h_data_list:
                if i["create_date"]["year"] == year and i["create_date"]["month"] == month and i["create_date"]["day"] == day:
                    self.h_listbox.add_from_local(i)
            # self.h_listbox.refresh_sort()

    def init_ui(self):
        self.setGraphicsEffect(get_shadow_effect(self))

        self.setObjectName("my_day_punch_interface")

        self.resize(self.h_width, self.h_height)

        #控件位移
        self.h_listbox.move(self.space_left, self.space_top)
        self.h_addbutton.move(25,self.h_height-self.h_addbutton.h_height-25)
        self.h_show_calendar_button.move(self.h_width-self.h_show_calendar_button.h_width-25,self.h_height-self.h_show_calendar_button.h_height-25)
        self.h_message_box.move(25,self.h_height-self.h_addbutton.h_height-25)

        #name_label样式
        self.h_name_label.resize(250,70)
        self.h_name_label.setObjectName("my_day_name_label")
        self.h_name_label.move(25,self.h_height-self.h_addbutton.h_height-25)
        self.h_name_label.setProperty('class','info_font')
        self.h_name_label.setText('          我的一天')
        self.h_name_label.setGraphicsEffect(get_shadow_effect(self))

        self.h_message_box.hide()

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


class MyDayCalendar(QFrame):
    h_width=None
    h_height=None

    background_label=None
    calendar=None
    style_file_path = 'gui/habit_widget.qss'

    def __init__(self):
        super(MyDayCalendar, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)

        self.background_label = QLabel(self)
        self.calendar=CalendarWidget(self)

        self.h_width=self.calendar.h_width
        self.h_height=self.calendar.h_height

        self.calendar._close_widget_signal.connect(self.close)

        self.init_ui()

    def init_ui(self):
        self.resize(self.h_width,self.h_height)
        self.background_label.resize(self.h_width,self.h_height)
        self.background_label.setObjectName("calendar_background")
        self.background_label.setGeometry(0,0,self.h_width,self.h_height)
        self.load_qss_style()

    def load_qss_style(self):
        file = open(self.style_file_path, 'r', encoding='utf-8')
        style_content = file.read()
        self.setStyleSheet(style_content)

    def select_and_close(self):
        self.close()

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