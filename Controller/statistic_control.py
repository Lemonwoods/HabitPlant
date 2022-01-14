import json
import os
import time
import calendar
from PyQt5.QtCore import QDate,QObject,QTimer
from PyQt5.Qt import pyqtSignal

class StatisticController(QObject):
    #信号定义
    #to_do到达提醒时间的信号
    _ready_todo_signal=pyqtSignal(list)

    # 目前
    last_use_time = {
                        "year": 1970,
                        "month": 1,
                        "day": 1
                    }
    to_do_unfinished_count = 0
    to_do_finished_count = 0
    my_day_unfinished_count = 0
    my_day_finished_count = 0
    habit_unfinished_count = 0
    habit_finished_count = 0
    full_days_counts=0
    total_use_days = 0
    is_all_finished=False

    #用于推送给植物的
    is_last_time_all_finished=False

    #用于推送的字典
    unfininshed_msg={
        "todo":0,
        "myday":0,
        "habit":0
    }

    myday_week_finished={
        '0':0,
        '1':0,
        '2':0,
        '3':0,
        '4':0,
        '5':0,
        '6':0
    }

    habit_week_finished={
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0
    }

    #用于存储今天的todo 用来倒计时还有多久去搜索todo的计时器
    today_todo_list = []
    search_timer=None

    def __init__(self):
        super(StatisticController, self).__init__()
        # 初始化本地存储文件
        path = "data/statistic.json"
        if not os.path.exists(path):
            with open(path, "w") as f:
                data = {
                    "last_use_time": {
                        "year": 1970,
                        "month": 1,
                        "day": 1
                    },
                    "habit_unfinished_count":0,
                    "habit_finished_count": 0,
                    "myday_unfinished_count": 0,
                    "myday_finished_count": 0,
                    "to_do_finished_count":0,
                    "to_do_unfinished_count":0,
                    "is_all_finished":False,
                    "full_days_counts":0,
                    "total_use_days": 0,
                    "is_last_time_all_finished":False
                }
                json.dump(data, f)
        else:
            try:
                with open(path, "r") as f:
                    local_data = json.load(f)
                    self.last_use_time = local_data["last_use_time"]
                    self.habit_finished_count = local_data["habit_finished_count"]
                    self.habit_unfinished_count = local_data["habit_unfinished_count"]
                    self.my_day_finished_count = local_data["myday_finished_count"]
                    self.my_day_unfinished_count = local_data["myday_unfinished_count"]
                    self.full_days_counts=local_data["full_days_counts"]
                    self.total_use_days = local_data["total_use_days"]
                    self.is_all_finished=local_data["is_all_finished"]
                    self.is_last_time_all_finished=local_data["is_last_time_all_finished"]
            except:
                pass

        self.to_do_unfinished_count=self.todo_unfinished_counts()
        self.my_day_unfinished_count=self.myday_unfinished_counts()
        self.habit_unfinished_count=self.habit_unfinished_counts()

        self.get_today_todo()
        self.search_timer=QTimer(self)
        self.search_timer.timeout.connect(self.push_ready_todo)
        self.search_timer.start(60000)

        self.my_day_week_info()
        self.habit_week_info()
        self.increase_full_day_count()

    # 计算难度值
    def difficult_number(self):
        pass

    # 判断一段时间内目标是否完成
    def is_finished_period(self, start_date, day_diff):
        pass

    # 定时事项推送
    def specific_time_info(self):
        pass

    # 统计今日habit未完成数量
    def habit_unfinished_counts(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        path = "data/habit/" + str(year) + "_" + str(month) + "_" + "habit_data.json"

        count = 0
        h_data_list = None
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)

            for h in local_data:
                if h["data"] == day:
                    h_data_list = h["habits"]
            if(h_data_list!=None):
                for h in h_data_list:
                    if h["finished"] is False:
                        count += 1

        return count

    # 统计今日myday未完成数量
    def myday_unfinished_counts(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        path = "data/myday/" + str(year) + "_" + str(month) + "_" + "myday_data.json"

        count = 0
        h_data_list = None
        if os.path.exists(path):
            with open(path, "r") as f:
                local_data = json.load(f)
                for h in local_data:
                    if h["data"] == day:
                        h_data_list = h["mydays"]
            if(h_data_list!=None):
                for h in h_data_list:
                    if h["finished"] is False:
                        count += 1

        return count

    def todo_unfinished_counts(self):
        path = "data/todo/todo_data.json"
        count = 0
        try:
            with open(path, "r") as f:
                local_data = json.load(f)
            for data in local_data:
                if data["finished"] is False:
                    count+=1
        except IOError as e:
            pass
        return count

    def my_day_week_info(self):
        try:
            year=QDate.currentDate().year()
            now_week=QDate.currentDate().dayOfWeek()
            now_day=QDate.currentDate().day()
            now_month=QDate.currentDate().month()
            for i in range(now_week):
                day=now_day-(now_week-1)+i
                if(day>0):
                    month=now_month
                else:
                    month=now_month-1
                    day=calendar.monthrange(year,month)[1]+day
                path = "data/myday/" + str(year) + "_" + str(month) + "_" + "myday_data.json"
                try:
                    count=0
                    temp_data_list=None
                    with open(path, "r") as f:
                        data_list = json.load(f)
                        for data in data_list:
                            if data["data"]==day:
                                temp_data_list = data["mydays"]
                        if (temp_data_list != None):
                            for data in temp_data_list:
                                if data["finished"] is True:
                                    count += 1
                    self.myday_week_finished[str(i)]=count
                except IOError as e:
                    self.myday_week_finished[str(i)]=count

            while(now_week!=7):
                self.myday_week_finished[str(now_week)]=0
                now_week+=1
        except Exception:
            pass

    def habit_week_info(self):
        try:
            year=QDate.currentDate().year()
            now_week=QDate.currentDate().dayOfWeek()
            now_day=QDate.currentDate().day()
            now_month=QDate.currentDate().month()
            for i in range(now_week):
                day=now_day-(now_week-1)+i
                if(day>0):
                    month=now_month
                else:
                    month=now_month-1
                    day=calendar.monthrange(year,month)[1]+day
                path = "data/habit/" + str(year) + "_" + str(month) + "_" + "habit_data.json"
                try:
                    count = 0
                    temp_data_list = None
                    with open(path, "r") as f:
                        data_list = json.load(f)
                        for data in data_list:
                            if data["data"] == day:
                                temp_data_list = data["habits"]
                        if (temp_data_list != None):
                            for data in temp_data_list:
                                if data["finished"] is True:
                                    count += 1
                    self.habit_week_finished[str(i)]=count
                except IOError as e :
                    self.habit_week_finished[str(i)]=count
            while(now_week!=7):
                self.habit_week_finished[str(now_week)]=0
                now_week+=1
        except Exception:
            pass

    # 统计一共使用软件天数
    def use_days(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        if( day!=int(self.last_use_time["day"]) or month!=int(self.last_use_time["month"]) or year!=int(self.last_use_time["year"])):
            self.total_use_days+=1
            self.last_use_time["year"]=year
            self.last_use_time["month"]=month
            self.last_use_time["day"]=day

    def increase_full_day_count(self):
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        if (day != int(self.last_use_time["day"]) or month != int(self.last_use_time["month"]) or year != int(self.last_use_time["year"])):
            if(self.is_all_finished==True):
                self.full_days_counts+=1
                self.is_all_finished=False
                self.is_last_time_all_finished=True
            else:
                self.is_all_finished=False
                self.is_last_time_all_finished=False


    # 今天是否完全打卡 如果完全打卡则记录天数 如果未完全打卡完成则不记录
    def is_full_day(self):
        if(self.habit_unfinished_count==0 and self.my_day_unfinished_count==0):
                #检验今天有没有设置任务 不设置任务不算
                if(self.habit_finished_count!=0 or self.my_day_finished_count!=0):
                   self.is_all_finished=True
        else:
                self.is_all_finished=False


    # 保存数据到本地
    def save_to_local(self):
        #在摧毁前判断今天任务是否已经全部完成
        self.is_full_day()
        self.use_days()
        path = "data/statistic.json"
        with open(path, "w") as f:
            data = {
                "last_use_time": self.last_use_time,
                "habit_unfinished_count": self.habit_unfinished_count,
                "habit_finished_count": self.habit_finished_count,
                "myday_unfinished_count": self.my_day_unfinished_count,
                "myday_finished_count": self.my_day_finished_count,
                "full_days_counts":self.full_days_counts,
                "total_use_days": self.total_use_days,
                "is_all_finished":self.is_all_finished,
                "is_last_time_all_finished":self.is_last_time_all_finished
            }
            json.dump(data, f)

    def get_today_todo(self):
        # 获取今天的待办
        self.today_todo_list.clear()
        year = QDate().currentDate().year()
        month = QDate().currentDate().month()
        day = QDate().currentDate().day()
        path = "data/todo/todo_data.json"
        try:
            with open(path, "r") as f:
                local_data = json.load(f)
            try:
                for data in local_data:
                    if (int(data["year"]) == year and int(data["month"]) == month and int(data["day"])==day):
                        self.today_todo_list.append(data)
            except Exception as e:
                pass
        except IOError as e:
            pass

    #推送即将到达时间的待办
    def push_ready_todo(self):
        # 将即将到达时间的待办推送
        is_changed=False
        ready_todo_list=[]
        now_time = time.localtime(time.time())
        try:
            for data in self.today_todo_list:
                if(int(data["hour"])==now_time.tm_hour and not(int(data["hour"])==0 and int(data["minute"])==0)):
                    if(int(data["minute"])-now_time.tm_min==10 or int(data["minute"])-now_time.tm_min==0):
                        data["type"]=int(data["minute"])-now_time.tm_min
                        ready_todo_list.append(data)
                        is_changed=True
        except Exception as e:
            pass
        if(is_changed):
            self._ready_todo_signal.emit(ready_todo_list)


